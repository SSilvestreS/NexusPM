"""
Schemas Pydantic para autenticação e autorização
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime

class UserRegister(BaseModel):
    """Schema para registro de usuário"""
    
    email: EmailStr = Field(..., description="Email do usuário")
    username: str = Field(..., min_length=3, max_length=50, description="Nome de usuário")
    password: str = Field(..., min_length=8, description="Senha do usuário")
    confirm_password: str = Field(..., description="Confirmação da senha")
    first_name: Optional[str] = Field(None, max_length=100, description="Primeiro nome")
    last_name: Optional[str] = Field(None, max_length=100, description="Sobrenome")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        """Valida se as senhas coincidem"""
        if 'password' in values and v != values['password']:
            raise ValueError('As senhas não coincidem')
        return v
    
    @validator('username')
    def username_valid(cls, v):
        """Valida o formato do username"""
        if not v.isalnum() and '_' not in v and '-' not in v:
            raise ValueError('Username deve conter apenas letras, números, underscore ou hífen')
        return v.lower()
    
    class Config:
        schema_extra = {
            "example": {
                "email": "usuario@exemplo.com",
                "username": "usuario_exemplo",
                "password": "senha123456",
                "confirm_password": "senha123456",
                "first_name": "João",
                "last_name": "Silva"
            }
        }

class UserLogin(BaseModel):
    """Schema para login de usuário"""
    
    email_or_username: str = Field(..., description="Email ou nome de usuário")
    password: str = Field(..., description="Senha do usuário")
    remember_me: Optional[bool] = Field(False, description="Lembrar do usuário")
    
    class Config:
        schema_extra = {
            "example": {
                "email_or_username": "usuario@exemplo.com",
                "password": "senha123456",
                "remember_me": False
            }
        }

class TokenResponse(BaseModel):
    """Schema para resposta de token"""
    
    access_token: str = Field(..., description="Token de acesso JWT")
    refresh_token: str = Field(..., description="Token de refresh JWT")
    token_type: str = Field(..., description="Tipo do token")
    expires_in: int = Field(..., description="Tempo de expiração em segundos")
    user: Dict[str, Any] = Field(..., description="Dados do usuário")
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "usuario@exemplo.com",
                    "username": "usuario_exemplo",
                    "first_name": "João",
                    "last_name": "Silva"
                }
            }
        }

class PasswordReset(BaseModel):
    """Schema para solicitação de reset de senha"""
    
    email: EmailStr = Field(..., description="Email do usuário")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "usuario@exemplo.com"
            }
        }

class PasswordResetConfirm(BaseModel):
    """Schema para confirmação de reset de senha"""
    
    token: str = Field(..., description="Token de reset de senha")
    email: EmailStr = Field(..., description="Email do usuário")
    new_password: str = Field(..., min_length=8, description="Nova senha")
    confirm_password: str = Field(..., description="Confirmação da nova senha")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        """Valida se as senhas coincidem"""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('As senhas não coincidem')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "email": "usuario@exemplo.com",
                "new_password": "nova_senha123",
                "confirm_password": "nova_senha123"
            }
        }

class OAuthLogin(BaseModel):
    """Schema para login OAuth"""
    
    provider: str = Field(..., description="Provedor OAuth (github, gitlab, google)")
    code: str = Field(..., description="Código de autorização OAuth")
    redirect_uri: Optional[str] = Field(None, description="URI de redirecionamento")
    
    @validator('provider')
    def validate_provider(cls, v):
        """Valida o provedor OAuth"""
        allowed_providers = ['github', 'gitlab', 'google']
        if v not in allowed_providers:
            raise ValueError(f'Provedor deve ser um dos seguintes: {", ".join(allowed_providers)}')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "provider": "github",
                "code": "abc123def456",
                "redirect_uri": "http://localhost:3000/auth/callback"
            }
        }

class ChangePassword(BaseModel):
    """Schema para alteração de senha"""
    
    current_password: str = Field(..., description="Senha atual")
    new_password: str = Field(..., min_length=8, description="Nova senha")
    confirm_password: str = Field(..., description="Confirmação da nova senha")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        """Valida se as senhas coincidem"""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('As senhas não coincidem')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "current_password": "senha_atual123",
                "new_password": "nova_senha456",
                "confirm_password": "nova_senha456"
            }
        }

class UserProfileUpdate(BaseModel):
    """Schema para atualização de perfil do usuário"""
    
    first_name: Optional[str] = Field(None, max_length=100, description="Primeiro nome")
    last_name: Optional[str] = Field(None, max_length=100, description="Sobrenome")
    bio: Optional[str] = Field(None, max_length=500, description="Biografia")
    location: Optional[str] = Field(None, max_length=200, description="Localização")
    website: Optional[str] = Field(None, max_length=500, description="Website")
    language: Optional[str] = Field(None, max_length=10, description="Idioma preferido")
    timezone: Optional[str] = Field(None, max_length=50, description="Fuso horário")
    theme: Optional[str] = Field(None, description="Tema preferido")
    
    @validator('theme')
    def validate_theme(cls, v):
        """Valida o tema"""
        if v and v not in ['light', 'dark', 'auto']:
            raise ValueError('Tema deve ser light, dark ou auto')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "first_name": "João",
                "last_name": "Silva",
                "bio": "Desenvolvedor Full Stack apaixonado por tecnologia",
                "location": "São Paulo, Brasil",
                "website": "https://joaosilva.dev",
                "language": "pt-BR",
                "timezone": "America/Sao_Paulo",
                "theme": "dark"
            }
        }

class EmailVerification(BaseModel):
    """Schema para verificação de email"""
    
    token: str = Field(..., description="Token de verificação de email")
    
    class Config:
        schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }

class ResendVerification(BaseModel):
    """Schema para reenvio de verificação de email"""
    
    email: EmailStr = Field(..., description="Email do usuário")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "usuario@exemplo.com"
            }
        }
