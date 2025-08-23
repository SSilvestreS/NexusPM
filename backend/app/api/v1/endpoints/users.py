"""
Endpoints para gerenciamento de usuários
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload, joinedload

from app.core.database import get_async_db
from app.core.security import get_current_user, get_current_active_user, get_current_admin_user
from app.models.user import User, UserSession, UserPreference
from app.schemas.user import (
    UserCreate, UserUpdate, UserProfileUpdate, UserResponse, UserDetailResponse,
    UserListResponse, UserSearchQuery, UserPreferenceUpdate, UserPreferenceResponse,
    UserSessionResponse, ChangePassword
)
from app.core.security import get_password_hash, verify_password
from app.websockets.manager import websocket_manager

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Criar novo usuário
    """
    # Verificar se o email já existe
    existing_user = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já está em uso"
        )
    
    # Verificar se o username já existe
    existing_username = await db.execute(
        select(User).where(User.username == user_data.username)
    )
    if existing_username.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username já está em uso"
        )
    
    # Criar hash da senha
    hashed_password = get_password_hash(user_data.password)
    
    # Criar usuário
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        name=user_data.name,
        bio=user_data.bio,
        location=user_data.location,
        website=user_data.website,
        avatar_url=user_data.avatar_url,
        hashed_password=hashed_password,
        is_active=True,
        is_verified=False,
        role="user"
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user


