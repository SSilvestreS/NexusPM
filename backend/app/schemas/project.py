"""
Schemas para projetos e membros
"""
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class ProjectStatus(str, Enum):
    """Status do projeto"""
    PLANNING = "planning"  # Planejamento
    ACTIVE = "active"  # Ativo
    ON_HOLD = "on_hold"  # Em espera
    COMPLETED = "completed"  # Concluído
    CANCELLED = "cancelled"  # Cancelado
    ARCHIVED = "archived"  # Arquivado


class ProjectPriority(str, Enum):
    """Prioridade do projeto"""
    LOW = "low"  # Baixa
    MEDIUM = "medium"  # Média
    HIGH = "high"  # Alta
    CRITICAL = "critical"  # Crítica


class ProjectVisibility(str, Enum):
    """Visibilidade do projeto"""
    PUBLIC = "public"  # Público
    PRIVATE = "private"  # Privado
    TEAM = "team"  # Equipe
    RESTRICTED = "restricted"  # Restrito


class MemberRole(str, Enum):
    """Papel do membro no projeto"""
    OWNER = "owner"  # Proprietário
    ADMIN = "admin"  # Administrador
    MEMBER = "member"  # Membro
    VIEWER = "viewer"  # Visualizador
    GUEST = "guest"  # Convidado


class ProjectBase(BaseModel):
    """Schema base para projeto"""
    name: str = Field(..., min_length=3, max_length=200, description="Nome do projeto")
    description: Optional[str] = Field(None, max_length=2000, description="Descrição do projeto")
    status: ProjectStatus = Field(ProjectStatus.PLANNING, description="Status do projeto")
    priority: ProjectPriority = Field(ProjectPriority.MEDIUM, description="Prioridade do projeto")
    visibility: ProjectVisibility = Field(ProjectVisibility.TEAM, description="Visibilidade do projeto")
    start_date: Optional[date] = Field(None, description="Data de início")
    due_date: Optional[date] = Field(None, description="Data de vencimento")
    tags: Optional[List[str]] = Field(None, description="Tags do projeto")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadados adicionais")


class ProjectCreate(ProjectBase):
    """Schema para criação de projeto"""
    parent_project_id: Optional[int] = Field(None, description="ID do projeto pai")
    template_id: Optional[int] = Field(None, description="ID do template")
    
    @validator('due_date')
    def due_date_after_start(cls, v, values):
        """Valida se a data de vencimento é após a data de início"""
        if v and 'start_date' in values and values['start_date']:
            if v <= values['start_date']:
                raise ValueError('A data de vencimento deve ser após a data de início')
        return v


class ProjectUpdate(BaseModel):
    """Schema para atualização de projeto"""
    name: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[ProjectStatus] = Field(None)
    priority: Optional[ProjectPriority] = Field(None)
    visibility: Optional[ProjectVisibility] = Field(None)
    start_date: Optional[date] = Field(None)
    due_date: Optional[date] = Field(None)
    tags: Optional[List[str]] = Field(None)
    metadata: Optional[Dict[str, Any]] = Field(None)
    
    @validator('due_date')
    def due_date_after_start(cls, v, values):
        """Valida se a data de vencimento é após a data de início"""
        if v and 'start_date' in values and values['start_date']:
            if v <= values['start_date']:
                raise ValueError('A data de vencimento deve ser após a data de início')
        return v


class ProjectResponse(ProjectBase):
    """Schema de resposta para projeto"""
    id: int
    owner_id: int
    parent_project_id: Optional[int]
    template_id: Optional[int]
    progress: float = Field(0.0, ge=0.0, le=100.0, description="Progresso do projeto (%)")
    total_tasks: int = 0
    completed_tasks: int = 0
    total_members: int = 0
    created_at: datetime
    updated_at: datetime
    archived_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ProjectDetailResponse(ProjectResponse):
    """Schema de resposta detalhada para projeto"""
    owner: Optional[Dict[str, Any]] = Field(None, description="Informações do proprietário")
    parent_project: Optional[Dict[str, Any]] = Field(None, description="Projeto pai")
    members: List[Dict[str, Any]] = Field([], description="Membros do projeto")
    recent_activities: List[Dict[str, Any]] = Field([], description="Atividades recentes")
    statistics: Dict[str, Any] = Field({}, description="Estatísticas do projeto")


class ProjectListResponse(BaseModel):
    """Schema de resposta para lista de projetos"""
    projects: List[ProjectResponse]
    total: int
    page: int
    size: int
    pages: int


class ProjectSearchQuery(BaseModel):
    """Schema para busca de projetos"""
    query: Optional[str] = Field(None, description="Termo de busca")
    status: Optional[ProjectStatus] = Field(None)
    priority: Optional[ProjectPriority] = Field(None)
    visibility: Optional[ProjectVisibility] = Field(None)
    owner_id: Optional[int] = Field(None)
    member_id: Optional[int] = Field(None)
    tags: Optional[List[str]] = Field(None)
    start_date_from: Optional[date] = Field(None, description="Data de início a partir de")
    start_date_to: Optional[date] = Field(None, description="Data de início até")
    due_date_from: Optional[date] = Field(None, description="Data de vencimento a partir de")
    due_date_to: Optional[date] = Field(None, description="Data de vencimento até")
    page: int = Field(1, ge=1, description="Número da página")
    size: int = Field(20, ge=1, le=100, description="Tamanho da página")
    sort_by: str = Field("created_at", description="Campo para ordenação")
    sort_order: str = Field("desc", description="Ordem da ordenação (asc/desc)")


