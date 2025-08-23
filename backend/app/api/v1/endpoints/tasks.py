"""
Endpoints para gerenciamento de tarefas
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload

from app.core.database import get_async_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.project import Project, ProjectMember
from app.models.task import Task, TimeLog, TaskAttachment, TaskDependency
from app.schemas.task import (
    TaskCreate, TaskUpdate, TaskResponse, TaskDetailResponse,
    TaskListResponse, TaskSearchQuery, TimeLogCreate, TimeLogUpdate,
    TimeLogResponse, TaskAttachmentCreate, TaskAttachmentResponse,
    TaskDependencyCreate, TaskDependencyResponse, TaskBulkUpdate
)
from app.core.websocket import websocket_manager

router = APIRouter()


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Criar nova tarefa
    """
    # Verificar se o projeto existe e o usuário tem acesso
    project = await db.execute(
        select(Project).where(Project.id == task_data.project_id)
    )
    project = project.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado"
        )
    
    # Verificar se o usuário é membro do projeto
    member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == task_data.project_id,
                ProjectMember.user_id == current_user.id
            )
        )
    )
    member = member.scalar_one_or_none()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não tem acesso ao projeto"
        )
    
    # Verificar se a tarefa pai existe (se especificada)
    if task_data.parent_task_id:
        parent_task = await db.execute(
            select(Task).where(Task.id == task_data.parent_task_id)
        )
        parent_task = parent_task.scalar_one_or_none()
        
        if not parent_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarefa pai não encontrada"
            )
        
        if parent_task.project_id != task_data.project_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tarefa pai deve pertencer ao mesmo projeto"
            )
    
    # Criar tarefa
    db_task = Task(
        name=task_data.name,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        type=task_data.type,
        start_date=task_data.start_date,
        due_date=task_data.due_date,
        estimated_hours=task_data.estimated_hours,
        project_id=task_data.project_id,
        assignee_id=task_data.assignee_id,
        parent_task_id=task_data.parent_task_id,
        tags=task_data.tags,
        metadata=task_data.metadata,
        created_by=current_user.id
    )
    
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    
    # Notificar via WebSocket
    await websocket_manager.broadcast_to_project(
        task_data.project_id,
        {
            "type": "task_created",
            "task_id": db_task.id,
            "task_name": db_task.name,
            "project_id": db_task.project_id
        }
    )
    
    return db_task


@router.get("/", response_model=TaskListResponse)
async def get_tasks(
    project_id: Optional[int] = Query(None, description="ID do projeto"),
    assignee_id: Optional[int] = Query(None, description="ID do responsável"),
    status: Optional[str] = Query(None, description="Status da tarefa"),
    priority: Optional[str] = Query(None, description="Prioridade da tarefa"),
    search: Optional[str] = Query(None, description="Termo de busca"),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(20, ge=1, le=100, description="Tamanho da página"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Listar tarefas com filtros e paginação
    """
    # Construir query base
    query = select(Task).options(
        selectinload(Task.assignee),
        selectinload(Task.project),
        selectinload(Task.parent_task)
    )
    
    # Aplicar filtros
    filters = []
    
    if project_id:
        # Verificar se o usuário tem acesso ao projeto
        member = await db.execute(
            select(ProjectMember).where(
                and_(
                    ProjectMember.project_id == project_id,
                    ProjectMember.user_id == current_user.id
                )
            )
        )
        if not member.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário não tem acesso ao projeto"
            )
        filters.append(Task.project_id == project_id)
    
    if assignee_id:
        filters.append(Task.assignee_id == assignee_id)
    
    if status:
        filters.append(Task.status == status)
    
    if priority:
        filters.append(Task.priority == priority)
    
    if search:
        search_filter = or_(
            Task.name.ilike(f"%{search}%"),
            Task.description.ilike(f"%{search}%")
        )
        filters.append(search_filter)
    
    # Aplicar filtros
    if filters:
        query = query.where(and_(*filters))
    
    # Contar total
    count_query = select(Task).where(and_(*filters) if filters else True)
    total = await db.scalar(select(func.count()).select_from(count_query.subquery()))
    
    # Aplicar paginação
    query = query.offset((page - 1) * size).limit(size)
    
    # Executar query
    result = await db.execute(query)
    tasks = result.scalars().all()
    
    return TaskListResponse(
        items=tasks,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.get("/{task_id}", response_model=TaskDetailResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Obter detalhes de uma tarefa
    """
    # Buscar tarefa com relacionamentos
    task = await db.execute(
        select(Task).options(
            selectinload(Task.assignee),
            selectinload(Task.project),
            selectinload(Task.parent_task),
            selectinload(Task.subtasks),
            selectinload(Task.comments),
            selectinload(Task.attachments),
            selectinload(Task.time_logs),
            selectinload(Task.dependencies)
        ).where(Task.id == task_id)
    )
    task = task.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    
    # Verificar se o usuário tem acesso ao projeto
    member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == task.project_id,
                ProjectMember.user_id == current_user.id
            )
        )
    )
    if not member.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não tem acesso ao projeto"
        )
    
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Atualizar tarefa
    """
    # Buscar tarefa
    task = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    task = task.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    
    # Verificar permissões (apenas responsável, criador ou admin do projeto)
    member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == task.project_id,
                ProjectMember.user_id == current_user.id
            )
        )
    )
    member = member.scalar_one_or_none()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não tem acesso ao projeto"
        )
    
    # Apenas responsável, criador ou admin pode editar
    can_edit = (
        task.assignee_id == current_user.id or
        task.created_by == current_user.id or
        member.role in ["admin", "owner"]
    )
    
    if not can_edit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não tem permissão para editar esta tarefa"
        )
    
    # Atualizar campos
    update_data = task_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    task.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(task)
    
    # Notificar via WebSocket
    await websocket_manager.broadcast_to_project(
        task.project_id,
        {
            "type": "task_updated",
            "task_id": task.id,
            "task_name": task.name,
            "project_id": task.project_id
        }
    )
    
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Excluir tarefa (soft delete)
    """
    # Buscar tarefa
    task = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    task = task.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    
    # Verificar permissões (apenas criador ou admin do projeto)
    member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == task.project_id,
                ProjectMember.user_id == current_user.id
            )
        )
    )
    member = member.scalar_one_or_none()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não tem acesso ao projeto"
        )
    
    # Apenas criador ou admin pode excluir
    can_delete = (
        task.created_by == current_user.id or
        member.role in ["admin", "owner"]
    )
    
    if not can_delete:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não tem permissão para excluir esta tarefa"
        )
    
    # Soft delete
    task.is_deleted = True
    task.deleted_at = datetime.utcnow()
    task.deleted_by = current_user.id
    
    await db.commit()
    
    # Notificar via WebSocket
    await websocket_manager.broadcast_to_project(
        task.project_id,
        {
            "type": "task_deleted",
            "task_id": task.id,
            "task_name": task.name,
            "project_id": task.project_id
        }
    )


