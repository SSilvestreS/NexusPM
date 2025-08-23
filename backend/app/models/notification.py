"""
Modelo de notificações para usuários
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import enum

from app.core.database import Base

class NotificationType(str, enum.Enum):
    """Tipos possíveis de notificação"""
    PROJECT_INVITE = "project_invite"           # Convite para projeto
    TASK_ASSIGNED = "task_assigned"             # Tarefa atribuída
    TASK_UPDATED = "task_updated"               # Tarefa atualizada
    COMMENT_MENTION = "comment_mention"         # Mencionado em comentário
    COMMENT_REPLY = "comment_reply"             # Resposta ao comentário
    PROJECT_UPDATE = "project_update"            # Atualização do projeto
    DEADLINE_REMINDER = "deadline_reminder"     # Lembrete de prazo
    SYSTEM_MESSAGE = "system_message"           # Mensagem do sistema
    CUSTOM = "custom"                           # Notificação customizada

class NotificationPriority(str, enum.Enum):
    """Prioridades possíveis para notificações"""
    LOW = "low"                 # Baixa
    NORMAL = "normal"           # Normal
    HIGH = "high"               # Alta
    URGENT = "urgent"           # Urgente

class NotificationStatus(str, enum.Enum):
    """Status possíveis para notificações"""
    UNREAD = "unread"           # Não lida
    READ = "read"               # Lida
    ARCHIVED = "archived"       # Arquivada
    DELETED = "deleted"         # Deletada

class Notification(Base):
    """Modelo de notificação principal"""
    
    __tablename__ = "notifications"
    
    # Chave primária
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Usuário destinatário
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Tipo e prioridade
    type = Column(Enum(NotificationType), nullable=False)
    priority = Column(Enum(NotificationPriority), default=NotificationPriority.NORMAL, nullable=False)
    status = Column(Enum(NotificationStatus), default=NotificationStatus.UNREAD, nullable=False)
    
    # Conteúdo da notificação
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    message_html = Column(Text, nullable=True)  # Versão HTML renderizada
    
    # Dados relacionados
    related_project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True)
    related_task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=True)
    related_comment_id = Column(UUID(as_uuid=True), ForeignKey("comments.id"), nullable=True)
    related_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Metadados
    metadata = Column(JSON, default={})                 # Dados adicionais
    action_url = Column(String(500), nullable=True)     # URL para ação
    action_text = Column(String(100), nullable=True)    # Texto do botão de ação
    
    # Configurações
    is_push_enabled = Column(Boolean, default=True)     # Se deve enviar push notification
    is_email_enabled = Column(Boolean, default=True)    # Se deve enviar email
    is_sms_enabled = Column(Boolean, default=False)     # Se deve enviar SMS
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    read_at = Column(DateTime(timezone=True), nullable=True)
    archived_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relacionamentos
    user = relationship("User", back_populates="notifications")
    related_project = relationship("Project")
    related_task = relationship("Task")
    related_comment = relationship("Comment")
    related_user = relationship("User")
    
    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type='{self.type}', title='{self.title}')>"
    
    @property
    def is_unread(self) -> bool:
        """Verifica se a notificação não foi lida"""
        return self.status == NotificationStatus.UNREAD
    
    @property
    def is_read(self) -> bool:
        """Verifica se a notificação foi lida"""
        return self.status == NotificationStatus.READ
    
    @property
    def is_archived(self) -> bool:
        """Verifica se a notificação foi arquivada"""
        return self.status == NotificationStatus.ARCHIVED
    
    def mark_as_read(self):
        """Marca a notificação como lida"""
        if self.status == NotificationStatus.UNREAD:
            self.status = NotificationStatus.READ
            self.read_at = datetime.utcnow()
    
    def mark_as_unread(self):
        """Marca a notificação como não lida"""
        self.status = NotificationStatus.UNREAD
        self.read_at = None
    
    def archive(self):
        """Arquiva a notificação"""
        self.status = NotificationStatus.ARCHIVED
        self.archived_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Converte notificação para dicionário"""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "type": self.type.value,
            "priority": self.priority.value,
            "status": self.status.value,
            "title": self.title,
            "message": self.message,
            "message_html": self.message_html,
            "related_project_id": str(self.related_project_id) if self.related_project_id else None,
            "related_task_id": str(self.related_task_id) if self.related_task_id else None,
            "related_comment_id": str(self.related_comment_id) if self.related_comment_id else None,
            "related_user_id": str(self.related_user_id) if self.related_user_id else None,
            "metadata": self.metadata,
            "action_url": self.action_url,
            "action_text": self.action_text,
            "is_push_enabled": self.is_push_enabled,
            "is_email_enabled": self.is_email_enabled,
            "is_sms_enabled": self.is_sms_enabled,
            "is_unread": self.is_unread,
            "is_read": self.is_read,
            "is_archived": self.is_archived,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "read_at": self.read_at.isoformat() if self.read_at else None,
            "archived_at": self.archived_at.isoformat() if self.archived_at else None
        }

