"""
Inicialização dos modelos de dados da aplicação
"""

# Importa todos os modelos para garantir que sejam registrados no SQLAlchemy
from .user import User, UserSession, UserPreference
from .project import Project, ProjectMember, ProjectVersion, ProjectFile
from .task import Task, TimeLog, TaskAttachment
from .comment import Comment, CommentReaction, CommentEdit
from .notification import Notification, NotificationTemplate, NotificationPreference

# Lista de todos os modelos para facilitar operações em lote
__all__ = [
    # Modelos de usuário
    "User",
    "UserSession", 
    "UserPreference",
    
    # Modelos de projeto
    "Project",
    "ProjectMember",
    "ProjectVersion",
    "ProjectFile",
    
    # Modelos de tarefa
    "Task",
    "TimeLog",
    "TaskAttachment",
    
    # Modelos de comentário
    "Comment",
    "CommentReaction",
    "CommentEdit",
    
    # Modelos de notificação
    "Notification",
    "NotificationTemplate",
    "NotificationPreference",
]

# Função para obter todos os modelos
def get_all_models():
    """Retorna uma lista de todas as classes de modelo"""
    return [
        User, UserSession, UserPreference,
        Project, ProjectMember, ProjectVersion, ProjectFile,
        Task, TimeLog, TaskAttachment,
        Comment, CommentReaction, CommentEdit,
        Notification, NotificationTemplate, NotificationPreference,
    ]

# Função para criar todas as tabelas
def create_all_tables(engine):
    """Cria todas as tabelas no banco de dados"""
    from app.core.database import Base
    Base.metadata.create_all(bind=engine)

# Função para dropar todas as tabelas
def drop_all_tables(engine):
    """Remove todas as tabelas do banco de dados"""
    from app.core.database import Base
    Base.metadata.drop_all(bind=engine)
