"""
Schemas para usuários e perfis
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum


class UserStatus(str, Enum):
    """Status do usuário"""
    ACTIVE = "active"  # Ativo
    INACTIVE = "inactive"  # Inativo
    SUSPENDED = "suspended"  # Suspenso
    PENDING = "pending"  # Pendente


class UserRole(str, Enum):
    """Papel do usuário no sistema"""
    USER = "user"  # Usuário comum
    ADMIN = "admin"  # Administrador
    SUPERUSER = "superuser"  # Super usuário


class Theme(str, Enum):
    """Temas disponíveis"""
    LIGHT = "light"  # Tema claro
    DARK = "dark"  # Tema escuro
    AUTO = "auto"  # Automático


class Language(str, Enum):
    """Idiomas disponíveis"""
    PT_BR = "pt-BR"  # Português Brasil
    EN_US = "en-US"  # Inglês EUA
    ES_ES = "es-ES"  # Espanhol


class UserBase(BaseModel):
    """Schema base para usuário"""
    email: EmailStr = Field(..., description="Email do usuário")
    username: str = Field(..., min_length=3, max_length=50, description="Nome de usuário")
    name: str = Field(..., min_length=2, max_length=100, description="Nome completo")
    bio: Optional[str] = Field(None, max_length=500, description="Biografia do usuário")
    location: Optional[str] = Field(None, max_length=100, description="Localização")
    website: Optional[str] = Field(None, description="Website pessoal")
    avatar_url: Optional[str] = Field(None, description="URL do avatar")


class UserCreate(UserBase):
    """Schema para criação de usuário"""
    password: str = Field(..., min_length=8, description="Senha do usuário")
    confirm_password: str = Field(..., description="Confirmação da senha")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Valida se as senhas coincidem"""
        if 'password' in values and v != values['password']:
            raise ValueError('As senhas não coincidem')
        return v
    
    @validator('username')
    def username_valid(cls, v):
        """Valida formato do username"""
        if not v.isalnum() and '_' not in v and '-' not in v:
            raise ValueError('Username deve conter apenas letras, números, _ ou -')
        return v.lower()


class UserUpdate(BaseModel):
    """Schema para atualização de usuário"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    location: Optional[str] = Field(None, max_length=100)
    website: Optional[str] = Field(None)
    avatar_url: Optional[str] = Field(None)


class UserProfileUpdate(BaseModel):
    """Schema para atualização de perfil"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    location: Optional[str] = Field(None, max_length=100)
    website: Optional[str] = Field(None)
    avatar_url: Optional[str] = Field(None)
    theme: Optional[Theme] = Field(None)
    language: Optional[Language] = Field(None)
    timezone: Optional[str] = Field(None, description="Fuso horário")
    email_notifications: Optional[bool] = Field(None, description="Notificações por email")
    push_notifications: Optional[bool] = Field(None, description="Notificações push")


class UserResponse(UserBase):
    """Schema de resposta para usuário"""
    id: int
    status: UserStatus
    role: UserRole
    is_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    avatar_url: Optional[str]
    
    class Config:
        from_attributes = True


class UserDetailResponse(UserResponse):
    """Schema de resposta detalhada para usuário"""
    projects_count: int = 0
    tasks_count: int = 0
    comments_count: int = 0


class UserPreferenceUpdate(BaseModel):
    """Schema para atualização de preferências"""
    theme: Optional[Theme] = Field(None)
    language: Optional[Language] = Field(None)
    timezone: Optional[str] = Field(None)
    email_notifications: Optional[bool] = Field(None)
    push_notifications: Optional[bool] = Field(None)
    sms_notifications: Optional[bool] = Field(None)
    weekly_digest: Optional[bool] = Field(None, description="Resumo semanal")
    project_updates: Optional[bool] = Field(None, description="Atualizações de projeto")
    task_assignments: Optional[bool] = Field(None, description="Atribuições de tarefas")
    comment_mentions: Optional[bool] = Field(None, description="Mentions em comentários")


class UserPreferenceResponse(BaseModel):
    """Schema de resposta para preferências do usuário"""
    theme: Theme
    language: Language
    timezone: str
    email_notifications: bool
    push_notifications: bool
    sms_notifications: bool
    weekly_digest: bool
    project_updates: bool
    task_assignments: bool
    comment_mentions: bool
    
    class Config:
        from_attributes = True


class UserSessionResponse(BaseModel):
    """Schema de resposta para sessão do usuário"""
    id: int
    user_id: int
    device_info: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    is_active: bool
    created_at: datetime
    last_activity: datetime
    
    class Config:
        from_attributes = True


class ChangePassword(BaseModel):
    """Schema para alteração de senha"""
    current_password: str = Field(..., description="Senha atual")
    new_password: str = Field(..., min_length=8, description="Nova senha")
    confirm_new_password: str = Field(..., description="Confirmação da nova senha")
    
    @validator('confirm_new_password')
    def passwords_match(cls, v, values):
        """Valida se as novas senhas coincidem"""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('As novas senhas não coincidem')
        return v
    
    @validator('new_password')
    def password_strength(cls, v):
        """Valida força da nova senha"""
        if len(v) < 8:
            raise ValueError('A senha deve ter pelo menos 8 caracteres')
        if not any(c.isupper() for c in v):
            raise ValueError('A senha deve conter pelo menos uma letra maiúscula')
        if not any(c.islower() for c in v):
            raise ValueError('A senha deve conter pelo menos uma letra minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('A senha deve conter pelo menos um número')
        return v


class UserListResponse(BaseModel):
    """Schema de resposta para lista de usuários"""
    users: List[UserResponse]
    total: int
    page: int
    size: int
    pages: int


class UserSearchQuery(BaseModel):
    """Schema para busca de usuários"""
    query: Optional[str] = Field(None, description="Termo de busca")
    status: Optional[UserStatus] = Field(None)
    role: Optional[UserRole] = Field(None)
    is_verified: Optional[bool] = Field(None)
    is_active: Optional[bool] = Field(None)
    page: int = Field(1, ge=1, description="Número da página")
    size: int = Field(20, ge=1, le=100, description="Tamanho da página")
