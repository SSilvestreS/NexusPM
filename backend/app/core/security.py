"""
Utilitários de segurança para autenticação e autorização
"""
from datetime import datetime, timedelta
from typing import Optional, Union, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import secrets
import string

from app.core.config import settings
from app.core.database import get_async_db
from app.models.user import User

# Configuração para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração para OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(
    subject: Union[str, Any], 
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Cria um token de acesso JWT
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm=settings.algorithm
    )
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any], 
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Cria um token de refresh JWT
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.refresh_token_expire_days
        )
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm=settings.algorithm
    )
    return encoded_jwt


def create_password_reset_token(
    subject: Union[str, Any], 
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Cria um token para reset de senha
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "password_reset"}
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm=settings.algorithm
    )
    return encoded_jwt


def create_email_verification_token(
    subject: Union[str, Any], 
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Cria um token para verificação de email
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=72)
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "email_verification"}
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm=settings.algorithm
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verifica um token JWT e retorna o payload
    """
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        return None


def verify_password_reset_token(token: str) -> Optional[str]:
    """
    Verifica um token de reset de senha
    """
    payload = verify_token(token)
    if payload and payload.get("type") == "password_reset":
        return payload.get("sub")
    return None


def verify_email_verification_token(token: str) -> Optional[str]:
    """
    Verifica um token de verificação de email
    """
    payload = verify_token(token)
    if payload and payload.get("type") == "email_verification":
        return payload.get("sub")
    return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde ao hash
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Gera o hash de uma senha
    """
    return pwd_context.hash(password)


def extract_user_id_from_token(token: str) -> Optional[int]:
    """
    Extrai o ID do usuário de um token JWT
    """
    payload = verify_token(token)
    if payload:
        try:
            return int(payload.get("sub"))
        except (ValueError, TypeError):
            return None
    return None


def check_token_expiration(token: str) -> bool:
    """
    Verifica se um token ainda é válido
    """
    payload = verify_token(token)
    if payload:
        exp = payload.get("exp")
        if exp:
            return datetime.utcnow().timestamp() < exp
    return False


def generate_secure_random_string(length: int = 32) -> str:
    """
    Gera uma string aleatória segura
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_db)
) -> User:
    """
    Obtém o usuário atual baseado no token JWT
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Buscar usuário no banco
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Obtém o usuário atual ativo
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuário inativo"
        )
    return current_user


async def get_current_verified_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Obtém o usuário atual verificado
    """
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Usuário não verificado"
        )
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Obtém o usuário atual com papel de administrador
    """
    if current_user.role not in ["admin", "superuser"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Permissão insuficiente"
        )
    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Obtém o usuário atual com papel de super usuário
    """
    if current_user.role != "superuser":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Permissão insuficiente"
        )
    return current_user


def check_user_permission(
    user: User, 
    required_role: str, 
    resource_owner_id: Optional[int] = None
) -> bool:
    """
    Verifica se o usuário tem permissão para acessar um recurso
    """
    # Super usuários têm acesso total
    if user.role == "superuser":
        return True
    
    # Administradores têm acesso total
    if user.role == "admin":
        return True
    
    # Verificar se é o proprietário do recurso
    if resource_owner_id and user.id == resource_owner_id:
        return True
    
    # Verificar papel específico
    if user.role == required_role:
        return True
    
    return False


def require_user_permission(
    user: User, 
    required_role: str, 
    resource_owner_id: Optional[int] = None
) -> None:
    """
    Exige que o usuário tenha permissão para acessar um recurso
    """
    if not check_user_permission(user, required_role, resource_owner_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Permissão insuficiente"
        )
