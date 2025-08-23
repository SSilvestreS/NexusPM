"""
Modelo de comentários para projetos e tarefas
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import re

from app.core.database import Base

class Comment(Base):
    """Modelo de comentário principal"""
    
    __tablename__ = "comments"
    
    # Chave primária
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Conteúdo do comentário
    content = Column(Text, nullable=False)
    content_html = Column(Text, nullable=True)  # Versão HTML renderizada
    
    # Relacionamentos principais
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=True)
    
    # Comentário pai (para respostas aninhadas)
    parent_comment_id = Column(UUID(as_uuid=True), ForeignKey("comments.id"), nullable=True)
    
    # Metadados
    mentions = Column(JSON, default=[])                 # Usuários mencionados
    tags = Column(JSON, default=[])                     # Tags do comentário
    metadata = Column(JSON, default={})                 # Metadados adicionais
    
    # Status
    is_edited = Column(Boolean, default=False)          # Se foi editado
    is_deleted = Column(Boolean, default=False)         # Se foi deletado
    is_pinned = Column(Boolean, default=False)          # Se está fixado
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    edited_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relacionamentos
    author = relationship("User", back_populates="comments")
    project = relationship("Project", back_populates="comments")
    task = relationship("Task", back_populates="comments")
    parent_comment = relationship("Comment", remote_side=[id], backref="replies")
    
    def __repr__(self):
        return f"<Comment(id={self.id}, author_id={self.author_id}, content='{self.content[:50]}...')>"
    
    @property
    def is_reply(self) -> bool:
        """Verifica se é uma resposta a outro comentário"""
        return self.parent_comment_id is not None
    
    @property
    def has_replies(self) -> bool:
        """Verifica se tem respostas"""
        return len(self.replies) > 0
    
    @property
    def reply_count(self) -> int:
        """Conta o número de respostas"""
        return len(self.replies)
    
    def extract_mentions(self) -> list:
        """Extrai menções de usuários do conteúdo"""
        # Padrão para menções: @username
        mention_pattern = r'@(\w+)'
        mentions = re.findall(mention_pattern, self.content)
        return list(set(mentions))  # Remove duplicatas
    
    def extract_tags(self) -> list:
        """Extrai tags do conteúdo"""
        # Padrão para tags: #tag
        tag_pattern = r'#(\w+)'
        tags = re.findall(tag_pattern, self.content)
        return list(set(tags))  # Remove duplicatas
    
    def mark_as_edited(self):
        """Marca o comentário como editado"""
        self.is_edited = True
        self.edited_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Converte comentário para dicionário"""
        return {
            "id": str(self.id),
            "content": self.content,
            "content_html": self.content_html,
            "author_id": str(self.author_id),
            "project_id": str(self.project_id) if self.project_id else None,
            "task_id": str(self.task_id) if self.task_id else None,
            "parent_comment_id": str(self.parent_comment_id) if self.parent_comment_id else None,
            "mentions": self.mentions,
            "tags": self.tags,
            "metadata": self.metadata,
            "is_edited": self.is_edited,
            "is_deleted": self.is_deleted,
            "is_pinned": self.is_pinned,
            "is_reply": self.is_reply,
            "has_replies": self.has_replies,
            "reply_count": self.reply_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "edited_at": self.edited_at.isoformat() if self.edited_at else None
        }

class CommentReaction(Base):
    """Reações aos comentários (like, dislike, etc.)"""
    
    __tablename__ = "comment_reactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    comment_id = Column(UUID(as_uuid=True), ForeignKey("comments.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Tipo de reação
    reaction_type = Column(String(50), nullable=False)  # like, dislike, heart, laugh, etc.
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    comment = relationship("Comment")
    user = relationship("User")
    
    def __repr__(self):
        return f"<CommentReaction(id={self.id}, comment_id={self.comment_id}, user_id={self.user_id}, type='{self.reaction_type}')>"
    
    def to_dict(self) -> dict:
        """Converte reação para dicionário"""
        return {
            "id": str(self.id),
            "comment_id": str(self.comment_id),
            "user_id": str(self.user_id),
            "reaction_type": self.reaction_type,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class CommentEdit(Base):
    """Histórico de edições de comentários"""
    
    __tablename__ = "comment_edits"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    comment_id = Column(UUID(as_uuid=True), ForeignKey("comments.id"), nullable=False)
    edited_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Conteúdo anterior
    previous_content = Column(Text, nullable=False)
    previous_content_html = Column(Text, nullable=True)
    
    # Razão da edição
    edit_reason = Column(String(500), nullable=True)
    
    # Timestamps
    edited_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    comment = relationship("Comment")
    editor = relationship("User")
    
    def __repr__(self):
        return f"<CommentEdit(id={self.id}, comment_id={self.comment_id}, edited_by={self.edited_by})>"
    
    def to_dict(self) -> dict:
        """Converte edição para dicionário"""
        return {
            "id": str(self.id),
            "comment_id": str(self.comment_id),
            "edited_by": str(self.edited_by),
            "previous_content": self.previous_content,
            "previous_content_html": self.previous_content_html,
            "edit_reason": self.edit_reason,
            "edited_at": self.edited_at.isoformat() if self.edited_at else None
        }
