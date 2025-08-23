"""
Endpoints para gerenciamento de projetos
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc, asc
from sqlalchemy.orm import selectinload, joinedload
import os
import uuid
from datetime import datetime, date

from app.core.database import get_async_db
from app.core.security import get_current_user, get_current_active_user
from app.models.project import Project, ProjectMember, ProjectVersion, ProjectFile, ProjectTemplate
from app.models.user import User
from app.schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectResponse, ProjectDetailResponse,
    ProjectListResponse, ProjectSearchQuery, ProjectMemberCreate, ProjectMemberUpdate,
    ProjectMemberResponse, ProjectMemberListResponse, ProjectVersionCreate,
    ProjectVersionUpdate, ProjectVersionResponse, ProjectFileCreate, ProjectFileUpdate,
    ProjectFileResponse, ProjectTemplateCreate, ProjectTemplateUpdate, ProjectTemplateResponse
)
from app.websockets.manager import websocket_manager

router = APIRouter()


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Criar novo projeto
    """
    # Verificar se o usuário tem permissão para criar projetos
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não está ativo"
        )
    
    # Criar projeto
    db_project = Project(
        name=project_data.name,
        description=project_data.description,
        status=project_data.status,
        priority=project_data.priority,
        visibility=project_data.visibility,
        start_date=project_data.start_date,
        due_date=project_data.due_date,
        tags=project_data.tags,
        metadata=project_data.metadata,
        owner_id=current_user.id,
        parent_project_id=project_data.parent_project_id,
        template_id=project_data.template_id
    )
    
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    
    # Adicionar usuário como membro com papel de owner
    project_member = ProjectMember(
        user_id=current_user.id,
        project_id=db_project.id,
        role="owner",
        joined_at=datetime.utcnow()
    )
    
    db.add(project_member)
    await db.commit()
    
    # Notificar via WebSocket
    await websocket_manager.broadcast_to_user(
        current_user.id,
        {
            "type": "project_created",
            "project_id": db_project.id,
            "project_name": db_project.name
        }
    )
    
    return db_project


