"""
Schemas para notificações e preferências
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class NotificationType(str, Enum):
    """Tipos de notificação"""
    PROJECT_UPDATE = "project_update"  # Atualização de projeto
    TASK_ASSIGNMENT = "task_assignment"  # Atribuição de tarefa
    TASK_UPDATE = "task_update"  # Atualização de tarefa
    COMMENT_ADDED = "comment_added"  # Comentário adicionado
    COMMENT_MENTION = "comment_mention"  # Menção em comentário
    DEADLINE_APPROACHING = "deadline_approaching"  # Prazo se aproximando
    DEADLINE_PASSED = "deadline_passed"  # Prazo vencido
    PROJECT_INVITATION = "project_invitation"  # Convite para projeto
    TASK_COMPLETED = "task_completed"  # Tarefa concluída
    MILESTONE_REACHED = "milestone_reached"  # Marco alcançado
    FILE_UPLOADED = "file_uploaded"  # Arquivo enviado
    SYSTEM_ANNOUNCEMENT = "system_announcement"  # Anúncio do sistema
    SECURITY_ALERT = "security_alert"  # Alerta de segurança


class NotificationPriority(str, Enum):
    """Prioridade da notificação"""
    LOW = "low"  # Baixa
    NORMAL = "normal"  # Normal
    HIGH = "high"  # Alta
    URGENT = "urgent"  # Urgente
    CRITICAL = "critical"  # Crítica


class NotificationStatus(str, Enum):
    """Status da notificação"""
    UNREAD = "unread"  # Não lida
    READ = "read"  # Lida
    ARCHIVED = "archived"  # Arquivada
    DELETED = "deleted"  # Deletada


class NotificationChannel(str, Enum):
    """Canais de notificação"""
    IN_APP = "in_app"  # No aplicativo
    EMAIL = "email"  # Email
    PUSH = "push"  # Push notification
    SMS = "sms"  # SMS
    WEBHOOK = "webhook"  # Webhook
    SLACK = "slack"  # Slack
    TEAMS = "teams"  # Microsoft Teams


class NotificationBase(BaseModel):
    """Schema base para notificação"""
    type: NotificationType = Field(..., description="Tipo da notificação")
    priority: NotificationPriority = Field(NotificationPriority.NORMAL, description="Prioridade da notificação")
    title: str = Field(..., min_length=3, max_length=200, description="Título da notificação")
    message: str = Field(..., min_length=1, max_length=1000, description="Mensagem da notificação")
    action_url: Optional[str] = Field(None, description="URL de ação")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadados adicionais")


class NotificationCreate(NotificationBase):
    """Schema para criação de notificação"""
    recipient_id: int = Field(..., description="ID do destinatário")
    sender_id: Optional[int] = Field(None, description="ID do remetente")
    project_id: Optional[int] = Field(None, description="ID do projeto relacionado")
    task_id: Optional[int] = Field(None, description="ID da tarefa relacionada")
    comment_id: Optional[int] = Field(None, description="ID do comentário relacionado")
    channels: List[NotificationChannel] = Field([NotificationChannel.IN_APP], description="Canais de envio")
    
    @validator('channels')
    def at_least_one_channel(cls, v):
        """Valida se pelo menos um canal foi especificado"""
        if not v:
            raise ValueError('Deve especificar pelo menos um canal de notificação')
        return v


class NotificationUpdate(BaseModel):
    """Schema para atualização de notificação"""
    status: Optional[NotificationStatus] = Field(None)
    read_at: Optional[datetime] = Field(None)
    archived_at: Optional[datetime] = Field(None)


class NotificationResponse(NotificationBase):
    """Schema de resposta para notificação"""
    id: int
    recipient_id: int
    sender_id: Optional[int]
    project_id: Optional[int]
    task_id: Optional[int]
    comment_id: Optional[int]
    status: NotificationStatus
    channels: List[NotificationChannel]
    created_at: datetime
    updated_at: datetime
    read_at: Optional[datetime]
    archived_at: Optional[datetime]
    deleted_at: Optional[datetime]
    sender: Optional[Dict[str, Any]] = Field(None, description="Informações do remetente")
    project: Optional[Dict[str, Any]] = Field(None, description="Informações do projeto")
    task: Optional[Dict[str, Any]] = Field(None, description="Informações da tarefa")
    
    class Config:
        from_attributes = True


class NotificationDetailResponse(NotificationResponse):
    """Schema de resposta detalhada para notificação"""
    related_notifications: List[Dict[str, Any]] = Field([], description="Notificações relacionadas")
    delivery_status: Dict[str, Any] = Field({}, description="Status de entrega por canal")


class NotificationListResponse(BaseModel):
    """Schema de resposta para lista de notificações"""
    notifications: List[NotificationResponse]
    total: int
    unread_count: int
    page: int
    size: int
    pages: int


class NotificationSearchQuery(BaseModel):
    """Schema para busca de notificações"""
    query: Optional[str] = Field(None, description="Termo de busca")
    type: Optional[NotificationType] = Field(None)
    priority: Optional[NotificationPriority] = Field(None)
    status: Optional[NotificationStatus] = Field(None)
    recipient_id: Optional[int] = Field(None)
    sender_id: Optional[int] = Field(None)
    project_id: Optional[int] = Field(None)
    task_id: Optional[int] = Field(None)
    channels: Optional[List[NotificationChannel]] = Field(None)
    created_from: Optional[datetime] = Field(None, description="Criado a partir de")
    created_to: Optional[datetime] = Field(None, description="Criado até")
    page: int = Field(1, ge=1, description="Número da página")
    size: int = Field(20, ge=1, le=100, description="Tamanho da página")
    sort_by: str = Field("created_at", description="Campo para ordenação")
    sort_order: str = Field("desc", description="Ordem da ordenação (asc/desc)")


class NotificationPreferenceBase(BaseModel):
    """Schema base para preferências de notificação"""
    email_notifications: bool = Field(True, description="Notificações por email")
    push_notifications: bool = Field(True, description="Notificações push")
    sms_notifications: bool = Field(False, description="Notificações por SMS")
    in_app_notifications: bool = Field(True, description="Notificações no aplicativo")
    webhook_notifications: bool = Field(False, description="Notificações por webhook")
    slack_notifications: bool = Field(False, description="Notificações no Slack")
    teams_notifications: bool = Field(False, description="Notificações no Teams")


class NotificationPreferenceCreate(NotificationPreferenceBase):
    """Schema para criação de preferências de notificação"""
    user_id: int = Field(..., description="ID do usuário")


class NotificationPreferenceUpdate(BaseModel):
    """Schema para atualização de preferências de notificação"""
    email_notifications: Optional[bool] = Field(None)
    push_notifications: Optional[bool] = Field(None)
    sms_notifications: Optional[bool] = Field(None)
    in_app_notifications: Optional[bool] = Field(None)
    webhook_notifications: Optional[bool] = Field(None)
    slack_notifications: Optional[bool] = Field(None)
    teams_notifications: Optional[bool] = Field(None)


class NotificationPreferenceResponse(NotificationPreferenceBase):
    """Schema de resposta para preferências de notificação"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class NotificationTypePreferenceBase(BaseModel):
    """Schema base para preferências por tipo de notificação"""
    notification_type: NotificationType = Field(..., description="Tipo da notificação")
    email_enabled: bool = Field(True, description="Habilitado para email")
    push_enabled: bool = Field(True, description="Habilitado para push")
    sms_enabled: bool = Field(False, description="Habilitado para SMS")
    in_app_enabled: bool = Field(True, description="Habilitado para aplicativo")
    webhook_enabled: bool = Field(False, description="Habilitado para webhook")
    slack_enabled: bool = Field(False, description="Habilitado para Slack")
    teams_enabled: bool = Field(False, description="Habilitado para Teams")


