"""
Schemas para comentários e reações
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class CommentStatus(str, Enum):
    """Status do comentário"""
    ACTIVE = "active"  # Ativo
    EDITED = "edited"  # Editado
    DELETED = "deleted"  # Deletado
    PINNED = "pinned"  # Fixado
    SPAM = "spam"  # Spam


class ReactionType(str, Enum):
    """Tipos de reação disponíveis"""
    LIKE = "like"  # Curtir
    LOVE = "love"  # Amor
    LAUGH = "laugh"  # Rir
    WOW = "wow"  # Uau
    SAD = "sad"  # Triste
    ANGRY = "angry"  # Bravo
    THUMBS_UP = "thumbs_up"  # Joinha
    THUMBS_DOWN = "thumbs_down"  # Joinha para baixo
    CHECK = "check"  # Marca de verificação
    STAR = "star"  # Estrela


class CommentBase(BaseModel):
    """Schema base para comentário"""
    content: str = Field(..., min_length=1, max_length=5000, description="Conteúdo do comentário")
    is_internal: bool = Field(False, description="Se é comentário interno")
    mentions: Optional[List[str]] = Field(None, description="Usuários mencionados")
    tags: Optional[List[str]] = Field(None, description="Tags do comentário")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadados adicionais")


class CommentCreate(CommentBase):
    """Schema para criação de comentário"""
    project_id: Optional[int] = Field(None, description="ID do projeto")
    task_id: Optional[int] = Field(None, description="ID da tarefa")
    parent_comment_id: Optional[int] = Field(None, description="ID do comentário pai")
    
    @validator('content')
    def content_not_empty(cls, v):
        """Valida se o conteúdo não está vazio"""
        if not v.strip():
            raise ValueError('O conteúdo do comentário não pode estar vazio')
        return v.strip()
    
    @validator('project_id', 'task_id')
    def at_least_one_entity(cls, v, values):
        """Valida se pelo menos um ID de entidade foi fornecido"""
        if 'project_id' not in values and 'task_id' not in values:
            raise ValueError('Deve fornecer project_id ou task_id')
        return v


class CommentUpdate(BaseModel):
    """Schema para atualização de comentário"""
    content: Optional[str] = Field(None, min_length=1, max_length=5000)
    is_internal: Optional[bool] = Field(None)
    mentions: Optional[List[str]] = Field(None)
    tags: Optional[List[str]] = Field(None)
    metadata: Optional[Dict[str, Any]] = Field(None)
    
    @validator('content')
    def content_not_empty(cls, v):
        """Valida se o conteúdo não está vazio"""
        if v is not None and not v.strip():
            raise ValueError('O conteúdo do comentário não pode estar vazio')
        return v.strip() if v else v


class CommentResponse(CommentBase):
    """Schema de resposta para comentário"""
    id: int
    author_id: int
    project_id: Optional[int]
    task_id: Optional[int]
    parent_comment_id: Optional[int]
    status: CommentStatus
    created_at: datetime
    updated_at: datetime
    edited_at: Optional[datetime]
    deleted_at: Optional[datetime]
    is_pinned: bool = False
    reactions_count: int = 0
    replies_count: int = 0
    author: Optional[Dict[str, Any]] = Field(None, description="Informações do autor")
    
    class Config:
        from_attributes = True


class CommentDetailResponse(CommentResponse):
    """Schema de resposta detalhada para comentário"""
    reactions: List[Dict[str, Any]] = Field([], description="Reações ao comentário")
    replies: List[Dict[str, Any]] = Field([], description="Respostas ao comentário")
    edit_history: List[Dict[str, Any]] = Field([], description="Histórico de edições")
    mentions_users: List[Dict[str, Any]] = Field([], description="Usuários mencionados")


class CommentListResponse(BaseModel):
    """Schema de resposta para lista de comentários"""
    comments: List[CommentResponse]
    total: int
    page: int
    size: int
    pages: int


class CommentSearchQuery(BaseModel):
    """Schema para busca de comentários"""
    query: Optional[str] = Field(None, description="Termo de busca")
    project_id: Optional[int] = Field(None)
    task_id: Optional[int] = Field(None)
    author_id: Optional[int] = Field(None)
    parent_comment_id: Optional[int] = Field(None)
    status: Optional[CommentStatus] = Field(None)
    is_internal: Optional[bool] = Field(None)
    mentions: Optional[List[str]] = Field(None)
    tags: Optional[List[str]] = Field(None)
    created_from: Optional[datetime] = Field(None, description="Criado a partir de")
    created_to: Optional[datetime] = Field(None, description="Criado até")
    page: int = Field(1, ge=1, description="Número da página")
    size: int = Field(20, ge=1, le=100, description="Tamanho da página")
    sort_by: str = Field("created_at", description="Campo para ordenação")
    sort_order: str = Field("desc", description="Ordem da ordenação (asc/desc)")


class CommentReactionBase(BaseModel):
    """Schema base para reação ao comentário"""
    reaction_type: ReactionType = Field(..., description="Tipo da reação")


class CommentReactionCreate(CommentReactionBase):
    """Schema para criação de reação ao comentário"""
    comment_id: int = Field(..., description="ID do comentário")
    user_id: int = Field(..., description="ID do usuário")


class CommentReactionUpdate(BaseModel):
    """Schema para atualização de reação ao comentário"""
    reaction_type: ReactionType = Field(..., description="Novo tipo da reação")


class CommentReactionResponse(CommentReactionBase):
    """Schema de resposta para reação ao comentário"""
    id: int
    comment_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    user: Optional[Dict[str, Any]] = Field(None, description="Informações do usuário")
    
    class Config:
        from_attributes = True


class CommentReactionSummary(BaseModel):
    """Schema para resumo de reações ao comentário"""
    reaction_type: ReactionType
    count: int
    users: List[Dict[str, Any]] = Field([], description="Usuários que reagiram")


class CommentEditBase(BaseModel):
    """Schema base para edição de comentário"""
    previous_content: str = Field(..., description="Conteúdo anterior")
    edit_reason: Optional[str] = Field(None, max_length=200, description="Motivo da edição")


class CommentEditCreate(CommentEditBase):
    """Schema para criação de edição de comentário"""
    comment_id: int = Field(..., description="ID do comentário")
    edited_by: int = Field(..., description="ID do usuário que editou")


class CommentEditResponse(CommentEditBase):
    """Schema de resposta para edição de comentário"""
    id: int
    comment_id: int
    edited_by: int
    edited_at: datetime
    editor: Optional[Dict[str, Any]] = Field(None, description="Informações do editor")
    
    class Config:
        from_attributes = True


class CommentMention(BaseModel):
    """Schema para menção em comentário"""
    user_id: int
    username: str
    full_name: str
    avatar_url: Optional[str] = None


class CommentThreadResponse(BaseModel):
    """Schema de resposta para thread de comentários"""
    root_comment: CommentDetailResponse
    replies: List[CommentDetailResponse] = Field([], description="Respostas ao comentário raiz")
    total_replies: int = 0
    has_more_replies: bool = False


class CommentBulkAction(BaseModel):
    """Schema para ações em massa em comentários"""
    comment_ids: List[int] = Field(..., description="IDs dos comentários")
    action: str = Field(..., description="Ação a ser executada")
    reason: Optional[str] = Field(None, max_length=200, description="Motivo da ação")


class CommentNotification(BaseModel):
    """Schema para notificação de comentário"""
    comment_id: int
    author_id: int
    project_id: Optional[int]
    task_id: Optional[int]
    content_preview: str = Field(..., max_length=100, description="Preview do conteúdo")
    mentions: List[int] = Field([], description="IDs dos usuários mencionados")
    is_reply: bool = False
    parent_comment_id: Optional[int] = None


class CommentStatistics(BaseModel):
    """Schema para estatísticas de comentários"""
    total_comments: int = 0
    total_replies: int = 0
    total_reactions: int = 0
    comments_by_project: Dict[str, int] = Field({})
    comments_by_task: Dict[str, int] = Field({})
    reactions_by_type: Dict[str, int] = Field({})
    average_comments_per_task: float = 0.0
    most_active_users: List[Dict[str, Any]] = Field([], description="Usuários mais ativos")
