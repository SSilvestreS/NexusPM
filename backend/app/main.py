"""
Aplicação principal FastAPI
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import structlog
from datetime import datetime

from app.core.config import settings
from app.core.database import init_db, check_db_health
from app.api.v1.api import api_router
from app.websockets.manager import websocket_manager


# Configuração do logging estruturado
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciador de ciclo de vida da aplicação"""
    # Startup
    logger.info("Iniciando aplicação NexusPM", version=settings.app_version)
    
    # Inicializar banco de dados
    try:
        await init_db()
        logger.info("Banco de dados inicializado com sucesso")
    except Exception as e:
        logger.error("Erro ao inicializar banco de dados", error=str(e))
        raise
    
    # Verificar saúde do banco
    try:
        await check_db_health()
        logger.info("Banco de dados está saudável")
    except Exception as e:
        logger.error("Banco de dados não está saudável", error=str(e))
        raise
    
    yield
    
    # Shutdown
    logger.info("Encerrando aplicação NexusPM")


# Criação da aplicação FastAPI
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None
)

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Middleware de hosts confiáveis
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para logging de requisições"""
    start_time = datetime.utcnow()
    
    # Log da requisição
    logger.info(
        "Requisição recebida",
        method=request.method,
        url=str(request.url),
        client_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )
    
    # Processar requisição
    response = await call_next(request)
    
    # Calcular tempo de resposta
    process_time = (datetime.utcnow() - start_time).total_seconds()
    
    # Log da resposta
    logger.info(
        "Requisição processada",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        process_time=process_time
    )
    
    # Adicionar header de tempo de processamento
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


# Handlers de exceção
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handler para exceções HTTP do Starlette"""
    logger.warning(
        "Exceção HTTP",
        status_code=exc.status_code,
        detail=exc.detail,
        url=str(request.url)
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "status_code": exc.status_code,
            "detail": exc.detail,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler para erros de validação de requisição"""
    logger.warning(
        "Erro de validação de requisição",
        errors=exc.errors(),
        url=str(request.url)
    )
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "detail": "Dados de entrada inválidos",
            "errors": exc.errors(),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handler para exceções gerais"""
    logger.error(
        "Exceção não tratada",
        error=str(exc),
        error_type=type(exc).__name__,
        url=str(request.url),
        exc_info=True
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "Erro interno do servidor",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# Endpoints básicos
@app.get("/")
async def root():
    """Endpoint raiz da aplicação"""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "description": settings.app_description,
        "status": "running",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health")
async def health_check():
    """Endpoint de verificação de saúde da aplicação"""
    try:
        # Verificar banco de dados
        db_healthy = await check_db_health()
        
        # Verificar Redis (implementar quando tiver cliente Redis)
        redis_healthy = True
        
        # Verificar RabbitMQ (implementar quando tiver cliente RabbitMQ)
        rabbitmq_healthy = True
        
        overall_healthy = db_healthy and redis_healthy and rabbitmq_healthy
        
        return {
            "status": "healthy" if overall_healthy else "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "database": "healthy" if db_healthy else "unhealthy",
                "redis": "healthy" if redis_healthy else "unhealthy",
                "rabbitmq": "healthy" if rabbitmq_healthy else "unhealthy"
            },
            "version": settings.app_version
        }
        
    except Exception as e:
        logger.error("Erro na verificação de saúde", error=str(e))
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e),
                "version": settings.app_version
            }
        )


@app.get("/info")
async def app_info():
    """Endpoint com informações da aplicação"""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "description": settings.app_description,
        "environment": settings.environment,
        "debug": settings.debug,
        "features": {
            "graphql": settings.enable_graphql,
            "offline_mode": settings.enable_offline_mode,
            "plugins": settings.enable_plugins,
            "virtual_scrolling": True,
            "real_time": True,
            "collaborative_editing": True,
            "notifications": True,
            "file_upload": True,
            "search": True,
            "internationalization": True,
            "themes": True
        },
        "timestamp": datetime.utcnow().isoformat()
    }


# Endpoint WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket):
    """Endpoint WebSocket para comunicação em tempo real"""
    await websocket_manager.connect(websocket)


# Incluir router da API
app.include_router(api_router, prefix="/api/v1")


# Eventos de startup e shutdown
@app.on_event("startup")
async def startup_event():
    """Evento executado na inicialização da aplicação"""
    logger.info("Aplicação NexusPM iniciada com sucesso")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento executado no encerramento da aplicação"""
    logger.info("Aplicação NexusPM encerrada")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
