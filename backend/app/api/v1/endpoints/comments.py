"""
Endpoints para gerenciamento de comentários
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
from app.models.task import Task
from app.models.comment import Comment, CommentReaction, CommentEdit
from app.schemas.comment import (
    CommentCreate, CommentUpdate, CommentResponse, CommentDetailResponse,
    CommentListResponse, CommentSearchQuery, CommentReactionCreate,
    CommentReactionResponse, CommentEditResponse, CommentThreadResponse
)
from app.core.websocket import websocket_manager

router = APIRouter()


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Criar novo comentário
    """
    # Verificar se pelo menos uma entidade foi especificada
    if not comment_data.project_id and not comment_data.task_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Deve especificar project_id ou task_id"
        )
    
    # Verificar se o usuário tem acesso ao projeto
    project_id = comment_data.project_id
    if comment_data.task_id:
        # Se for comentário de tarefa, buscar o projeto da tarefa
        task = await db.execute(
            select(Task).where(Task.id == comment_data.task_id)
        )
        task = task.scalar_one_or_none()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarefa não encontrada"
            )
        project_id = task.project_id
    
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
    
    # Verificar se o comentário pai existe (se especificado)
    if comment_data.parent_comment_id:
        parent_comment = await db.execute(
            select(Comment).where(Comment.id == comment_data.parent_comment_id)
        )
        parent_comment = parent_comment.scalar_one_or_none()
        
        if not parent_comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comentário pai não encontrado"
            )
        
        # Verificar se o comentário pai pertence à mesma entidade
        if (comment_data.project_id and parent_comment.project_id != comment_data.project_id) or \
           (comment_data.task_id and parent_comment.task_id != comment_data.task_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Comentário pai deve pertencer à mesma entidade"
            )
    
    # Criar comentário
    db_comment = Comment(
        content=comment_data.content,
        project_id=comment_data.project_id,
        task_id=comment_data.task_id,
        parent_comment_id=comment_data.parent_comment_id,
        author_id=current_user.id,
        status="active"
    )
    
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    
    # Notificar via WebSocket
    await websocket_manager.broadcast_to_project(
        project_id,
        {
            "type": "comment_created",
            "comment_id": db_comment.id,
            "author_id": current_user.id,
            "project_id": project_id,
            "task_id": comment_data.task_id
        }
    )
    
    return db_comment


