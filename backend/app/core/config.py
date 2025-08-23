"""
Configuration settings for Nova Pasta application
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Nova Pasta"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Security
    SECRET_KEY: str = "nova_pasta_secret_key_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = "postgresql://nova_user:nova_password@localhost:5432/nova_pasta"
    POSTGRES_DB: str = "nova_pasta"
    POSTGRES_USER: str = "nova_user"
    POSTGRES_PASSWORD: str = "nova_password"
    
    # Redis
    REDIS_URL: str = "redis://:nova_redis_password@localhost:6379/0"
    REDIS_PASSWORD: str = "nova_redis_password"
    
    # RabbitMQ
    RABBITMQ_URL: str = "amqp://nova_user:nova_password@localhost:5672/nova_pasta"
    CELERY_BROKER_URL: str = "amqp://nova_user:nova_password@localhost:5672/nova_pasta"
    CELERY_RESULT_BACKEND: str = "redis://:nova_redis_password@localhost:6379/0"
    
    # OAuth2
    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None
    GITLAB_CLIENT_ID: Optional[str] = None
    GITLAB_CLIENT_SECRET: Optional[str] = None
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # File Storage
    STORAGE_TYPE: str = "local"  # local, s3, azure
    STORAGE_PATH: str = "./uploads"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    AWS_BUCKET_NAME: str = "nova-pasta-uploads"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # WebSocket
    WS_MESSAGE_QUEUE_SIZE: int = 100
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Search
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    SEARCH_INDEX_PREFIX: str = "nova_pasta"
    
    # Cache
    CACHE_TTL: int = 300  # 5 minutes
    USER_CACHE_TTL: int = 3600  # 1 hour
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = [
        "image/jpeg", "image/png", "image/gif", "image/webp",
        "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain", "text/csv", "application/json"
    ]
    
    # Operational Transformation
    OT_HISTORY_SIZE: int = 100
    OT_SYNC_INTERVAL: int = 100  # milliseconds
    
    # Notifications
    NOTIFICATION_RETENTION_DAYS: int = 30
    PUSH_NOTIFICATION_ENABLED: bool = True
    
    # Monitoring
    METRICS_ENABLED: bool = True
    HEALTH_CHECK_INTERVAL: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Validate required settings in production
if settings.ENVIRONMENT == "production":
    if not settings.SECRET_KEY or settings.SECRET_KEY == "nova_pasta_secret_key_change_in_production":
        raise ValueError("SECRET_KEY must be set in production")
    
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        raise ValueError("SMTP credentials must be set in production")