@router.get("/", response_model=ProjectListResponse)
async def get_projects(
    query: Optional[str] = Query(None, description="Termo de busca"),
    status_filter: Optional[str] = Query(None, description="Filtrar por status"),
    priority_filter: Optional[str] = Query(None, description="Filtrar por prioridade"),
    visibility_filter: Optional[str] = Query(None, description="Filtrar por visibilidade"),
    owner_id: Optional[int] = Query(None, description="Filtrar por proprietário"),
    member_id: Optional[int] = Query(None, description="Filtrar por membro"),
    tags: Optional[List[str]] = Query(None, description="Filtrar por tags"),
    start_date_from: Optional[date] = Query(None, description="Data de início a partir de"),
    start_date_to: Optional[date] = Query(None, description="Data de início até"),
    due_date_from: Optional[date] = Query(None, description="Data de vencimento a partir de"),
    due_date_to: Optional[date] = Query(None, description="Data de vencimento até"),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(20, ge=1, le=100, description="Tamanho da página"),
    sort_by: str = Query("created_at", description="Campo para ordenação"),
    sort_order: str = Query("desc", description="Ordem da ordenação (asc/desc)"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Listar projetos (filtrados por permissões do usuário)
    """
    # Construir query base - apenas projetos que o usuário pode ver
    base_query = select(Project).join(ProjectMember).where(
        ProjectMember.user_id == current_user.id
    )
    
    # Aplicar filtros
    filters = []
    
    if query:
        filters.append(
            or_(
                Project.name.ilike(f"%{query}%"),
                Project.description.ilike(f"%{query}%")
            )
        )
    
    if status_filter:
        filters.append(Project.status == status_filter)
    
    if priority_filter:
        filters.append(Project.priority == priority_filter)
    
    if visibility_filter:
        filters.append(Project.visibility == visibility_filter)
    
    if owner_id:
        filters.append(Project.owner_id == owner_id)
    
    if tags:
        for tag in tags:
            filters.append(Project.tags.contains([tag]))
    
    if start_date_from:
        filters.append(Project.start_date >= start_date_from)
    
    if start_date_to:
        filters.append(Project.start_date <= start_date_to)
    
    if due_date_from:
        filters.append(Project.due_date >= due_date_from)
    
    if due_date_to:
        filters.append(Project.due_date <= due_date_to)
    
    if filters:
        base_query = base_query.where(and_(*filters))
    
    # Aplicar ordenação
    if hasattr(Project, sort_by):
        order_column = getattr(Project, sort_by)
        if sort_order.lower() == "desc":
            base_query = base_query.order_by(desc(order_column))
        else:
            base_query = base_query.order_by(asc(order_column))
    else:
        # Ordenação padrão
        base_query = base_query.order_by(desc(Project.created_at))
    
    # Contar total
    count_query = select(func.count()).select_from(base_query.subquery())
    total = await db.execute(count_query)
    total_count = total.scalar()
    
    # Aplicar paginação
    offset = (page - 1) * size
    projects_query = base_query.offset(offset).limit(size)
    
    # Executar query
    result = await db.execute(projects_query)
    projects = result.scalars().all()
    
    # Calcular páginas
    pages = (total_count + size - 1) // size
    
    return ProjectListResponse(
        projects=projects,
        total=total_count,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/{project_id}", response_model=ProjectDetailResponse)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Obter detalhes de um projeto específico
    """
    # Verificar se o usuário é membro do projeto
    project_member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == current_user.id
            )
        )
    )
    
    if not project_member.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado ao projeto"
        )
    
    # Buscar projeto com relacionamentos
    project_query = select(Project).options(
        selectinload(Project.owner),
        selectinload(Project.parent_project),
        selectinload(Project.members).selectinload(ProjectMember.user)
    ).where(Project.id == project_id)
    
    result = await db.execute(project_query)
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )
    
    # Buscar estatísticas
    tasks_count = 0  # Implementar quando tiver o modelo de tarefas
    completed_tasks = 0  # Implementar quando tiver o modelo de tarefas
    
    # Calcular progresso
    progress = 0.0
    if tasks_count > 0:
        progress = (completed_tasks / tasks_count) * 100
    
    # Buscar atividades recentes
    recent_activities = []  # Implementar quando tiver o modelo de atividades
    
    # Buscar estatísticas
    statistics = {
        "total_members": len(project.members),
        "total_tasks": tasks_count,
        "completed_tasks": completed_tasks,
        "progress": progress
    }
    
    return ProjectDetailResponse(
        **project.__dict__,
        progress=progress,
        total_tasks=tasks_count,
        completed_tasks=completed_tasks,
        total_members=len(project.members),
        owner=project.owner.__dict__ if project.owner else None,
        parent_project=project.parent_project.__dict__ if project.parent_project else None,
        members=[member.__dict__ for member in project.members],
        recent_activities=recent_activities,
        statistics=statistics
    )


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Atualizar projeto
    """
    # Verificar se o usuário tem permissão para editar o projeto
    project_member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == current_user.id
            )
        )
    )
    
    member = project_member.scalar_one_or_none()
    if not member or member.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente para editar o projeto"
        )
    
    # Buscar projeto
    project_query = select(Project).where(Project.id == project_id)
    result = await db.execute(project_query)
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )
    
    # Atualizar campos
    update_data = project_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    project.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(project)
    
    # Notificar via WebSocket
    await websocket_manager.broadcast_to_room(
        f"project_{project_id}",
        {
            "type": "project_updated",
            "project_id": project.id,
            "project_name": project.name,
            "updated_by": current_user.id
        }
    )
    
    return project


@router.delete("/{project_id}", status_code=status.HTTP_200_OK)
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Deletar projeto
    """
    # Verificar se o usuário é o proprietário do projeto
    project_query = select(Project).where(Project.id == project_id)
    result = await db.execute(project_query)
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )
    
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas o proprietário pode deletar o projeto"
        )
    
    # Soft delete - marcar como arquivado
    project.status = "archived"
    project.archived_at = datetime.utcnow()
    project.updated_at = datetime.utcnow()
    
    await db.commit()
    
    # Notificar via WebSocket
    await websocket_manager.broadcast_to_room(
        f"project_{project_id}",
        {
            "type": "project_archived",
            "project_id": project.id,
            "project_name": project.name,
            "archived_by": current_user.id
        }
    )
    
    return {"message": "Projeto arquivado com sucesso"}


