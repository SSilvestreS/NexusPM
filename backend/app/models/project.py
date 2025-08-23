"""
Modelo de projeto para gerenciamento de projetos colaborativos
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import enum

from app.core.database import Base

class ProjectStatus(str, enum.Enum):
    """Status possíveis para um projeto"""
    PLANNING = "planning"      # Planejamento
    ACTIVE = "active"          # Ativo
    ON_HOLD = "on_hold"        # Em espera
    COMPLETED = "completed"    # Concluído
    CANCELLED = "cancelled"    # Cancelado

class ProjectPriority(str, enum.Enum):
    """Prioridades possíveis para um projeto"""
    LOW = "low"                # Baixa
    MEDIUM = "medium"          # Média
    HIGH = "high"              # Alta
    URGENT = "urgent"          # Urgente

class ProjectVisibility(str, enum.Enum):
    """Visibilidades possíveis para um projeto"""
    PUBLIC = "public"          # Público
    PRIVATE = "private"        # Privado
    TEAM = "team"              # Equipe

class Project(Base):
    """Modelo de projeto principal"""
    
    __tablename__ = "projects"
    
    # Chave primária
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Campos básicos
    name = Column(String(200), nullable=False, index=True)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    short_description = Column(String(500), nullable=True)
    
    # Status e prioridade
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PLANNING, nullable=False)
    priority = Column(Enum(ProjectPriority), default=ProjectPriority.MEDIUM, nullable=False)
    visibility = Column(Enum(ProjectVisibility), default=ProjectVisibility.TEAM, nullable=False)
    
    # Datas importantes
    start_date = Column(DateTime(timezone=True), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    completed_date = Column(DateTime(timezone=True), nullable=True)
    
    # Configurações
    settings = Column(JSON, default={})  # Configurações específicas do projeto
    tags = Column(JSON, default=[])      # Tags para categorização
    metadata = Column(JSON, default={})  # Metadados adicionais
    
    # Relacionamentos
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    parent_project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    owner = relationship("User", back_populates="projects")
    parent_project = relationship("Project", remote_side=[id], backref="sub_projects")
    members = relationship("ProjectMember", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="project", cascade="all, delete-orphan")
    files = relationship("ProjectFile", back_populates="project", cascade="all, delete-orphan")
    versions = relationship("ProjectVersion", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', status='{self.status}')>"
    
    @property
    def is_active(self) -> bool:
        """Verifica se o projeto está ativo"""
        return self.status == ProjectStatus.ACTIVE
    
    @property
    def is_completed(self) -> bool:
        """Verifica se o projeto está concluído"""
        return self.status == ProjectStatus.COMPLETED
    
    @property
    def is_overdue(self) -> bool:
        """Verifica se o projeto está atrasado"""
        if not self.due_date or self.is_completed:
            return False
        return datetime.utcnow() > self.due_date
    
    def to_dict(self) -> dict:
        """Converte projeto para dicionário"""
        return {
            "id": str(self.id),
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
            "short_description": self.short_description,
            "status": self.status.value,
            "priority": self.priority.value,
            "visibility": self.visibility.value,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed_date": self.completed_date.isoformat() if self.completed_date else None,
            "owner_id": str(self.owner_id),
            "parent_project_id": str(self.parent_project_id) if self.parent_project_id else None,
            "settings": self.settings,
            "tags": self.tags,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active,
            "is_completed": self.is_completed,
            "is_overdue": self.is_overdue
        }

class ProjectMember(Base):
    """Membros de um projeto com suas permissões"""
    
    __tablename__ = "project_members"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Permissões
    role = Column(String(50), default="member", nullable=False)  # owner, admin, member, viewer
    permissions = Column(JSON, default={})  # Permissões específicas
    
    # Status
    is_active = Column(Boolean, default=True)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    left_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relacionamentos
    project = relationship("Project", back_populates="members")
    user = relationship("User", back_populates="project_memberships")
    
    def __repr__(self):
        return f"<ProjectMember(id={self.id}, project_id={self.project_id}, user_id={self.user_id}, role='{self.role}')>"
    
    def has_permission(self, permission: str) -> bool:
        """Verifica se o membro tem uma permissão específica"""
        if self.role == "owner":
            return True
        elif self.role == "admin":
            return permission in ["read", "write", "delete", "manage_members"]
        elif self.role == "member":
            return permission in ["read", "write"]
        elif self.role == "viewer":
            return permission == "read"
        return False
    
    def to_dict(self) -> dict:
        """Converte membro do projeto para dicionário"""
        return {
            "id": str(self.id),
            "project_id": str(self.project_id),
            "user_id": str(self.user_id),
            "role": self.role,
            "permissions": self.permissions,
            "is_active": self.is_active,
            "joined_at": self.joined_at.isoformat() if self.joined_at else None,
            "left_at": self.left_at.isoformat() if self.left_at else None
        }

class ProjectVersion(Base):
    """Versionamento de projetos para controle de mudanças"""
    
    __tablename__ = "project_versions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    
    # Informações da versão
    version_number = Column(String(50), nullable=False)  # ex: "1.0.0", "2.1.3"
    name = Column(String(200), nullable=True)            # Nome da versão
    description = Column(Text, nullable=True)            # Descrição das mudanças
    
    # Status da versão
    is_released = Column(Boolean, default=False)         # Se foi lançada
    is_deprecated = Column(Boolean, default=False)       # Se foi descontinuada
    
    # Dados da versão
    data_snapshot = Column(JSON, nullable=True)          # Snapshot dos dados do projeto
    changes = Column(JSON, default=[])                   # Lista de mudanças
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    released_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relacionamentos
    project = relationship("Project", back_populates="versions")
    
    def __repr__(self):
        return f"<ProjectVersion(id={self.id}, project_id={self.project_id}, version='{self.version_number}')>"
    
    def to_dict(self) -> dict:
        """Converte versão do projeto para dicionário"""
        return {
            "id": str(self.id),
            "project_id": str(self.project_id),
            "version_number": self.version_number,
            "name": self.name,
            "description": self.description,
            "is_released": self.is_released,
            "is_deprecated": self.is_deprecated,
            "data_snapshot": self.data_snapshot,
            "changes": self.changes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "released_at": self.released_at.isoformat() if self.released_at else None
        }

class ProjectFile(Base):
    """Arquivos associados a um projeto"""
    
    __tablename__ = "project_files"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Informações do arquivo
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)  # Tamanho em bytes
    mime_type = Column(String(100), nullable=False)
    
    # Metadados
    description = Column(Text, nullable=True)
    tags = Column(JSON, default=[])
    metadata = Column(JSON, default={})
    
    # Status
    is_public = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    
    # Timestamps
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<ProjectFile(id={self.id}, filename='{self.filename}', project_id={self.project_id})>"
    
    def to_dict(self) -> dict:
        """Converte arquivo do projeto para dicionário"""
        return {
            "id": str(self.id),
            "project_id": str(self.project_id),
            "uploaded_by": str(self.uploaded_by),
            "filename": self.filename,
            "original_filename": self.original_filename,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "mime_type": self.mime_type,
            "description": self.description,
            "tags": self.tags,
            "metadata": self.metadata,
            "is_public": self.is_public,
            "is_deleted": self.is_deleted,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