@router.get("/", response_model=CommentListResponse)
async def get_comments(
    project_id: Optional[int] = Query(None, description="ID do projeto"),
    task_id: Optional[int] = Query(None, description="ID da tarefa"),
    author_id: Optional[int] = Query(None, description="ID do autor"),
    parent_comment_id: Optional[int] = Query(None, description="ID do comentário pai"),
    search: Optional[str] = Query(None, description="Termo de busca"),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(20, ge=1, le=100, description="Tamanho da página"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Listar comentários com filtros e paginação
    """
    # Construir query base
    query = select(Comment).options(
        selectinload(Comment.author),
        selectinload(Comment.project),
        selectinload(Comment.task),
        selectinload(Comment.parent_comment)
    )
    
    # Aplicar filtros
    filters = [Comment.status == "active"]
    
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
        filters.append(Comment.project_id == project_id)
    
    if task_id:
        # Verificar se o usuário tem acesso à tarefa (através do projeto)
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
        filters.append(Comment.task_id == task_id)
    
    if author_id:
        filters.append(Comment.author_id == author_id)
    
    if parent_comment_id:
        filters.append(Comment.parent_comment_id == parent_comment_id)
    
    if search:
        search_filter = Comment.content.ilike(f"%{search}%")
        filters.append(search_filter)
    
    # Aplicar filtros
    query = query.where(and_(*filters))
    
    # Contar total
    count_query = select(Comment).where(and_(*filters))
    total = await db.scalar(select(func.count()).select_from(count_query.subquery()))
    
    # Aplicar paginação
    query = query.offset((page - 1) * size).limit(size)
    
    # Executar query
    result = await db.execute(query)
    comments = result.scalars().all()
    
    return CommentListResponse(
        items=comments,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.get("/{comment_id}", response_model=CommentDetailResponse)
async def get_comment(
    comment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Obter detalhes de um comentário
    """
    # Buscar comentário com relacionamentos
    comment = await db.execute(
        select(Comment).options(
            selectinload(Comment.author),
            selectinload(Comment.project),
            selectinload(Comment.task),
            selectinload(Comment.parent_comment),
            selectinload(Comment.replies),
            selectinload(Comment.reactions),
            selectinload(Comment.edit_history)
        ).where(Comment.id == comment_id)
    )
    comment = comment.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comentário não encontrado"
        )
    
    # Verificar se o usuário tem acesso
    project_id = comment.project_id
    if comment.task_id:
        task = await db.execute(
            select(Task).where(Task.id == comment.task_id)
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
                detail="Usuário não tem acesso ao comentário"
            )
    
    return comment


@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Atualizar comentário
    """
    # Buscar comentário
    comment = await db.execute(
        select(Comment).where(Comment.id == comment_id)
    )
    comment = comment.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comentário não encontrado"
        )
    
    # Apenas o autor pode editar
    if comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas o autor pode editar o comentário"
        )
    
    # Verificar se o comentário ainda pode ser editado (não muito antigo)
    time_diff = datetime.utcnow() - comment.created_at
    if time_diff.total_seconds() > 3600:  # 1 hora
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Comentário não pode mais ser editado após 1 hora"
        )
    
    # Salvar versão anterior
    comment_edit = CommentEdit(
        comment_id=comment.id,
        content=comment.content,
        edited_by=current_user.id
    )
    db.add(comment_edit)
    
    # Atualizar comentário
    comment.content = comment_data.content
    comment.updated_at = datetime.utcnow()
    comment.is_edited = True
    
    await db.commit()
    await db.refresh(comment)
    
    # Notificar via WebSocket
    project_id = comment.project_id
    if comment.task_id:
        task = await db.execute(
            select(Task).where(Task.id == comment.task_id)
        )
        task = task.scalar_one_or_none()
        if task:
            project_id = task.project_id
    
    if project_id:
        await websocket_manager.broadcast_to_project(
            project_id,
            {
                "type": "comment_updated",
                "comment_id": comment.id,
                "project_id": project_id,
                "task_id": comment.task_id
            }
        )
    
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Excluir comentário (soft delete)
    """
    # Buscar comentário
    comment = await db.execute(
        select(Comment).where(Comment.id == comment_id)
    )
    comment = comment.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comentário não encontrado"
        )
    
    # Apenas o autor ou admin do projeto pode excluir
    project_id = comment.project_id
    if comment.task_id:
        task = await db.execute(
            select(Task).where(Task.id == comment.task_id)
        )
        task = task.scalar_one_or_none()
        if task:
            project_id = task.project_id
    
    can_delete = comment.author_id == current_user.id
    
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
            detail="Usuário não tem permissão para excluir este comentário"
        )
    
    # Soft delete
    comment.status = "deleted"
    comment.deleted_at = datetime.utcnow()
    comment.deleted_by = current_user.id
    
    await db.commit()
    
    # Notificar via WebSocket
    if project_id:
        await websocket_manager.broadcast_to_project(
            project_id,
            {
                "type": "comment_deleted",
                "comment_id": comment.id,
                "project_id": project_id,
                "task_id": comment.task_id
            }
        )