@router.post("/{task_id}/assign", response_model=TaskResponse)
async def assign_task(
    task_id: int,
    assignee_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Atribuir tarefa a um usuário
    """
    # Buscar tarefa
    task = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    task = task.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    
    # Verificar permissões
    member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == task.project_id,
                ProjectMember.user_id == current_user.id
            )
        )
    )
    member = member.scalar_one_or_none()
    
    if not member or member.role not in ["admin", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não tem permissão para atribuir tarefas"
        )
    
    # Verificar se o novo responsável é membro do projeto
    new_assignee = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == task.project_id,
                ProjectMember.user_id == assignee_id
            )
        )
    )
    if not new_assignee.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário não é membro do projeto"
        )
    
    # Atribuir tarefa
    old_assignee_id = task.assignee_id
    task.assignee_id = assignee_id
    task.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(task)
    
    # Notificar via WebSocket
    await websocket_manager.broadcast_to_project(
        task.project_id,
        {
            "type": "task_assigned",
            "task_id": task.id,
            "task_name": task.name,
            "old_assignee_id": old_assignee_id,
            "new_assignee_id": assignee_id,
            "project_id": task.project_id
        }
    )
    
    return task


@router.post("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: int,
    new_status: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Atualizar status de uma tarefa
    """
    # Buscar tarefa
    task = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    task = task.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    
    # Verificar permissões
    member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == task.project_id,
                ProjectMember.user_id == current_user.id
            )
        )
    )
    member = member.scalar_one_or_none()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não tem acesso ao projeto"
        )
    
    # Apenas responsável, criador ou admin pode alterar status
    can_change = (
        task.assignee_id == current_user.id or
        task.created_by == current_user.id or
        member.role in ["admin", "owner"]
    )
    
    if not can_change:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não tem permissão para alterar status desta tarefa"
        )
    
    # Atualizar status
    old_status = task.status
    task.status = new_status
    task.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(task)
    
    # Notificar via WebSocket
    await websocket_manager.broadcast_to_project(
        task.project_id,
        {
            "type": "task_status_changed",
            "task_id": task.id,
            "task_name": task.name,
            "old_status": old_status,
            "new_status": new_status,
            "project_id": task.project_id
        }
    )
    
    return task