@router.post("/{project_id}/members", response_model=ProjectMemberResponse, status_code=status.HTTP_201_CREATED)
async def add_project_member(
    project_id: int,
    member_data: ProjectMemberCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Adicionar membro ao projeto
    """
    # Verificar se o usuário tem permissão para adicionar membros
    project_member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == current_user.id
            )
        )
    )
    
    member = project_member.scalar_one_or_none()
    if not member or member.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente para adicionar membros"
        )
    
    # Verificar se o usuário já é membro
    existing_member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == member_data.user_id
            )
        )
    )
    
    if existing_member.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já é membro do projeto"
        )
    
    # Verificar se o usuário existe
    user_query = select(User).where(User.id == member_data.user_id)
    result = await db.execute(user_query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Adicionar membro
    project_member = ProjectMember(
        user_id=member_data.user_id,
        project_id=project_id,
        role=member_data.role,
        permissions=member_data.permissions,
        joined_at=datetime.utcnow()
    )
    
    db.add(project_member)
    await db.commit()
    await db.refresh(project_member)
    
    # Notificar via WebSocket
    await websocket_manager.broadcast_to_user(
        member_data.user_id,
        {
            "type": "project_invitation",
            "project_id": project_id,
            "invited_by": current_user.id
        }
    )
    
    return project_member


@router.get("/{project_id}/members", response_model=ProjectMemberListResponse)
async def get_project_members(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Listar membros do projeto
    """
    # Verificar se o usuário é membro do projeto
    project_member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == current_user.id
            )
        )
    )
    
    if not project_member.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado ao projeto"
        )
    
    # Buscar membros
    members_query = select(ProjectMember).options(
        selectinload(ProjectMember.user)
    ).where(ProjectMember.project_id == project_id)
    
    result = await db.execute(members_query)
    members = result.scalars().all()
    
    # Formatar resposta
    formatted_members = []
    for member in members:
        member_dict = member.__dict__.copy()
        member_dict["user"] = member.user.__dict__ if member.user else None
        formatted_members.append(member_dict)
    
    return ProjectMemberListResponse(
        members=formatted_members,
        total=len(formatted_members)
    )


@router.put("/{project_id}/members/{member_id}", response_model=ProjectMemberResponse)
async def update_project_member(
    project_id: int,
    member_id: int,
    member_data: ProjectMemberUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Atualizar membro do projeto
    """
    # Verificar se o usuário tem permissão para editar membros
    project_member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == current_user.id
            )
        )
    )
    
    member = project_member.scalar_one_or_none()
    if not member or member.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente para editar membros"
        )
    
    # Buscar membro a ser editado
    target_member_query = select(ProjectMember).where(
        and_(
            ProjectMember.id == member_id,
            ProjectMember.project_id == project_id
        )
    )
    
    result = await db.execute(target_member_query)
    target_member = result.scalar_one_or_none()
    
    if not target_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membro não encontrado"
        )
    
    # Não permitir alterar o papel do proprietário
    if target_member.role == "owner":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível alterar o papel do proprietário"
        )
    
    # Atualizar campos
    update_data = member_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(target_member, field, value)
    
    await db.commit()
    await db.refresh(target_member)
    
    return target_member


@router.delete("/{project_id}/members/{member_id}", status_code=status.HTTP_200_OK)
async def remove_project_member(
    project_id: int,
    member_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Remover membro do projeto
    """
    # Verificar se o usuário tem permissão para remover membros
    project_member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == current_user.id
            )
        )
    )
    
    member = project_member.scalar_one_or_none()
    if not member or member.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente para remover membros"
        )
    
    # Buscar membro a ser removido
    target_member_query = select(ProjectMember).where(
        and_(
            ProjectMember.id == member_id,
            ProjectMember.project_id == project_id
        )
    )
    
    result = await db.execute(target_member_query)
    target_member = result.scalar_one_or_none()
    
    if not target_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membro não encontrado"
        )
    
    # Não permitir remover o proprietário
    if target_member.role == "owner":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível remover o proprietário do projeto"
        )
    
    # Remover membro
    await db.delete(target_member)
    await db.commit()
    
    return {"message": "Membro removido com sucesso"}


