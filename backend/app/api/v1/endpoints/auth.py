"""
Endpoints de autenticação e autorização
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import Optional
import structlog

from app.core.database import get_async_db
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_token,
    get_password_hash,
    verify_password
)
from app.models.user import User, UserSession
from app.schemas.auth import (
    TokenResponse,
    UserLogin,
    UserRegister,
    PasswordReset,
    PasswordResetConfirm,
    OAuthLogin
)

logger = structlog.get_logger()

# Cria o roteador de autenticação
router = APIRouter()

# Configuração do OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Registra um novo usuário no sistema
    
    Args:
        user_data: Dados do usuário para registro
        db: Sessão do banco de dados
        
    Returns:
        Dicionário com mensagem de sucesso e ID do usuário
    """
    try:
        # Verifica se o email já existe
        existing_user = await db.get(User, email=user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já está em uso"
            )
        
        # Verifica se o username já existe
        existing_username = await db.get(User, username=user_data.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nome de usuário já está em uso"
            )
        
        # Cria o novo usuário
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        logger.info("Novo usuário registrado", user_id=str(new_user.id), email=user_data.email)
        
        return {
            "message": "Usuário registrado com sucesso",
            "user_id": str(new_user.id),
            "email": new_user.email,
            "username": new_user.username
        }
        
    except Exception as e:
        await db.rollback()
        logger.error("Erro ao registrar usuário", error=str(e), email=user_data.email)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/login", response_model=TokenResponse)
async def login_user(
    user_data: UserLogin,
    request: Request,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Autentica um usuário e retorna tokens de acesso
    
    Args:
        user_data: Credenciais do usuário
        request: Objeto da requisição para obter IP e User-Agent
        db: Sessão do banco de dados
        
    Returns:
        Tokens de acesso e refresh
    """
    try:
        # Busca o usuário pelo email ou username
        user = await db.get(User, email=user_data.email_or_username)
        if not user:
            user = await db.get(User, username=user_data.email_or_username)
        
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Conta desativada"
            )
        
        # Cria tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        # Cria sessão do usuário
        user_session = UserSession(
            user_id=user.id,
            token_id=access_token,
            refresh_token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )
        
        db.add(user_session)
        
        # Atualiza último login
        user.update_last_login()
        
        await db.commit()
        
        logger.info("Usuário logado com sucesso", user_id=str(user.id), email=user.email)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error("Erro ao fazer login", error=str(e), email_or_username=user_data.email_or_username)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Renova o token de acesso usando o refresh token
    
    Args:
        refresh_token: Token de refresh
        db: Sessão do banco de dados
        
    Returns:
        Novos tokens de acesso e refresh
    """
    try:
        # Verifica o refresh token
        payload = verify_token(refresh_token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        # Busca a sessão do usuário
        session = await db.get(UserSession, refresh_token=refresh_token)
        if not session or not session.is_active or session.is_expired():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Sessão expirada ou inválida"
            )
        
        # Busca o usuário
        user = await db.get(User, user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado ou inativo"
            )
        
        # Cria novos tokens
        new_access_token = create_access_token(data={"sub": str(user.id)})
        new_refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        # Atualiza a sessão
        session.token_id = new_access_token
        session.refresh_token = new_refresh_token
        session.expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        await db.commit()
        
        logger.info("Token renovado com sucesso", user_id=str(user.id))
        
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error("Erro ao renovar token", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Faz logout do usuário invalidando a sessão
    
    Args:
        token: Token de acesso
        db: Sessão do banco de dados
        
    Returns:
        Mensagem de sucesso
    """
    try:
        # Verifica o token
        payload = verify_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        # Busca e invalida a sessão
        session = await db.get(UserSession, token_id=token)
        if session:
            session.is_active = False
            await db.commit()
        
        logger.info("Usuário fez logout", user_id=user_id)
        
        return {"message": "Logout realizado com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error("Erro ao fazer logout", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/password-reset", status_code=status.HTTP_200_OK)
async def request_password_reset(
    email: str,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Solicita reset de senha enviando email
    
    Args:
        email: Email do usuário
        db: Sessão do banco de dados
        
    Returns:
        Mensagem de sucesso
    """
    try:
        # Busca o usuário
        user = await db.get(User, email=email)
        if not user or not user.is_active:
            # Por segurança, não revela se o email existe ou não
            return {"message": "Se o email existir, você receberá instruções de reset"}
        
        # TODO: Implementar envio de email com token de reset
        # Por enquanto, apenas retorna sucesso
        
        logger.info("Solicitação de reset de senha", user_id=str(user.id), email=email)
        
        return {"message": "Se o email existir, você receberá instruções de reset"}
        
    except Exception as e:
        logger.error("Erro ao solicitar reset de senha", error=str(e), email=email)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.post("/password-reset-confirm", status_code=status.HTTP_200_OK)
async def confirm_password_reset(
    reset_data: PasswordResetConfirm,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Confirma reset de senha com token
    
    Args:
        reset_data: Dados do reset incluindo token e nova senha
        db: Sessão do banco de dados
        
    Returns:
        Mensagem de sucesso
    """
    try:
        # TODO: Implementar verificação do token de reset
        # Por enquanto, apenas retorna sucesso
        
        logger.info("Reset de senha confirmado", email=reset_data.email)
        
        return {"message": "Senha alterada com sucesso"}
        
    except Exception as e:
        logger.error("Erro ao confirmar reset de senha", error=str(e), email=reset_data.email)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/me", response_model=dict)
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Retorna informações do usuário atual
    
    Args:
        token: Token de acesso
        db: Sessão do banco de dados
        
    Returns:
        Dados do usuário atual
    """
    try:
        # Verifica o token
        payload = verify_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        # Busca o usuário
        user = await db.get(User, user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado ou inativo"
            )
        
        return user.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Erro ao buscar usuário atual", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )
