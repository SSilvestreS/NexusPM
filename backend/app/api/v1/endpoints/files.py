"""
Endpoints para upload e gerenciamento de arquivos
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
import os
import aiofiles
import hashlib
from pathlib import Path

from app.core.database import get_async_db
from app.core.security import get_current_active_user
from app.core.config import settings
from app.models.user import User
from app.models.project import Project, ProjectMember
from app.models.task import Task
from app.models.project import ProjectFile
from app.schemas.file import (
    FileUploadResponse, FileListResponse, FileDetailResponse,
    FileUpdateRequest, FileMetadata
)
from app.core.websocket import websocket_manager

router = APIRouter()

# Configurações de upload
ALLOWED_EXTENSIONS = {
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
    'document': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
    'spreadsheet': ['.xls', '.xlsx', '.csv', '.ods'],
    'presentation': ['.ppt', '.pptx', '.odp'],
    'archive': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'code': ['.py', '.js', '.ts', '.html', '.css', '.json', '.xml', '.sql']
}

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB


@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    project_id: Optional[int] = Form(None),
    task_id: Optional[int] = Form(None),
    description: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Upload de arquivo para projeto ou tarefa
    """
    # Verificar se pelo menos um ID foi fornecido
    if not project_id and not task_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Deve especificar project_id ou task_id"
        )
    
    # Verificar tamanho do arquivo
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Arquivo muito grande. Tamanho máximo: {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    # Verificar extensão do arquivo
    file_extension = Path(file.filename).suffix.lower()
    allowed_extensions = []
    for ext_list in ALLOWED_EXTENSIONS.values():
        allowed_extensions.extend(ext_list)
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de arquivo não permitido. Extensões permitidas: {', '.join(allowed_extensions)}"
        )
    
    # Determinar projeto (se não fornecido diretamente)
    final_project_id = project_id
    if task_id and not project_id:
        task = await db.execute(
            select(Task).where(Task.id == task_id)
        )
        task = task.scalar_one_or_none()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarefa não encontrada"
            )
        final_project_id = task.project_id
    
    # Verificar permissões do projeto
    if final_project_id:
        member = await db.execute(
            select(ProjectMember).where(
                and_(
                    ProjectMember.project_id == final_project_id,
                    ProjectMember.user_id == current_user.id
                )
            )
        )
        if not member.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário não tem acesso ao projeto"
            )
    
    # Criar diretório de upload se não existir
    upload_dir = Path(settings.file_storage_path) / str(final_project_id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Gerar nome único para o arquivo
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file_hash = hashlib.md5(f"{file.filename}{timestamp}".encode()).hexdigest()[:8]
    safe_filename = f"{timestamp}_{file_hash}_{Path(file.filename).name}"
    file_path = upload_dir / safe_filename
    
    # Salvar arquivo
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar arquivo: {str(e)}"
        )
    
    # Determinar tipo de arquivo
    file_type = "other"
    for category, extensions in ALLOWED_EXTENSIONS.items():
        if file_extension in extensions:
            file_type = category
            break
    
    # Criar registro no banco
    db_file = ProjectFile(
        filename=file.filename,
        stored_filename=safe_filename,
        file_path=str(file_path),
        file_size=len(content),
        file_type=file_type,
        mime_type=file.content_type,
        description=description,
        tags=tags.split(',') if tags else [],
        project_id=final_project_id,
        task_id=task_id,
        uploaded_by=current_user.id
    )
    
    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)
    
    # Notificar via WebSocket
    if final_project_id:
        await websocket_manager.broadcast_to_project(
            final_project_id,
            {
                "type": "file_uploaded",
                "file_id": db_file.id,
                "filename": file.filename,
                "project_id": final_project_id,
                "task_id": task_id,
                "uploaded_by": current_user.id
            }
        )
    
    return FileUploadResponse(
        id=db_file.id,
        filename=file.filename,
        file_size=len(content),
        file_type=file_type,
        mime_type=file.content_type,
        project_id=final_project_id,
        task_id=task_id,
        uploaded_by=current_user.id,
        upload_date=datetime.utcnow()
    )


