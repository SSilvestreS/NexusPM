"""
Endpoints para gerenciamento de notificações
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
from app.models.notification import (
    Notification, NotificationPreference, NotificationTypePreference,
    NotificationTemplate
)
from app.schemas.notification import (
    NotificationCreate, NotificationUpdate, NotificationResponse,
    NotificationDetailResponse, NotificationListResponse, NotificationSearchQuery,
    NotificationPreferenceCreate, NotificationPreferenceUpdate,
    NotificationPreferenceResponse, NotificationTypePreferenceCreate,
    NotificationTypePreferenceUpdate, NotificationTypePreferenceResponse
)
from app.core.websocket import websocket_manager

router = APIRouter()


@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_data: NotificationCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Criar nova notificação
    """
    # Verificar se o destinatário existe
    recipient = await db.execute(
        select(User).where(User.id == notification_data.recipient_id)
    )
    if not recipient.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destinatário não encontrado"
        )
    
    # Verificar se o usuário atual pode criar notificações para o destinatário
    # Apenas o próprio usuário ou admin pode criar notificações
    if notification_data.recipient_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não tem permissão para criar notificações para outros"
        )
    
    # Criar notificação
    db_notification = Notification(
        recipient_id=notification_data.recipient_id,
        sender_id=notification_data.sender_id or current_user.id,
        type=notification_data.type,
        title=notification_data.title,
        message=notification_data.message,
        priority=notification_data.priority,
        channels=notification_data.channels,
        project_id=notification_data.project_id,
        task_id=notification_data.task_id,
        comment_id=notification_data.comment_id,
        metadata=notification_data.metadata,
        status="unread"
    )
    
    db.add(db_notification)
    await db.commit()
    await db.refresh(db_notification)
    
    # Notificar via WebSocket
    await websocket_manager.send_to_user(
        notification_data.recipient_id,
        {
            "type": "notification_created",
            "notification_id": db_notification.id,
            "notification_type": db_notification.type,
            "title": db_notification.title
        }
    )
    
    return db_notification


