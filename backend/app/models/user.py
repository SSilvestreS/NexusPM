"""
User model for authentication and profile management
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from passlib.hash import bcrypt

from app.core.database import Base

class User(Base):
    """User model for authentication and profile"""
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Authentication fields
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)  # Nullable for OAuth users
    
    # Profile fields
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    location = Column(String(200), nullable=True)
    website = Column(String(500), nullable=True)
    
    # OAuth fields
    oauth_provider = Column(String(50), nullable=True)  # github, gitlab, google
    oauth_id = Column(String(255), nullable=True)
    oauth_access_token = Column(String(500), nullable=True)
    oauth_refresh_token = Column(String(500), nullable=True)
    
    # Status fields
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    
    # Preferences
    preferences = Column(JSON, default={})
    language = Column(String(10), default="pt-BR")
    timezone = Column(String(50), default="America/Sao_Paulo")
    theme = Column(String(20), default="light")  # light, dark, auto
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    project_memberships = relationship("ProjectMember", back_populates="user", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="assignee", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.username
    
    @property
    def display_name(self) -> str:
        """Get user's display name (full name or username)"""
        return self.full_name if self.full_name != self.username else self.username
    
    def set_password(self, password: str):
        """Hash and set user password"""
        self.hashed_password = bcrypt.hash(password)
    
    def verify_password(self, password: str) -> bool:
        """Verify user password"""
        if not self.hashed_password:
            return False
        return bcrypt.verify(password, self.hashed_password)
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
    
    def to_dict(self, include_sensitive: bool = False) -> dict:
        """Convert user to dictionary"""
        data = {
            "id": str(self.id),
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "avatar_url": self.avatar_url,
            "bio": self.bio,
            "location": self.location,
            "website": self.website,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "language": self.language,
            "timezone": self.timezone,
            "theme": self.theme,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None
        }
        
        if include_sensitive:
            data.update({
                "oauth_provider": self.oauth_provider,
                "is_superuser": self.is_superuser,
                "preferences": self.preferences
            })
        
        return data

class UserSession(Base):
    """User session management for JWT tokens"""
    
    __tablename__ = "user_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    token_id = Column(String(255), unique=True, index=True, nullable=False)
    refresh_token = Column(String(500), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)
    ip_address = Column(String(45), nullable=True)  # IPv6 support
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    
    def __repr__(self):
        return f"<UserSession(id={self.id}, user_id={self.user_id}, expires_at={self.expires_at})>"
    
    def is_expired(self) -> bool:
        """Check if session is expired"""
        return datetime.utcnow() > self.expires_at
    
    def to_dict(self) -> dict:
        """Convert session to dictionary"""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "token_id": self.token_id,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_active": self.is_active,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class UserPreference(Base):
    """User preferences and settings"""
    
    __tablename__ = "user_preferences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category = Column(String(100), nullable=False)  # notifications, ui, privacy, etc.
    key = Column(String(100), nullable=False)
    value = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<UserPreference(id={self.id}, user_id={self.user_id}, category='{self.category}', key='{self.key}')>"
    
    def to_dict(self) -> dict:
        """Convert preference to dictionary"""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "category": self.category,
            "key": self.key,
            "value": self.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
