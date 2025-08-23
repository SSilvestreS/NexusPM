"""
Configurações da aplicação
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseSettings, validator
import os


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Configurações básicas da aplicação
    app_name: str = "NexusPM"
    app_version: str = "1.0.0"
    app_description: str = "Sistema de Gerenciamento de Projetos Colaborativos"
    debug: bool = False
    environment: str = "development"
    
    # Configurações de segurança
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Configurações do banco de dados
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/nexuspm"
    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "nexuspm"
    database_user: str = "postgres"
    database_password: str = "postgres"
    
    # Configurações do Redis
    redis_url: str = "redis://localhost:6379"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    
    # Configurações do RabbitMQ
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"
    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672
    rabbitmq_user: str = "guest"
    rabbitmq_password: str = "guest"
    rabbitmq_vhost: str = "/"
    
    # Configurações de CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    # Configurações de hosts permitidos
    allowed_hosts: List[str] = ["localhost", "127.0.0.1"]
    
    # Configurações de email
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_tls: bool = True
    smtp_ssl: bool = False
    
    # Configurações de armazenamento de arquivos
    file_storage_backend: str = "local"  # local, s3, azure
    file_storage_path: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: List[str] = ["jpg", "jpeg", "png", "gif", "pdf", "doc", "docx", "xls", "xlsx", "txt"]
    
    # Configurações de logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configurações de WebSocket
    websocket_ping_interval: int = 20
    websocket_ping_timeout: int = 20
    
    # Configurações de paginação
    default_page_size: int = 20
    max_page_size: int = 100
    
    # Configurações de busca
    search_index_path: str = "search_index"
    search_max_results: int = 1000
    
    # Configurações de cache
    cache_ttl: int = 3600  # 1 hora
    cache_max_size: int = 1000
    
    # Configurações de rate limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600  # 1 hora
    
    # Configurações de upload
    upload_chunk_size: int = 1024 * 1024  # 1MB
    upload_max_concurrent: int = 5
    
    # Configurações de operational transformation
    ot_max_operations: int = 1000
    ot_cleanup_interval: int = 3600  # 1 hora
    
    # Configurações de notificações
    notification_batch_size: int = 100
    notification_retry_attempts: int = 3
    notification_retry_delay: int = 300  # 5 minutos
    
    # Configurações de monitoramento
    enable_metrics: bool = True
    metrics_port: int = 8001
    health_check_interval: int = 30
    
    # Configurações de GraphQL
    enable_graphql: bool = True
    graphql_path: str = "/graphql"
    
    # Configurações de internacionalização
    default_language: str = "pt-BR"
    supported_languages: List[str] = ["pt-BR", "en-US", "es-ES"]
    
    # Configurações de tema
    default_theme: str = "light"
    available_themes: List[str] = ["light", "dark", "auto"]
    
    # Configurações de modo offline
    enable_offline_mode: bool = True
    offline_sync_interval: int = 300  # 5 minutos
    
    # Configurações de plugins
    enable_plugins: bool = True
    plugins_directory: str = "plugins"
    
    # Configurações de virtual scrolling
    virtual_scroll_page_size: int = 50
    virtual_scroll_buffer_size: int = 100
    
    # Configurações de integração externa
    github_webhook_secret: Optional[str] = None
    gitlab_webhook_secret: Optional[str] = None
    
    # Configurações de OAuth2
    oauth2_providers: Dict[str, Dict[str, str]] = {
        "github": {
            "client_id": "",
            "client_secret": "",
            "authorize_url": "https://github.com/login/oauth/authorize",
            "token_url": "https://github.com/login/oauth/access_token",
            "userinfo_url": "https://api.github.com/user"
        },
        "gitlab": {
            "client_id": "",
            "client_secret": "",
            "authorize_url": "https://gitlab.com/oauth/authorize",
            "token_url": "https://gitlab.com/oauth/token",
            "userinfo_url": "https://gitlab.com/api/v4/user"
        }
    }
    
    @validator('secret_key')
    def validate_secret_key(cls, v):
        """Valida se a chave secreta foi definida em produção"""
        if os.getenv('ENVIRONMENT') == 'production' and v == "your-secret-key-here":
            raise ValueError("SECRET_KEY deve ser definida em produção")
        return v
    
    @validator('smtp_host', 'smtp_user', 'smtp_password')
    def validate_smtp_settings(cls, v, values):
        """Valida se as configurações SMTP estão completas"""
        if any([values.get('smtp_host'), values.get('smtp_user'), values.get('smtp_password')]):
            if not all([values.get('smtp_host'), values.get('smtp_user'), values.get('smtp_password')]):
                raise ValueError("Todas as configurações SMTP devem ser fornecidas")
        return v
    
    @property
    def database_url(self) -> str:
        """Constrói a URL do banco de dados"""
        return f"postgresql+asyncpg://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"
    
    @property
    def redis_url(self) -> str:
        """Constrói a URL do Redis"""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    @property
    def rabbitmq_url(self) -> str:
        """Constrói a URL do RabbitMQ"""
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}/{self.rabbitmq_vhost}"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instância global das configurações
settings = Settings()