@router.get("/", response_model=FileListResponse)
async def list_files(
    project_id: Optional[int] = None,
    task_id: Optional[int] = None,
    file_type: Optional[str] = None,
    uploaded_by: Optional[int] = None,
    search: Optional[str] = None,
    page: int = 1,
    size: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Listar arquivos com filtros e paginação
    """
    # Construir query base
    query = select(ProjectFile).options(
        selectinload(ProjectFile.uploaded_by_user),
        selectinload(ProjectFile.project),
        selectinload(ProjectFile.task)
    )
    
    # Aplicar filtros
    filters = []
    
    if project_id:
        # Verificar permissões do projeto
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
        filters.append(ProjectFile.project_id == project_id)
    
    if task_id:
        # Verificar permissões da tarefa (através do projeto)
        task = await db.execute(
            select(Task).where(Task.id == task_id)
        )
        task = task.scalar_one_or_none()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarefa não encontrada"
            )
        
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
                detail="Usuário não tem acesso à tarefa"
            )
        filters.append(ProjectFile.task_id == task_id)
    
    if file_type:
        filters.append(ProjectFile.file_type == file_type)
    
    if uploaded_by:
        filters.append(ProjectFile.uploaded_by == uploaded_by)
    
    if search:
        search_filter = ProjectFile.filename.ilike(f"%{search}%")
        filters.append(search_filter)
    
    # Aplicar filtros
    if filters:
        query = query.where(and_(*filters))
    
    # Contar total
    count_query = select(ProjectFile).where(and_(*filters) if filters else True)
    total = await db.scalar(select(func.count()).select_from(count_query.subquery()))
    
    # Aplicar paginação
    query = query.offset((page - 1) * size).limit(size)
    
    # Executar query
    result = await db.execute(query)
    files = result.scalars().all()
    
    return FileListResponse(
        items=files,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.get("/{file_id}", response_model=FileDetailResponse)
async def get_file(
    file_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Obter detalhes de um arquivo
    """
    # Buscar arquivo
    file = await db.execute(
        select(ProjectFile).options(
            selectinload(ProjectFile.uploaded_by_user),
            selectinload(ProjectFile.project),
            selectinload(ProjectFile.task)
        ).where(ProjectFile.id == file_id)
    )
    file = file.scalar_one_or_none()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo não encontrado"
        )
    
    # Verificar permissões
    project_id = file.project_id
    if file.task_id:
        task = await db.execute(
            select(Task).where(Task.id == file.task_id)
        )
        task = task.scalar_one_or_none()
        if task:
            project_id = task.project_id
    
    if project_id:
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
                detail="Usuário não tem acesso ao arquivo"
            )
    
    return file


@router.put("/{file_id}", response_model=FileDetailResponse)
async def update_file(
    file_id: int,
    file_data: FileUpdateRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Atualizar metadados de um arquivo
    """
    # Buscar arquivo
    file = await db.execute(
        select(ProjectFile).where(ProjectFile.id == file_id)
    )
    file = file.scalar_one_or_none()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo não encontrado"
        )
    
    # Verificar permissões (apenas quem fez upload ou admin do projeto)
    project_id = file.project_id
    if file.task_id:
        task = await db.execute(
            select(Task).where(Task.id == file.task_id)
        )
        task = task.scalar_one_or_none()
        if task:
            project_id = task.project_id
    
    can_edit = file.uploaded_by == current_user.id
    
    if project_id:
        member = await db.execute(
            select(ProjectMember).where(
                and_(
                    ProjectMember.project_id == project_id,
                    ProjectMember.user_id == current_user.id
                )
            )
        )
        member = member.scalar_one_or_none()
        if member and member.role in ["admin", "owner"]:
            can_edit = True
    
    if not can_edit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não tem permissão para editar este arquivo"
        )
    
    # Atualizar campos
    update_data = file_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(file, field, value)
    
    file.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(file)
    
    # Notificar via WebSocket
    if project_id:
        await websocket_manager.broadcast_to_project(
            project_id,
            {
                "type": "file_updated",
                "file_id": file.id,
                "filename": file.filename,
                "project_id": project_id
            }
        )
    
    return file


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Excluir arquivo
    """
    # Buscar arquivo
    file = await db.execute(
        select(ProjectFile).where(ProjectFile.id == file_id)
    )
    file = file.scalar_one_or_none()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo não encontrado"
        )
    
    # Verificar permissões (apenas quem fez upload ou admin do projeto)
    project_id = file.project_id
    if file.task_id:
        task = await db.execute(
            select(Task).where(Task.id == file.task_id)
        )
        task = task.scalar_one_or_none()
        if task:
            project_id = task.project_id
    
    can_delete = file.uploaded_by == current_user.id
    
    if project_id:
        member = await db.execute(
            select(ProjectMember).where(
                and_(
                    ProjectMember.project_id == project_id,
                    ProjectMember.user_id == current_user.id
                )
            )
        )
        member = member.scalar_one_or_none()
        if member and member.role in ["admin", "owner"]:
            can_delete = True
    
    if not can_delete:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não tem permissão para excluir este arquivo"
        )
    
    # Remover arquivo físico
    try:
        if os.path.exists(file.file_path):
            os.remove(file.file_path)
    except Exception as e:
        # Log do erro, mas continuar com a exclusão do registro
        print(f"Erro ao remover arquivo físico: {str(e)}")
    
    # Remover registro do banco
    await db.delete(file)
    await db.commit()
    
    # Notificar via WebSocket
    if project_id:
        await websocket_manager.broadcast_to_project(
            project_id,
            {
                "type": "file_deleted",
                "file_id": file_id,
                "project_id": project_id
            }
        )


@router.get("/{file_id}/download")
async def download_file(
    file_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Download de arquivo
    """
    # Buscar arquivo
    file = await db.execute(
        select(ProjectFile).where(ProjectFile.id == file_id)
    )
    file = file.scalar_one_or_none()
    
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo não encontrado"
        )
    
    # Verificar permissões
    project_id = file.project_id
    if file.task_id:
        task = await db.execute(
            select(Task).where(Task.id == file.task_id)
        )
        task = task.scalar_one_or_none()
        if task:
            project_id = task.project_id
    
    if project_id:
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
                detail="Usuário não tem acesso ao arquivo"
            )
    
    # Verificar se arquivo existe fisicamente
    if not os.path.exists(file.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Arquivo não encontrado no servidor"
        )
    
    # Retornar arquivo para download
    from fastapi.responses import FileResponse
    
    return FileResponse(
        path=file.file_path,
        filename=file.filename,
        media_type=file.mime_type
    )
