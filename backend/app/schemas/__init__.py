"""
Inicialização dos schemas Pydantic da aplicação
"""

# Importa todos os schemas para garantir que sejam registrados
from .auth import (
    UserRegister,
    UserLogin,
    TokenResponse,
    PasswordReset,
    PasswordResetConfirm,
    OAuthLogin,
    ChangePassword,
    UserProfileUpdate,
    EmailVerification,
    ResendVerification
)

# Lista de todos os schemas para facilitar operações em lote
__all__ = [
    # Schemas de autenticação
    "UserRegister",
    "UserLogin", 
    "TokenResponse",
    "PasswordReset",
    "PasswordResetConfirm",
    "OAuthLogin",
    "ChangePassword",
    "UserProfileUpdate",
    "EmailVerification",
    "ResendVerification",
]

# Função para obter todos os schemas
def get_all_schemas():
    """Retorna uma lista de todas as classes de schema"""
    return [
        UserRegister,
        UserLogin,
        TokenResponse,
        PasswordReset,
        PasswordResetConfirm,
        OAuthLogin,
        ChangePassword,
        UserProfileUpdate,
        EmailVerification,
        ResendVerification,
    ]
