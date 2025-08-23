"""
Schemas para tarefas e logs de tempo
"""
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class TaskStatus(str, Enum):
    """Status da tarefa"""
    TODO = "todo"  # A fazer
    IN_PROGRESS = "in_progress"  # Em progresso
    REVIEW = "review"  # Em revisão
    TESTING = "testing"  # Em teste
    DONE = "done"  # Concluída
    CANCELLED = "cancelled"  # Cancelada
    BLOCKED = "blocked"  # Bloqueada


class TaskPriority(str, Enum):
    """Prioridade da tarefa"""
    LOW = "low"  # Baixa
    MEDIUM = "medium"  # Média
    HIGH = "high"  # Alta
    URGENT = "urgent"  # Urgente
    CRITICAL = "critical"  # Crítica


class TaskType(str, Enum):
    """Tipo da tarefa"""
    FEATURE = "feature"  # Funcionalidade
    BUG = "bug"  # Correção de bug
    IMPROVEMENT = "improvement"  # Melhoria
    DOCUMENTATION = "documentation"  # Documentação
    TESTING = "testing"  # Teste
    DESIGN = "design"  # Design
    RESEARCH = "research"  # Pesquisa
    MAINTENANCE = "maintenance"  # Manutenção


class TaskBase(BaseModel):
    """Schema base para tarefa"""
    title: str = Field(..., min_length=3, max_length=200, description="Título da tarefa")
    description: Optional[str] = Field(None, max_length=2000, description="Descrição da tarefa")
    status: TaskStatus = Field(TaskStatus.TODO, description="Status da tarefa")
    priority: TaskPriority = Field(TaskPriority.MEDIUM, description="Prioridade da tarefa")
    type: TaskType = Field(TaskType.FEATURE, description="Tipo da tarefa")
    estimated_hours: Optional[float] = Field(None, ge=0, description="Horas estimadas")
    actual_hours: Optional[float] = Field(None, ge=0, description="Horas reais")
    progress: float = Field(0.0, ge=0.0, le=100.0, description="Progresso da tarefa (%)")
    start_date: Optional[date] = Field(None, description="Data de início")
    due_date: Optional[date] = Field(None, description="Data de vencimento")
    tags: Optional[List[str]] = Field(None, description="Tags da tarefa")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadados adicionais")


class TaskCreate(TaskBase):
    """Schema para criação de tarefa"""
    project_id: int = Field(..., description="ID do projeto")
    assignee_id: Optional[int] = Field(None, description="ID do responsável")
    parent_task_id: Optional[int] = Field(None, description="ID da tarefa pai")
    
    @validator('due_date')
    def due_date_after_start(cls, v, values):
        """Valida se a data de vencimento é após a data de início"""
        if v and 'start_date' in values and values['start_date']:
            if v <= values['start_date']:
                raise ValueError('A data de vencimento deve ser após a data de início')
        return v
    
    @validator('estimated_hours')
    def estimated_hours_positive(cls, v):
        """Valida se as horas estimadas são positivas"""
        if v is not None and v <= 0:
            raise ValueError('As horas estimadas devem ser maiores que zero')
        return v


class TaskUpdate(BaseModel):
    """Schema para atualização de tarefa"""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatus] = Field(None)
    priority: Optional[TaskPriority] = Field(None)
    type: Optional[TaskType] = Field(None)
    estimated_hours: Optional[float] = Field(None, ge=0)
    actual_hours: Optional[float] = Field(None, ge=0)
    progress: Optional[float] = Field(None, ge=0.0, le=100.0)
    start_date: Optional[date] = Field(None)
    due_date: Optional[date] = Field(None)
    assignee_id: Optional[int] = Field(None)
    parent_task_id: Optional[int] = Field(None)
    tags: Optional[List[str]] = Field(None)
    metadata: Optional[Dict[str, Any]] = Field(None)
    
    @validator('due_date')
    def due_date_after_start(cls, v, values):
        """Valida se a data de vencimento é após a data de início"""
        if v and 'start_date' in values and values['start_date']:
            if v <= values['start_date']:
                raise ValueError('A data de vencimento deve ser após a data de início')
        return v


class TaskResponse(TaskBase):
    """Schema de resposta para tarefa"""
    id: int
    project_id: int
    assignee_id: Optional[int]
    parent_task_id: Optional[int]
    created_by: int
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    assignee: Optional[Dict[str, Any]] = Field(None, description="Informações do responsável")
    project: Optional[Dict[str, Any]] = Field(None, description="Informações do projeto")
    
    class Config:
        from_attributes = True


class TaskDetailResponse(TaskResponse):
    """Schema de resposta detalhada para tarefa"""
    subtasks: List[Dict[str, Any]] = Field([], description="Subtarefas")
    comments: List[Dict[str, Any]] = Field([], description="Comentários")
    attachments: List[Dict[str, Any]] = Field([], description="Anexos")
    time_logs: List[Dict[str, Any]] = Field([], description="Logs de tempo")
    dependencies: List[Dict[str, Any]] = Field([], description="Dependências")
    history: List[Dict[str, Any]] = Field([], description="Histórico de mudanças")


class TaskListResponse(BaseModel):
    """Schema de resposta para lista de tarefas"""
    tasks: List[TaskResponse]
    total: int
    page: int
    size: int
    pages: int