@router.get("/", response_model=NotificationListResponse)
async def get_notifications(
    type: Optional[str] = Query(None, description="Tipo de notificação"),
    status: Optional[str] = Query(None, description="Status da notificação"),
    priority: Optional[str] = Query(None, description="Prioridade da notificação"),
    unread_only: bool = Query(False, description="Apenas não lidas"),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(20, ge=1, le=100, description="Tamanho da página"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Listar notificações do usuário atual
    """
    # Construir query base
    query = select(Notification).options(
        selectinload(Notification.sender),
        selectinload(Notification.project),
        selectinload(Notification.task),
        selectinload(Notification.comment)
    ).where(Notification.recipient_id == current_user.id)
    
    # Aplicar filtros
    filters = []
    
    if type:
        filters.append(Notification.type == type)
    
    if status:
        filters.append(Notification.status == status)
    
    if priority:
        filters.append(Notification.priority == priority)
    
    if unread_only:
        filters.append(Notification.status == "unread")
    
    # Aplicar filtros
    if filters:
        query = query.where(and_(*filters))
    
    # Contar total
    count_query = select(Notification).where(
        and_(
            Notification.recipient_id == current_user.id,
            *filters
        ) if filters else Notification.recipient_id == current_user.id
    )
    total = await db.scalar(select(func.count()).select_from(count_query.subquery()))
    
    # Aplicar paginação e ordenação
    query = query.order_by(Notification.created_at.desc()).offset((page - 1) * size).limit(size)
    
    # Executar query
    result = await db.execute(query)
    notifications = result.scalars().all()
    
    return NotificationListResponse(
        items=notifications,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.get("/{notification_id}", response_model=NotificationDetailResponse)
async def get_notification(
    notification_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Obter detalhes de uma notificação
    """
    # Buscar notificação
    notification = await db.execute(
        select(Notification).options(
            selectinload(Notification.sender),
            selectinload(Notification.project),
            selectinload(Notification.task),
            selectinload(Notification.comment),
            selectinload(Notification.related_notifications)
        ).where(
            and_(
                Notification.id == notification_id,
                Notification.recipient_id == current_user.id
            )
        )
    )
    notification = notification.scalar_one_or_none()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificação não encontrada"
        )
    
    return notification


@router.put("/{notification_id}", response_model=NotificationResponse)
async def update_notification(
    notification_id: int,
    notification_data: NotificationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Atualizar notificação
    """
    # Buscar notificação
    notification = await db.execute(
        select(Notification).where(
            and_(
                Notification.id == notification_id,
                Notification.recipient_id == current_user.id
            )
        )
    )
    notification = notification.scalar_one_or_none()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificação não encontrada"
        )
    
    # Atualizar campos
    update_data = notification_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(notification, field, value)
    
    notification.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(notification)
    
    return notification


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Excluir notificação
    """
    # Buscar notificação
    notification = await db.execute(
        select(Notification).where(
            and_(
                Notification.id == notification_id,
                Notification.recipient_id == current_user.id
            )
        )
    )
    notification = notification.scalar_one_or_none()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificação não encontrada"
        )
    
    # Remover notificação
    await db.delete(notification)
    await db.commit()


@router.post("/{notification_id}/mark-read", response_model=NotificationResponse)
async def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Marcar notificação como lida
    """
    # Buscar notificação
    notification = await db.execute(
        select(Notification).where(
            and_(
                Notification.id == notification_id,
                Notification.recipient_id == current_user.id
            )
        )
    )
    notification = notification.scalar_one_or_none()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notificação não encontrada"
        )
    
    # Marcar como lida
    notification.status = "read"
    notification.read_at = datetime.utcnow()
    notification.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(notification)
    
    return notification


@router.post("/mark-all-read", response_model=dict)
async def mark_all_notifications_read(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Marcar todas as notificações como lidas
    """
    # Buscar todas as notificações não lidas
    unread_notifications = await db.execute(
        select(Notification).where(
            and_(
                Notification.recipient_id == current_user.id,
                Notification.status == "unread"
            )
        )
    )
    unread_notifications = unread_notifications.scalars().all()
    
    # Marcar todas como lidas
    now = datetime.utcnow()
    for notification in unread_notifications:
        notification.status = "read"
        notification.read_at = now
        notification.updated_at = now
    
    await db.commit()
    
    return {
        "message": f"{len(unread_notifications)} notificações marcadas como lidas",
        "count": len(unread_notifications)
    }


@router.get("/preferences", response_model=NotificationPreferenceResponse)
async def get_notification_preferences(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Obter preferências de notificação do usuário
    """
    # Buscar preferências
    preferences = await db.execute(
        select(NotificationPreference).where(
            NotificationPreference.user_id == current_user.id
        )
    )
    preferences = preferences.scalar_one_or_none()
    
    if not preferences:
        # Criar preferências padrão
        preferences = NotificationPreference(
            user_id=current_user.id,
            email_enabled=True,
            push_enabled=True,
            in_app_enabled=True,
            digest_frequency="daily",
            quiet_hours_start="22:00",
            quiet_hours_end="08:00"
        )
        db.add(preferences)
        await db.commit()
        await db.refresh(preferences)
    
    return preferences


@router.put("/preferences", response_model=NotificationPreferenceResponse)
async def update_notification_preferences(
    preferences_data: NotificationPreferenceUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Atualizar preferências de notificação
    """
    # Buscar preferências existentes
    preferences = await db.execute(
        select(NotificationPreference).where(
            NotificationPreference.user_id == current_user.id
        )
    )
    preferences = preferences.scalar_one_or_none()
    
    if not preferences:
        # Criar novas preferências
        preferences = NotificationPreference(
            user_id=current_user.id,
            **preferences_data.dict()
        )
        db.add(preferences)
    else:
        # Atualizar preferências existentes
        update_data = preferences_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(preferences, field, value)
        preferences.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(preferences)
    
    return preferences


@router.get("/type-preferences", response_model=List[NotificationTypePreferenceResponse])
async def get_notification_type_preferences(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Obter preferências por tipo de notificação
    """
    # Buscar preferências por tipo
    type_preferences = await db.execute(
        select(NotificationTypePreference).where(
            NotificationTypePreference.user_id == current_user.id
        )
    )
    type_preferences = type_preferences.scalars().all()
    
    return type_preferences


@router.put("/type-preferences/{notification_type}", response_model=NotificationTypePreferenceResponse)
async def update_notification_type_preference(
    notification_type: str,
    type_preference_data: NotificationTypePreferenceUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Atualizar preferência para um tipo específico de notificação
    """
    # Buscar preferência existente
    type_preference = await db.execute(
        select(NotificationTypePreference).where(
            and_(
                NotificationTypePreference.user_id == current_user.id,
                NotificationTypePreference.notification_type == notification_type
            )
        )
    )
    type_preference = type_preference.scalar_one_or_none()
    
    if not type_preference:
        # Criar nova preferência
        type_preference = NotificationTypePreference(
            user_id=current_user.id,
            notification_type=notification_type,
            **type_preference_data.dict()
        )
        db.add(type_preference)
    else:
        # Atualizar preferência existente
        update_data = type_preference_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(type_preference, field, value)
        type_preference.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(type_preference)
    
    return type_preference


@router.get("/unread-count", response_model=dict)
async def get_unread_notification_count(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Obter contagem de notificações não lidas
    """
    # Contar notificações não lidas
    count = await db.scalar(
        select(func.count(Notification.id)).where(
            and_(
                Notification.recipient_id == current_user.id,
                Notification.status == "unread"
            )
        )
    )
    
    return {
        "unread_count": count or 0,
        "user_id": current_user.id
    }


@router.post("/bulk-action", response_model=dict)
async def bulk_notification_action(
    notification_ids: List[int],
    action: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Ação em massa para notificações
    """
    if not notification_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lista de IDs não pode estar vazia"
        )
    
    # Buscar notificações
    notifications = await db.execute(
        select(Notification).where(
            and_(
                Notification.id.in_(notification_ids),
                Notification.recipient_id == current_user.id
            )
        )
    )
    notifications = notifications.scalars().all()
    
    if len(notifications) != len(notification_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Algumas notificações não foram encontradas"
        )
    
    # Aplicar ação
    now = datetime.utcnow()
    updated_count = 0
    
    if action == "mark_read":
        for notification in notifications:
            if notification.status == "unread":
                notification.status = "read"
                notification.read_at = now
                notification.updated_at = now
                updated_count += 1
    
    elif action == "mark_unread":
        for notification in notifications:
            if notification.status == "read":
                notification.status = "unread"
                notification.read_at = None
                notification.updated_at = now
                updated_count += 1
    
    elif action == "delete":
        for notification in notifications:
            await db.delete(notification)
        updated_count = len(notifications)
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ação inválida. Use: mark_read, mark_unread, ou delete"
        )
    
    await db.commit()
    
    return {
        "message": f"Ação '{action}' aplicada a {updated_count} notificações",
        "action": action,
        "updated_count": updated_count
    }