@router.post("/{task_id}/time-log", response_model=TimeLogResponse)
async def add_time_log(
    task_id: int,
    time_log_data: TimeLogCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Adicionar registro de tempo trabalhado
    """
    # Buscar tarefa
    task = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    task = task.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    
    # Verificar se o usuário tem acesso ao projeto
    member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == task.project_id,
                ProjectMember.user_id == current_user.id
            )
        )
    )
    if not member.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não tem acesso ao projeto"
        )
    
    # Criar registro de tempo
    time_log = TimeLog(
        task_id=task_id,
        user_id=current_user.id,
        hours_spent=time_log_data.hours_spent,
        description=time_log_data.description,
        date=time_log_data.date or datetime.utcnow().date()
    )
    
    db.add(time_log)
    await db.commit()
    await db.refresh(time_log)
    
    # Notificar via WebSocket
    await websocket_manager.broadcast_to_project(
        task.project_id,
        {
            "type": "time_log_added",
            "task_id": task_id,
            "time_log_id": time_log.id,
            "hours_spent": time_log.hours_spent,
            "project_id": task.project_id
        }
    )
    
    return time_log


@router.post("/{task_id}/dependencies", response_model=TaskDependencyResponse)
async def add_task_dependency(
    task_id: int,
    dependency_data: TaskDependencyCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Adicionar dependência entre tarefas
    """
    # Buscar tarefa
    task = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    task = task.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    
    # Verificar se a tarefa dependente existe
    dependent_task = await db.execute(
        select(Task).where(Task.id == dependency_data.dependent_task_id)
    )
    dependent_task = dependent_task.scalar_one_or_none()
    
    if not dependent_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa dependente não encontrada"
        )
    
    # Verificar se ambas as tarefas pertencem ao mesmo projeto
    if task.project_id != dependent_task.project_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tarefas devem pertencer ao mesmo projeto"
        )
    
    # Verificar permissões
    member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == task.project_id,
                ProjectMember.user_id == current_user.id
            )
        )
    )
    member = member.scalar_one_or_none()
    
    if not member or member.role not in ["admin", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não tem permissão para criar dependências"
        )
    
    # Verificar se a dependência já existe
    existing_dependency = await db.execute(
        select(TaskDependency).where(
            and_(
                TaskDependency.task_id == task_id,
                TaskDependency.dependent_task_id == dependency_data.dependent_task_id
            )
        )
    )
    if existing_dependency.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dependência já existe"
        )
    
    # Criar dependência
    dependency = TaskDependency(
        task_id=task_id,
        dependent_task_id=dependency_data.dependent_task_id,
        dependency_type=dependency_data.dependency_type,
        description=dependency_data.description
    )
    
    db.add(dependency)
    await db.commit()
    await db.refresh(dependency)
    
    return dependency


@router.delete("/{task_id}/dependencies/{dependency_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_task_dependency(
    task_id: int,
    dependency_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Remover dependência entre tarefas
    """
    # Buscar dependência
    dependency = await db.execute(
        select(TaskDependency).where(TaskDependency.id == dependency_id)
    )
    dependency = dependency.scalar_one_or_none()
    
    if not dependency or dependency.task_id != task_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dependência não encontrada"
        )
    
    # Verificar permissões
    member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == dependency.task.project_id,
                ProjectMember.user_id == current_user.id
            )
        )
    )
    member = member.scalar_one_or_none()
    
    if not member or member.role not in ["admin", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não tem permissão para remover dependências"
        )
    
    # Remover dependência
    await db.delete(dependency)
    await db.commit()


@router.post("/bulk-update", response_model=List[TaskResponse])
async def bulk_update_tasks(
    updates: TaskBulkUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Atualizar múltiplas tarefas de uma vez
    """
    if not updates.task_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lista de IDs de tarefas não pode estar vazia"
        )
    
    # Buscar tarefas
    tasks = await db.execute(
        select(Task).where(Task.id.in_(updates.task_ids))
    )
    tasks = tasks.scalars().all()
    
    if len(tasks) != len(updates.task_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Algumas tarefas não foram encontradas"
        )
    
    # Verificar se todas as tarefas pertencem ao mesmo projeto
    project_ids = {task.project_id for task in tasks}
    if len(project_ids) > 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Todas as tarefas devem pertencer ao mesmo projeto"
        )
    
    project_id = list(project_ids)[0]
    
    # Verificar permissões
    member = await db.execute(
        select(ProjectMember).where(
            and_(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == current_user.id
            )
        )
    )
    member = member.scalar_one_or_none()
    
    if not member or member.role not in ["admin", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não tem permissão para atualizar múltiplas tarefas"
        )
    
    # Aplicar atualizações
    update_data = updates.dict(exclude_unset=True, exclude={"task_ids"})
    
    for task in tasks:
        for field, value in update_data.items():
            setattr(task, field, value)
        task.updated_at = datetime.utcnow()
    
    await db.commit()
    
    # Notificar via WebSocket
    await websocket_manager.broadcast_to_project(
        project_id,
        {
            "type": "tasks_bulk_updated",
            "task_ids": updates.task_ids,
            "project_id": project_id
        }
    )
    
    return tasks