@router.post("/{comment_id}/reactions", response_model=CommentReactionResponse)
async def add_reaction(
    comment_id: int,
    reaction_data: CommentReactionCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Adicionar reação a um comentário
    """
    # Buscar comentário
    comment = await db.execute(
        select(Comment).where(Comment.id == comment_id)
    )
    comment = comment.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comentário não encontrado"
        )
    
    # Verificar se o usuário tem acesso
    project_id = comment.project_id
    if comment.task_id:
        task = await db.execute(
            select(Task).where(Task.id == comment.task_id)
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
                detail="Usuário não tem acesso ao comentário"
            )
    
    # Verificar se a reação já existe
    existing_reaction = await db.execute(
        select(CommentReaction).where(
            and_(
                CommentReaction.comment_id == comment_id,
                CommentReaction.user_id == current_user.id,
                CommentReaction.reaction_type == reaction_data.reaction_type
            )
        )
    )
    
    if existing_reaction.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reação já existe"
        )
    
    # Criar reação
    reaction = CommentReaction(
        comment_id=comment_id,
        user_id=current_user.id,
        reaction_type=reaction_data.reaction_type
    )
    
    db.add(reaction)
    await db.commit()
    await db.refresh(reaction)
    
    # Notificar via WebSocket
    if project_id:
        await websocket_manager.broadcast_to_project(
            project_id,
            {
                "type": "reaction_added",
                "comment_id": comment_id,
                "reaction_type": reaction_data.reaction_type,
                "user_id": current_user.id,
                "project_id": project_id
            }
        )
    
    return reaction


@router.delete("/{comment_id}/reactions/{reaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_reaction(
    comment_id: int,
    reaction_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Remover reação de um comentário
    """
    # Buscar reação
    reaction = await db.execute(
        select(CommentReaction).where(
            and_(
                CommentReaction.id == reaction_id,
                CommentReaction.comment_id == comment_id
            )
        )
    )
    reaction = reaction.scalar_one_or_none()
    
    if not reaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reação não encontrada"
        )
    
    # Apenas o usuário que criou a reação pode removê-la
    if reaction.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas o usuário que criou a reação pode removê-la"
        )
    
    # Remover reação
    await db.delete(reaction)
    await db.commit()
    
    # Notificar via WebSocket
    comment = await db.execute(
        select(Comment).where(Comment.id == comment_id)
    )
    comment = comment.scalar_one_or_none()
    
    if comment:
        project_id = comment.project_id
        if comment.task_id:
            task = await db.execute(
                select(Task).where(Task.id == comment.task_id)
            )
            task = task.scalar_one_or_none()
            if task:
                project_id = task.project_id
        
        if project_id:
            await websocket_manager.broadcast_to_project(
                project_id,
                {
                    "type": "reaction_removed",
                    "comment_id": comment_id,
                    "reaction_type": reaction.reaction_type,
                    "user_id": current_user.id,
                    "project_id": project_id
                }
            )


@router.get("/{comment_id}/thread", response_model=CommentThreadResponse)
async def get_comment_thread(
    comment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Obter thread completa de um comentário
    """
    # Buscar comentário raiz
    root_comment = await db.execute(
        select(Comment).where(Comment.id == comment_id)
    )
    root_comment = root_comment.scalar_one_or_none()
    
    if not root_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comentário não encontrado"
        )
    
    # Encontrar o comentário raiz da thread
    while root_comment.parent_comment_id:
        root_comment = await db.execute(
            select(Comment).where(Comment.id == root_comment.parent_comment_id)
        )
        root_comment = root_comment.scalar_one_or_none()
        if not root_comment:
            break
    
    if not root_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comentário raiz não encontrado"
        )
    
    # Verificar permissões
    project_id = root_comment.project_id
    if root_comment.task_id:
        task = await db.execute(
            select(Task).where(Task.id == root_comment.task_id)
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
                detail="Usuário não tem acesso ao comentário"
            )
    
    # Buscar todos os comentários da thread
    thread_comments = await db.execute(
        select(Comment).options(
            selectinload(Comment.author),
            selectinload(Comment.reactions)
        ).where(
            or_(
                Comment.id == root_comment.id,
                Comment.parent_comment_id == root_comment.id
            )
        ).order_by(Comment.created_at)
    )
    thread_comments = thread_comments.scalars().all()
    
    return CommentThreadResponse(
        root_comment=root_comment,
        replies=thread_comments[1:] if len(thread_comments) > 1 else [],
        total_replies=len(thread_comments) - 1
    )
