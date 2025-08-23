"""
Módulo de segurança para autenticação e autorização
"""

from datetime import datetime, timedelta
from typing import Optional, Union, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
import structlog

from app.core.config import settings

logger = structlog.get_logger()

# Configuração do contexto de criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Cria um token de acesso JWT
    
    Args:
        data: Dados a serem incluídos no token
        expires_delta: Tempo de expiração personalizado
        
    Returns:
        Token JWT codificado
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    
    try:
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.error("Erro ao criar token de acesso", error=str(e))
        raise

def create_refresh_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Cria um token de refresh JWT
    
    Args:
        data: Dados a serem incluídos no token
        expires_delta: Tempo de expiração personalizado
        
    Returns:
        Token JWT de refresh codificado
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire, "type": "refresh"})
    
    try:
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.error("Erro ao criar token de refresh", error=str(e))
        raise

def verify_token(token: str) -> dict:
    """
    Verifica e decodifica um token JWT
    
    Args:
        token: Token JWT a ser verificado
        
    Returns:
        Payload decodificado do token
        
    Raises:
        JWTError: Se o token for inválido ou expirado
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        # Verifica se o token expirou
        if datetime.fromtimestamp(payload["exp"]) < datetime.utcnow():
            raise JWTError("Token expirado")
        
        return payload
        
    except JWTError as e:
        logger.warning("Token JWT inválido", error=str(e))
        raise
    except Exception as e:
        logger.error("Erro ao verificar token", error=str(e))
        raise JWTError("Erro ao verificar token")

def get_password_hash(password: str) -> str:
    """
    Gera hash de uma senha
    
    Args:
        password: Senha em texto plano
        
    Returns:
        Hash da senha
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha corresponde ao hash
    
    Args:
        plain_password: Senha em texto plano
        hashed_password: Hash da senha
        
    Returns:
        True se a senha corresponder, False caso contrário
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user_id(token: str) -> Optional[str]:
    """
    Extrai o ID do usuário de um token JWT
    
    Args:
        token: Token JWT
        
    Returns:
        ID do usuário ou None se inválido
    """
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        return user_id
    except JWTError:
        return None

def is_token_expired(token: str) -> bool:
    """
    Verifica se um token JWT expirou
    
    Args:
        token: Token JWT
        
    Returns:
        True se expirado, False caso contrário
    """
    try:
        payload = verify_token(token)
        return False
    except JWTError:
        return True

def get_token_expiration(token: str) -> Optional[datetime]:
    """
    Obtém a data de expiração de um token JWT
    
    Args:
        token: Token JWT
        
    Returns:
        Data de expiração ou None se inválido
    """
    try:
        payload = verify_token(token)
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            return datetime.fromtimestamp(exp_timestamp)
        return None
    except JWTError:
        return None

def create_password_reset_token(email: str) -> str:
    """
    Cria um token para reset de senha
    
    Args:
        email: Email do usuário
        
    Returns:
        Token JWT para reset de senha
    """
    data = {
        "sub": email,
        "type": "password_reset",
        "exp": datetime.utcnow() + timedelta(hours=1)  # Expira em 1 hora
    }
    
    try:
        encoded_jwt = jwt.encode(
            data,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.error("Erro ao criar token de reset de senha", error=str(e))
        raise

def verify_password_reset_token(token: str) -> Optional[str]:
    """
    Verifica um token de reset de senha
    
    Args:
        token: Token JWT de reset de senha
        
    Returns:
        Email do usuário ou None se inválido
    """
    try:
        payload = verify_token(token)
        
        # Verifica se é um token de reset de senha
        if payload.get("type") != "password_reset":
            return None
        
        return payload.get("sub")
        
    except JWTError:
        return None

def create_email_verification_token(email: str) -> str:
    """
    Cria um token para verificação de email
    
    Args:
        email: Email do usuário
        
    Returns:
        Token JWT para verificação de email
    """
    data = {
        "sub": email,
        "type": "email_verification",
        "exp": datetime.utcnow() + timedelta(days=7)  # Expira em 7 dias
    }
    
    try:
        encoded_jwt = jwt.encode(
            data,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.error("Erro ao criar token de verificação de email", error=str(e))
        raise

def verify_email_verification_token(token: str) -> Optional[str]:
    """
    Verifica um token de verificação de email
    
    Args:
        token: Token JWT de verificação de email
        
    Returns:
        Email do usuário ou None se inválido
    """
    try:
        payload = verify_token(token)
        
        # Verifica se é um token de verificação de email
        if payload.get("type") != "email_verification":
            return None
        
        return payload.get("sub")
        
    except JWTError:
        return None

def generate_secure_random_string(length: int = 32) -> str:
    """
    Gera uma string aleatória segura
    
    Args:
        length: Comprimento da string
        
    Returns:
        String aleatória segura
    """
    import secrets
    import string
    
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def hash_sensitive_data(data: str) -> str:
    """
    Aplica hash em dados sensíveis
    
    Args:
        data: Dados sensíveis
        
    Returns:
        Hash dos dados
    """
    return pwd_context.hash(data)

def verify_sensitive_data(plain_data: str, hashed_data: str) -> bool:
    """
    Verifica dados sensíveis
    
    Args:
        plain_data: Dados em texto plano
        hashed_data: Hash dos dados
        
    Returns:
        True se corresponder, False caso contrário
    """
    return pwd_context.verify(plain_data, hashed_data)