class ProjectMemberBase(BaseModel):
    """Schema base para membro do projeto"""
    role: MemberRole = Field(MemberRole.MEMBER, description="Papel do membro")
    permissions: Optional[Dict[str, bool]] = Field(None, description="Permissões específicas")
    joined_at: Optional[datetime] = Field(None, description="Data de entrada")


class ProjectMemberCreate(ProjectMemberBase):
    """Schema para adicionar membro ao projeto"""
    user_id: int = Field(..., description="ID do usuário")
    project_id: int = Field(..., description="ID do projeto")


class ProjectMemberUpdate(BaseModel):
    """Schema para atualizar membro do projeto"""
    role: Optional[MemberRole] = Field(None)
    permissions: Optional[Dict[str, bool]] = Field(None)


class ProjectMemberResponse(ProjectMemberBase):
    """Schema de resposta para membro do projeto"""
    id: int
    user_id: int
    project_id: int
    user: Dict[str, Any] = Field(..., description="Informações do usuário")
    joined_at: datetime
    last_activity: Optional[datetime]
    
    class Config:
        from_attributes = True


class ProjectMemberListResponse(BaseModel):
    """Schema de resposta para lista de membros do projeto"""
    members: List[ProjectMemberResponse]
    total: int


class ProjectVersionBase(BaseModel):
    """Schema base para versão do projeto"""
    version_number: str = Field(..., description="Número da versão")
    description: Optional[str] = Field(None, max_length=1000, description="Descrição da versão")
    changes: Optional[List[str]] = Field(None, description="Lista de mudanças")
    is_released: bool = Field(False, description="Se a versão foi lançada")
    release_notes: Optional[str] = Field(None, max_length=2000, description="Notas de lançamento")


class ProjectVersionCreate(ProjectVersionBase):
    """Schema para criação de versão do projeto"""
    project_id: int = Field(..., description="ID do projeto")


class ProjectVersionUpdate(BaseModel):
    """Schema para atualização de versão do projeto"""
    description: Optional[str] = Field(None, max_length=1000)
    changes: Optional[List[str]] = Field(None)
    is_released: Optional[bool] = Field(None)
    release_notes: Optional[str] = Field(None, max_length=2000)


class ProjectVersionResponse(ProjectVersionBase):
    """Schema de resposta para versão do projeto"""
    id: int
    project_id: int
    created_by: int
    created_at: datetime
    released_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ProjectFileBase(BaseModel):
    """Schema base para arquivo do projeto"""
    filename: str = Field(..., max_length=255, description="Nome do arquivo")
    original_filename: str = Field(..., max_length=255, description="Nome original do arquivo")
    file_path: str = Field(..., description="Caminho do arquivo")
    file_size: int = Field(..., ge=0, description="Tamanho do arquivo em bytes")
    mime_type: str = Field(..., description="Tipo MIME do arquivo")
    description: Optional[str] = Field(None, max_length=500, description="Descrição do arquivo")
    tags: Optional[List[str]] = Field(None, description="Tags do arquivo")


class ProjectFileCreate(ProjectFileBase):
    """Schema para criação de arquivo do projeto"""
    project_id: int = Field(..., description="ID do projeto")
    uploaded_by: int = Field(..., description="ID do usuário que fez upload")


class ProjectFileUpdate(BaseModel):
    """Schema para atualização de arquivo do projeto"""
    filename: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = Field(None)


class ProjectFileResponse(ProjectFileBase):
    """Schema de resposta para arquivo do projeto"""
    id: int
    project_id: int
    uploaded_by: int
    upload_date: datetime
    last_modified: datetime
    download_count: int = 0
    
    class Config:
        from_attributes = True


class ProjectTemplateBase(BaseModel):
    """Schema base para template de projeto"""
    name: str = Field(..., min_length=3, max_length=200, description="Nome do template")
    description: Optional[str] = Field(None, max_length=1000, description="Descrição do template")
    category: str = Field(..., max_length=100, description="Categoria do template")
    is_public: bool = Field(False, description="Se o template é público")
    structure: Optional[Dict[str, Any]] = Field(None, description="Estrutura do template")


class ProjectTemplateCreate(ProjectTemplateBase):
    """Schema para criação de template de projeto"""
    created_by: int = Field(..., description="ID do usuário criador")


class ProjectTemplateUpdate(BaseModel):
    """Schema para atualização de template de projeto"""
    name: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    category: Optional[str] = Field(None, max_length=100)
    is_public: Optional[bool] = Field(None)
    structure: Optional[Dict[str, Any]] = Field(None)


class ProjectTemplateResponse(ProjectTemplateBase):
    """Schema de resposta para template de projeto"""
    id: int
    created_by: int
    usage_count: int = 0
    rating: float = 0.0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
