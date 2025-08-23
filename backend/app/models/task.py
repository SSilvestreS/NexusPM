"""
Modelo de tarefas para gerenciamento de projetos
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON, Integer, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import enum

from app.core.database import Base

class TaskStatus(str, enum.Enum):
    """Status possíveis para uma tarefa"""
    TODO = "todo"              # A fazer
    IN_PROGRESS = "in_progress" # Em progresso
    REVIEW = "review"           # Em revisão
    TESTING = "testing"         # Em teste
    DONE = "done"               # Concluída
    CANCELLED = "cancelled"     # Cancelada

class TaskPriority(str, enum.Enum):
    """Prioridades possíveis para uma tarefa"""
    LOW = "low"                 # Baixa
    MEDIUM = "medium"           # Média
    HIGH = "high"               # Alta
    URGENT = "urgent"           # Urgente
    CRITICAL = "critical"       # Crítica

class TaskType(str, enum.Enum):
    """Tipos possíveis para uma tarefa"""
    FEATURE = "feature"         # Funcionalidade
    BUG = "bug"                 # Correção de bug
    IMPROVEMENT = "improvement" # Melhoria
    DOCUMENTATION = "documentation" # Documentação
    TEST = "test"               # Teste
    RESEARCH = "research"       # Pesquisa
    OTHER = "other"             # Outro

class Task(Base):
    """Modelo de tarefa principal"""
    
    __tablename__ = "tasks"
    
    # Chave primária
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Campos básicos
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    short_description = Column(String(500), nullable=True)
    
    # Status e prioridade
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    type = Column(Enum(TaskType), default=TaskType.FEATURE, nullable=False)
    
    # Estimativas e progresso
    estimated_hours = Column(Float, nullable=True)      # Horas estimadas
    actual_hours = Column(Float, nullable=True)         # Horas reais
    progress_percentage = Column(Integer, default=0)    # Progresso em porcentagem
    
    # Datas importantes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relacionamentos
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    assignee_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    parent_task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=True)
    
    # Metadados
    tags = Column(JSON, default=[])                     # Tags para categorização
    metadata = Column(JSON, default={})                 # Metadados adicionais
    custom_fields = Column(JSON, default={})            # Campos customizados
    
    # Relacionamentos
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks")
    parent_task = relationship("Task", remote_side=[id], backref="sub_tasks")
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
    time_logs = relationship("TimeLog", back_populates="task", cascade="all, delete-orphan")
    attachments = relationship("TaskAttachment", back_populates="task", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
    
    @property
    def is_active(self) -> bool:
        """Verifica se a tarefa está ativa"""
        return self.status not in [TaskStatus.DONE, TaskStatus.CANCELLED]
    
    @property
    def is_overdue(self) -> bool:
        """Verifica se a tarefa está atrasada"""
        if not self.due_date or self.status == TaskStatus.DONE:
            return False
        return datetime.utcnow() > self.due_date
    
    @property
    def is_assigned(self) -> bool:
        """Verifica se a tarefa está atribuída"""
        return self.assignee_id is not None
    
    def update_progress(self, percentage: int):
        """Atualiza o progresso da tarefa"""
        if 0 <= percentage <= 100:
            self.progress_percentage = percentage
            if percentage == 100 and self.status != TaskStatus.DONE:
                self.status = TaskStatus.DONE
                self.completed_at = datetime.utcnow()
            elif percentage > 0 and self.status == TaskStatus.TODO:
                self.status = TaskStatus.IN_PROGRESS
                if not self.started_at:
                    self.started_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Converte tarefa para dicionário"""
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "short_description": self.short_description,
            "status": self.status.value,
            "priority": self.priority.value,
            "type": self.type.value,
            "estimated_hours": self.estimated_hours,
            "actual_hours": self.actual_hours,
            "progress_percentage": self.progress_percentage,
            "project_id": str(self.project_id),
            "assignee_id": str(self.assignee_id) if self.assignee_id else None,
            "parent_task_id": str(self.parent_task_id) if self.parent_task_id else None,
            "tags": self.tags,
            "metadata": self.metadata,
            "custom_fields": self.custom_fields,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "is_active": self.is_active,
            "is_overdue": self.is_overdue,
            "is_assigned": self.is_assigned
        }

class TimeLog(Base):
    """Registro de tempo gasto em tarefas"""
    
    __tablename__ = "time_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Informações do tempo
    hours_spent = Column(Float, nullable=False)         # Horas gastas
    description = Column(Text, nullable=True)           # Descrição do trabalho
    date = Column(DateTime(timezone=True), nullable=False) # Data do trabalho
    
    # Metadados
    is_billable = Column(Boolean, default=True)         # Se é cobrável
    rate_per_hour = Column(Float, nullable=True)        # Taxa por hora
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    task = relationship("Task", back_populates="time_logs")
    user = relationship("User")
    
    def __repr__(self):
        return f"<TimeLog(id={self.id}, task_id={self.task_id}, hours={self.hours_spent})>"
    
    @property
    def total_cost(self) -> float:
        """Calcula o custo total do registro de tempo"""
        if self.rate_per_hour:
            return self.hours_spent * self.rate_per_hour
        return 0.0
    
    def to_dict(self) -> dict:
        """Converte registro de tempo para dicionário"""
        return {
            "id": str(self.id),
            "task_id": str(self.task_id),
            "user_id": str(self.user_id),
            "hours_spent": self.hours_spent,
            "description": self.description,
            "date": self.date.isoformat() if self.date else None,
            "is_billable": self.is_billable,
            "rate_per_hour": self.rate_per_hour,
            "total_cost": self.total_cost,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class TaskAttachment(Base):
    """Anexos de tarefas"""
    
    __tablename__ = "task_attachments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Informações do arquivo
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)         # Tamanho em bytes
    mime_type = Column(String(100), nullable=False)
    
    # Metadados
    description = Column(Text, nullable=True)
    tags = Column(JSON, default=[])
    
    # Status
    is_deleted = Column(Boolean, default=False)
    
    # Timestamps
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<TaskAttachment(id={self.id}, filename='{self.filename}', task_id={self.task_id})>"
    
    def to_dict(self) -> dict:
        """Converte anexo da tarefa para dicionário"""
        return {
            "id": str(self.id),
            "task_id": str(self.task_id),
            "uploaded_by": str(self.uploaded_by),
            "filename": self.filename,
            "original_filename": self.original_filename,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "mime_type": self.mime_type,
            "description": self.description,
            "tags": self.tags,
            "is_deleted": self.is_deleted,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None
        }