class TaskSearchQuery(BaseModel):
    """Schema para busca de tarefas"""
    query: Optional[str] = Field(None, description="Termo de busca")
    project_id: Optional[int] = Field(None)
    assignee_id: Optional[int] = Field(None)
    status: Optional[TaskStatus] = Field(None)
    priority: Optional[TaskPriority] = Field(None)
    type: Optional[TaskType] = Field(None)
    tags: Optional[List[str]] = Field(None)
    start_date_from: Optional[date] = Field(None, description="Data de início a partir de")
    start_date_to: Optional[date] = Field(None, description="Data de início até")
    due_date_from: Optional[date] = Field(None, description="Data de vencimento a partir de")
    due_date_to: Optional[date] = Field(None, description="Data de vencimento até")
    overdue: Optional[bool] = Field(None, description="Tarefas vencidas")
    page: int = Field(1, ge=1, description="Número da página")
    size: int = Field(20, ge=1, le=100, description="Tamanho da página")
    sort_by: str = Field("created_at", description="Campo para ordenação")
    sort_order: str = Field("desc", description="Ordem da ordenação (asc/desc)")


class TimeLogBase(BaseModel):
    """Schema base para log de tempo"""
    description: str = Field(..., min_length=3, max_length=500, description="Descrição do trabalho")
    hours_spent: float = Field(..., gt=0, le=24, description="Horas gastas")
    date: date = Field(..., description="Data do trabalho")
    start_time: Optional[datetime] = Field(None, description="Hora de início")
    end_time: Optional[datetime] = Field(None, description="Hora de fim")


class TimeLogCreate(TimeLogBase):
    """Schema para criação de log de tempo"""
    task_id: int = Field(..., description="ID da tarefa")
    user_id: int = Field(..., description="ID do usuário")
    
    @validator('hours_spent')
    def hours_spent_reasonable(cls, v):
        """Valida se as horas gastas são razoáveis"""
        if v > 24:
            raise ValueError('As horas gastas não podem exceder 24 horas por dia')
        return v


class TimeLogUpdate(BaseModel):
    """Schema para atualização de log de tempo"""
    description: Optional[str] = Field(None, min_length=3, max_length=500)
    hours_spent: Optional[float] = Field(None, gt=0, le=24)
    date: Optional[date] = Field(None)
    start_time: Optional[datetime] = Field(None)
    end_time: Optional[datetime] = Field(None)


class TimeLogResponse(TimeLogBase):
    """Schema de resposta para log de tempo"""
    id: int
    task_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: Optional[Dict[str, Any]] = Field(None, description="Informações do usuário")
    task: Optional[Dict[str, Any]] = Field(None, description="Informações da tarefa")
    
    class Config:
        from_attributes = True


class TaskAttachmentBase(BaseModel):
    """Schema base para anexo de tarefa"""
    filename: str = Field(..., max_length=255, description="Nome do arquivo")
    original_filename: str = Field(..., max_length=255, description="Nome original do arquivo")
    file_path: str = Field(..., description="Caminho do arquivo")
    file_size: int = Field(..., ge=0, description="Tamanho do arquivo em bytes")
    mime_type: str = Field(..., description="Tipo MIME do arquivo")
    description: Optional[str] = Field(None, max_length=500, description="Descrição do anexo")


class TaskAttachmentCreate(TaskAttachmentBase):
    """Schema para criação de anexo de tarefa"""
    task_id: int = Field(..., description="ID da tarefa")
    uploaded_by: int = Field(..., description="ID do usuário que fez upload")


class TaskAttachmentUpdate(BaseModel):
    """Schema para atualização de anexo de tarefa"""
    filename: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=500)


class TaskAttachmentResponse(TaskAttachmentBase):
    """Schema de resposta para anexo de tarefa"""
    id: int
    task_id: int
    uploaded_by: int
    upload_date: datetime
    download_count: int = 0
    
    class Config:
        from_attributes = True


class TaskDependencyBase(BaseModel):
    """Schema base para dependência de tarefa"""
    dependent_task_id: int = Field(..., description="ID da tarefa dependente")
    prerequisite_task_id: int = Field(..., description="ID da tarefa pré-requisito")
    dependency_type: str = Field("finish_to_start", description="Tipo de dependência")
    lag_days: int = Field(0, ge=0, description="Dias de atraso")


class TaskDependencyCreate(TaskDependencyBase):
    """Schema para criação de dependência de tarefa"""
    pass


class TaskDependencyResponse(TaskDependencyBase):
    """Schema de resposta para dependência de tarefa"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class TaskBulkUpdate(BaseModel):
    """Schema para atualização em massa de tarefas"""
    task_ids: List[int] = Field(..., description="IDs das tarefas")
    status: Optional[TaskStatus] = Field(None)
    priority: Optional[TaskPriority] = Field(None)
    assignee_id: Optional[int] = Field(None)
    tags: Optional[List[str]] = Field(None)
    due_date: Optional[date] = Field(None)


class TaskStatistics(BaseModel):
    """Schema para estatísticas de tarefas"""
    total_tasks: int = 0
    completed_tasks: int = 0
    in_progress_tasks: int = 0
    overdue_tasks: int = 0
    total_estimated_hours: float = 0.0
    total_actual_hours: float = 0.0
    average_completion_time: Optional[float] = Field(None, description="Tempo médio de conclusão em dias")
    tasks_by_status: Dict[str, int] = Field({})
    tasks_by_priority: Dict[str, int] = Field({})
    tasks_by_type: Dict[str, int] = Field({})