class NotificationTypePreferenceCreate(NotificationTypePreferenceBase):
    """Schema para criação de preferências por tipo"""
    user_id: int = Field(..., description="ID do usuário")


class NotificationTypePreferenceUpdate(BaseModel):
    """Schema para atualização de preferências por tipo"""
    email_enabled: Optional[bool] = Field(None)
    push_enabled: Optional[bool] = Field(None)
    sms_enabled: Optional[bool] = Field(None)
    in_app_enabled: Optional[bool] = Field(None)
    webhook_enabled: Optional[bool] = Field(None)
    slack_enabled: Optional[bool] = Field(None)
    teams_enabled: Optional[bool] = Field(None)


class NotificationTypePreferenceResponse(NotificationTypePreferenceBase):
    """Schema de resposta para preferências por tipo"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class NotificationTemplateBase(BaseModel):
    """Schema base para template de notificação"""
    name: str = Field(..., min_length=3, max_length=100, description="Nome do template")
    type: NotificationType = Field(..., description="Tipo da notificação")
    title_template: str = Field(..., min_length=3, max_length=200, description="Template do título")
    message_template: str = Field(..., min_length=1, max_length=1000, description="Template da mensagem")
    is_active: bool = Field(True, description="Se o template está ativo")
    variables: Optional[List[str]] = Field(None, description="Variáveis disponíveis no template")


class NotificationTemplateCreate(NotificationTemplateBase):
    """Schema para criação de template de notificação"""
    created_by: int = Field(..., description="ID do usuário criador")


class NotificationTemplateUpdate(BaseModel):
    """Schema para atualização de template de notificação"""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    title_template: Optional[str] = Field(None, min_length=3, max_length=200)
    message_template: Optional[str] = Field(None, min_length=1, max_length=1000)
    is_active: Optional[bool] = Field(None)
    variables: Optional[List[str]] = Field(None)


class NotificationTemplateResponse(NotificationTemplateBase):
    """Schema de resposta para template de notificação"""
    id: int
    created_by: int
    usage_count: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class NotificationBulkAction(BaseModel):
    """Schema para ações em massa em notificações"""
    notification_ids: List[int] = Field(..., description="IDs das notificações")
    action: str = Field(..., description="Ação a ser executada")
    reason: Optional[str] = Field(None, max_length=200, description="Motivo da ação")


class NotificationDeliveryStatus(BaseModel):
    """Schema para status de entrega da notificação"""
    notification_id: int
    channel: NotificationChannel
    status: str = Field(..., description="Status da entrega")
    sent_at: Optional[datetime] = Field(None, description="Hora do envio")
    delivered_at: Optional[datetime] = Field(None, description="Hora da entrega")
    error_message: Optional[str] = Field(None, description="Mensagem de erro")
    retry_count: int = 0
    max_retries: int = 3


class NotificationStatistics(BaseModel):
    """Schema para estatísticas de notificações"""
    total_notifications: int = 0
    unread_notifications: int = 0
    read_notifications: int = 0
    archived_notifications: int = 0
    notifications_by_type: Dict[str, int] = Field({})
    notifications_by_priority: Dict[str, int] = Field({})
    notifications_by_channel: Dict[str, int] = Field({})
    delivery_success_rate: float = 0.0
    average_delivery_time: Optional[float] = Field(None, description="Tempo médio de entrega em segundos")
    most_active_senders: List[Dict[str, Any]] = Field([], description="Remetentes mais ativos")