@router.post("/{project_id}/versions", response_model=ProjectVersionResponse, status_code=status.HTTP_201_CREATED)
async def create_project_version(
    project_id: int,
    version_data: ProjectVersionCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Criar nova versão do projeto
    """
    # Verificar se o usuário tem permissão para criar versões
    project_member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == current_user.id
            )
        )
    )
    
    member = project_member.scalar_one_or_none()
    if not member or member.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente para criar versões"
        )
    
    # Verificar se o projeto existe
    project_query = select(Project).where(Project.id == project_id)
    result = await db.execute(project_query)
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )
    
    # Criar versão
    project_version = ProjectVersion(
        project_id=project_id,
        version_number=version_data.version_number,
        description=version_data.description,
        changes=version_data.changes,
        is_released=version_data.is_released,
        release_notes=version_data.release_notes,
        created_by=current_user.id
    )
    
    db.add(project_version)
    await db.commit()
    await db.refresh(project_version)
    
    return project_version


@router.get("/{project_id}/versions", response_model=List[ProjectVersionResponse])
async def get_project_versions(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Listar versões do projeto
    """
    # Verificar se o usuário é membro do projeto
    project_member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == current_user.id
            )
        )
    )
    
    if not project_member.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado ao projeto"
        )
    
    # Buscar versões
    versions_query = select(ProjectVersion).where(
        ProjectVersion.project_id == project_id
    ).order_by(desc(ProjectVersion.created_at))
    
    result = await db.execute(versions_query)
    versions = result.scalars().all()
    
    return versions


@router.post("/{project_id}/files", response_model=ProjectFileResponse, status_code=status.HTTP_201_CREATED)
async def upload_project_file(
    project_id: int,
    file: UploadFile = File(...),
    description: Optional[str] = Query(None, description="Descrição do arquivo"),
    tags: Optional[List[str]] = Query(None, description="Tags do arquivo"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Fazer upload de arquivo para o projeto
    """
    # Verificar se o usuário é membro do projeto
    project_member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == current_user.id
            )
        )
    )
    
    if not project_member.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado ao projeto"
        )
    
    # Verificar se o projeto existe
    project_query = select(Project).where(Project.id == project_id)
    result = await db.execute(project_query)
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )
    
    # Validar arquivo
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome do arquivo é obrigatório"
        )
    
    # Gerar nome único para o arquivo
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # Salvar arquivo (implementar lógica de armazenamento)
    file_path = f"uploads/projects/{project_id}/{unique_filename}"
    
    # Criar registro do arquivo
    project_file = ProjectFile(
        project_id=project_id,
        filename=unique_filename,
        original_filename=file.filename,
        file_path=file_path,
        file_size=0,  # Implementar quando tiver o arquivo
        mime_type=file.content_type or "application/octet-stream",
        description=description,
        tags=tags,
        uploaded_by=current_user.id
    )
    
    db.add(project_file)
    await db.commit()
    await db.refresh(project_file)
    
    return project_file


@router.get("/{project_id}/files", response_model=List[ProjectFileResponse])
async def get_project_files(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Listar arquivos do projeto
    """
    # Verificar se o usuário é membro do projeto
    project_member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == current_user.id
            )
        )
    )
    
    if not project_member.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado ao projeto"
        )
    
    # Buscar arquivos
    files_query = select(ProjectFile).where(
        ProjectFile.project_id == project_id
    ).order_by(desc(ProjectFile.upload_date))
    
    result = await db.execute(files_query)
    files = result.scalars().all()
    
    return files


@router.get("/templates", response_model=List[ProjectTemplateResponse])
async def get_project_templates(
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    is_public: Optional[bool] = Query(True, description="Filtrar por visibilidade"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Listar templates de projeto disponíveis
    """
    # Construir query base
    base_query = select(ProjectTemplate).where(ProjectTemplate.is_active == True)
    
    # Aplicar filtros
    if category:
        base_query = base_query.where(ProjectTemplate.category == category)
    
    if is_public is not None:
        base_query = base_query.where(ProjectTemplate.is_public == is_public)
    
    # Ordenar por uso
    base_query = base_query.order_by(desc(ProjectTemplate.usage_count))
    
    result = await db.execute(base_query)
    templates = result.scalars().all()
    
    return templates


@router.post("/templates", response_model=ProjectTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_project_template(
    template_data: ProjectTemplateCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Criar template de projeto
    """
    # Verificar se o usuário tem permissão para criar templates
    if current_user.role not in ["admin", "superuser"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente para criar templates"
        )
    
    # Criar template
    project_template = ProjectTemplate(
        name=template_data.name,
        description=template_data.description,
        category=template_data.category,
        is_public=template_data.is_public,
        structure=template_data.structure,
        created_by=current_user.id
    )
    
    db.add(project_template)
    await db.commit()
    await db.refresh(project_template)
    
    return project_template