@router.get("/me", response_model=UserDetailResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Obter perfil do usuário atual
    """
    # Buscar estatísticas do usuário
    projects_count = await db.execute(
        select(func.count()).select_from(User).where(User.id == current_user.id)
    )
    
    # Aqui você pode adicionar mais estatísticas conforme necessário
    
    return UserDetailResponse(
        **current_user.__dict__,
        projects_count=projects_count.scalar() or 0,
        tasks_count=0,  # Implementar quando tiver o modelo de tarefas
        comments_count=0  # Implementar quando tiver o modelo de comentários
    )


@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_data: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Atualizar perfil do usuário atual
    """
    update_data = user_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    current_user.updated_at = func.now()
    
    await db.commit()
    await db.refresh(current_user)
    
    return current_user


@router.put("/me/password", status_code=status.HTTP_200_OK)
async def change_password(
    password_data: ChangePassword,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Alterar senha do usuário atual
    """
    # Verificar senha atual
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha atual incorreta"
        )
    
    # Atualizar senha
    current_user.hashed_password = get_password_hash(password_data.new_password)
    current_user.updated_at = func.now()
    
    await db.commit()
    
    return {"message": "Senha alterada com sucesso"}


@router.get("/me/preferences", response_model=UserPreferenceResponse)
async def get_current_user_preferences(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Obter preferências do usuário atual
    """
    preferences = await db.execute(
        select(UserPreference).where(UserPreference.user_id == current_user.id)
    )
    
    user_prefs = preferences.scalar_one_or_none()
    if not user_prefs:
        # Criar preferências padrão se não existirem
        user_prefs = UserPreference(
            user_id=current_user.id,
            theme="light",
            language="pt-BR",
            timezone="America/Sao_Paulo",
            email_notifications=True,
            push_notifications=True,
            sms_notifications=False,
            weekly_digest=True,
            project_updates=True,
            task_assignments=True,
            comment_mentions=True
        )
        db.add(user_prefs)
        await db.commit()
        await db.refresh(user_prefs)
    
    return user_prefs


@router.put("/me/preferences", response_model=UserPreferenceResponse)
async def update_current_user_preferences(
    preferences_data: UserPreferenceUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Atualizar preferências do usuário atual
    """
    preferences = await db.execute(
        select(UserPreference).where(UserPreference.user_id == current_user.id)
    )
    
    user_prefs = preferences.scalar_one_or_none()
    if not user_prefs:
        # Criar se não existir
        user_prefs = UserPreference(user_id=current_user.id)
        db.add(user_prefs)
        await db.commit()
        await db.refresh(user_prefs)
    
    update_data = preferences_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user_prefs, field, value)
    
    await db.commit()
    await db.refresh(user_prefs)
    
    return user_prefs


@router.get("/me/sessions", response_model=List[UserSessionResponse])
async def get_current_user_sessions(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Obter sessões ativas do usuário atual
    """
    sessions = await db.execute(
        select(UserSession)
        .where(UserSession.user_id == current_user.id, UserSession.is_active == True)
        .order_by(UserSession.last_activity.desc())
    )
    
    return sessions.scalars().all()


@router.delete("/me/sessions/{session_id}", status_code=status.HTTP_200_OK)
async def terminate_session(
    session_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Encerrar uma sessão específica do usuário
    """
    session = await db.execute(
        select(UserSession).where(
            UserSession.id == session_id,
            UserSession.user_id == current_user.id
        )
    )
    
    user_session = session.scalar_one_or_none()
    if not user_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sessão não encontrada"
        )
    
    user_session.is_active = False
    await db.commit()
    
    return {"message": "Sessão encerrada com sucesso"}


@router.delete("/me/sessions", status_code=status.HTTP_200_OK)
async def terminate_all_sessions(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Encerrar todas as sessões do usuário atual (exceto a atual)
    """
    await db.execute(
        UserSession.__table__.update()
        .where(
            and_(
                UserSession.user_id == current_user.id,
                UserSession.is_active == True
            )
        )
        .values(is_active=False)
    )
    
    await db.commit()
    
    return {"message": "Todas as sessões foram encerradas"}


@router.get("/", response_model=UserListResponse)
async def get_users(
    query: Optional[str] = Query(None, description="Termo de busca"),
    status_filter: Optional[str] = Query(None, description="Filtrar por status"),
    role_filter: Optional[str] = Query(None, description="Filtrar por papel"),
    is_verified: Optional[bool] = Query(None, description="Filtrar por verificação"),
    is_active: Optional[bool] = Query(None, description="Filtrar por status ativo"),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(20, ge=1, le=100, description="Tamanho da página"),
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Listar usuários (apenas para administradores)
    """
    # Construir query base
    base_query = select(User)
    
    # Aplicar filtros
    filters = []
    if query:
        filters.append(
            or_(
                User.name.ilike(f"%{query}%"),
                User.username.ilike(f"%{query}%"),
                User.email.ilike(f"%{query}%")
            )
        )
    
    if status_filter:
        filters.append(User.status == status_filter)
    
    if role_filter:
        filters.append(User.role == role_filter)
    
    if is_verified is not None:
        filters.append(User.is_verified == is_verified)
    
    if is_active is not None:
        filters.append(User.is_active == is_active)
    
    if filters:
        base_query = base_query.where(and_(*filters))
    
    # Contar total
    count_query = select(func.count()).select_from(base_query.subquery())
    total = await db.execute(count_query)
    total_count = total.scalar()
    
    # Aplicar paginação
    offset = (page - 1) * size
    users_query = base_query.offset(offset).limit(size)
    
    # Executar query
    result = await db.execute(users_query)
    users = result.scalars().all()
    
    # Calcular páginas
    pages = (total_count + size - 1) // size
    
    return UserListResponse(
        users=users,
        total=total_count,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/{user_id}", response_model=UserDetailResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Obter detalhes de um usuário específico
    """
    # Usuários só podem ver seus próprios detalhes ou usuários públicos
    if current_user.id != user_id and current_user.role not in ["admin", "superuser"]:
        # Verificar se o usuário é público
        user = await db.execute(
            select(User).where(
                and_(
                    User.id == user_id,
                    User.is_active == True,
                    User.is_verified == True
                )
            )
        )
        user_obj = user.scalar_one_or_none()
        if not user_obj:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado"
            )
    else:
        user = await db.execute(
            select(User).where(User.id == user_id)
        )
        user_obj = user.scalar_one_or_none()
    
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Buscar estatísticas
    projects_count = 0  # Implementar quando tiver o modelo de projetos
    tasks_count = 0     # Implementar quando tiver o modelo de tarefas
    comments_count = 0  # Implementar quando tiver o modelo de comentários
    
    return UserDetailResponse(
        **user_obj.__dict__,
        projects_count=projects_count,
        tasks_count=tasks_count,
        comments_count=comments_count
    )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Atualizar usuário (apenas para administradores)
    """
    user = await db.execute(
        select(User).where(User.id == user_id)
    )
    
    user_obj = user.scalar_one_or_none()
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    update_data = user_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user_obj, field, value)
    
    user_obj.updated_at = func.now()
    
    await db.commit()
    await db.refresh(user_obj)
    
    return user_obj


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Deletar usuário (apenas para administradores)
    """
    # Não permitir deletar a si mesmo
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível deletar sua própria conta"
        )
    
    user = await db.execute(
        select(User).where(User.id == user_id)
    )
    
    user_obj = user.scalar_one_or_none()
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Soft delete - marcar como inativo
    user_obj.is_active = False
    user_obj.updated_at = func.now()
    
    await db.commit()
    
    return {"message": "Usuário deletado com sucesso"}


@router.post("/{user_id}/activate", response_model=UserResponse)
async def activate_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Ativar usuário (apenas para administradores)
    """
    user = await db.execute(
        select(User).where(User.id == user_id)
    )
    
    user_obj = user.scalar_one_or_none()
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    user_obj.is_active = True
    user_obj.updated_at = func.now()
    
    await db.commit()
    await db.refresh(user_obj)
    
    return user_obj


@router.post("/{user_id}/deactivate", response_model=UserResponse)
async def deactivate_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Desativar usuário (apenas para administradores)
    """
    # Não permitir desativar a si mesmo
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível desativar sua própria conta"
        )
    
    user = await db.execute(
        select(User).where(User.id == user_id)
    )
    
    user_obj = user.scalar_one_or_none()
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    user_obj.is_active = False
    user_obj.updated_at = func.now()
    
    await db.commit()
    await db.refresh(user_obj)
    
    return user_obj


@router.post("/{user_id}/verify", response_model=UserResponse)
async def verify_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Verificar usuário (apenas para administradores)
    """
    user = await db.execute(
        select(User).where(User.id == user_id)
    )
    
    user_obj = user.scalar_one_or_none()
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    user_obj.is_verified = True
    user_obj.updated_at = func.now()
    
    await db.commit()
    await db.refresh(user_obj)
    
    return user_obj


@router.get("/search/suggestions", response_model=List[str])
async def get_user_suggestions(
    query: str = Query(..., min_length=2, description="Termo de busca"),
    limit: int = Query(10, ge=1, le=50, description="Limite de sugestões"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Obter sugestões de usuários para busca
    """
    users = await db.execute(
        select(User.username, User.name)
        .where(
            and_(
                User.is_active == True,
                or_(
                    User.username.ilike(f"%{query}%"),
                    User.name.ilike(f"%{query}%")
                )
            )
        )
        .limit(limit)
    )
    
    suggestions = []
    for username, name in users.all():
        suggestions.append(f"{username} ({name})")
    
    return suggestions