class NotificationTemplate(Base):
    """Templates para notificações"""
    
    __tablename__ = "notification_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Identificação do template
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Tipo de notificação
    notification_type = Column(Enum(NotificationType), nullable=False)
    
    # Conteúdo do template
    title_template = Column(String(200), nullable=False)
    message_template = Column(Text, nullable=False)
    message_html_template = Column(Text, nullable=True)
    
    # Configurações padrão
    default_priority = Column(Enum(NotificationPriority), default=NotificationPriority.NORMAL, nullable=False)
    default_push_enabled = Column(Boolean, default=True)
    default_email_enabled = Column(Boolean, default=True)
    default_sms_enabled = Column(Boolean, default=False)
    
    # Variáveis do template
    variables = Column(JSON, default=[])                 # Lista de variáveis disponíveis
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<NotificationTemplate(id={self.id}, name='{self.name}', type='{self.notification_type}')>"
    
    def render(self, **kwargs) -> dict:
        """Renderiza o template com as variáveis fornecidas"""
        title = self.title_template
        message = self.message_template
        message_html = self.message_html_template
        
        # Substitui variáveis nos templates
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            title = title.replace(placeholder, str(value))
            message = message.replace(placeholder, str(value))
            if message_html:
                message_html = message_html.replace(placeholder, str(value))
        
        return {
            "title": title,
            "message": message,
            "message_html": message_html,
            "priority": self.default_priority,
            "push_enabled": self.default_push_enabled,
            "email_enabled": self.default_email_enabled,
            "sms_enabled": self.default_sms_enabled
        }
    
    def to_dict(self) -> dict:
        """Converte template para dicionário"""
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "notification_type": self.notification_type.value,
            "title_template": self.title_template,
            "message_template": self.message_template,
            "message_html_template": self.message_html_template,
            "default_priority": self.default_priority.value,
            "default_push_enabled": self.default_push_enabled,
            "default_email_enabled": self.default_email_enabled,
            "default_sms_enabled": self.default_sms_enabled,
            "variables": self.variables,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class NotificationPreference(Base):
    """Preferências de notificação dos usuários"""
    
    __tablename__ = "notification_preferences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Tipo de notificação
    notification_type = Column(Enum(NotificationType), nullable=False)
    
    # Configurações de canal
    push_enabled = Column(Boolean, default=True)
    email_enabled = Column(Boolean, default=True)
    sms_enabled = Column(Boolean, default=False)
    
    # Configurações de frequência
    frequency = Column(String(50), default="immediate")  # immediate, daily, weekly, never
    
    # Configurações de horário
    quiet_hours_start = Column(String(5), nullable=True)  # HH:MM
    quiet_hours_end = Column(String(5), nullable=True)    # HH:MM
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    user = relationship("User")
    
    def __repr__(self):
        return f"<NotificationPreference(id={self.id}, user_id={self.user_id}, type='{self.notification_type}')>"
    
    def is_quiet_hours(self, current_time: datetime = None) -> bool:
        """Verifica se está no período de silêncio"""
        if not self.quiet_hours_start or not self.quiet_hours_end:
            return False
        
        if not current_time:
            current_time = datetime.utcnow()
        
        current_time_str = current_time.strftime("%H:%M")
        return self.quiet_hours_start <= current_time_str <= self.quiet_hours_end
    
    def to_dict(self) -> dict:
        """Converte preferência para dicionário"""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "notification_type": self.notification_type.value,
            "push_enabled": self.push_enabled,
            "email_enabled": self.email_enabled,
            "sms_enabled": self.sms_enabled,
            "frequency": self.frequency,
            "quiet_hours_start": self.quiet_hours_start,
            "quiet_hours_end": self.quiet_hours_end,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
