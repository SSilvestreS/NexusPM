"""
Roteador principal da API v1
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, projects, tasks, comments, notifications, search, websockets

# Cria o roteador principal da API
api_router = APIRouter()

# Inclui os roteadores de cada módulo
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Autenticação"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Usuários"]
)

api_router.include_router(
    projects.router,
    prefix="/projects",
    tags=["Projetos"]
)

api_router.include_router(
    tasks.router,
    prefix="/tasks",
    tags=["Tarefas"]
)

api_router.include_router(
    comments.router,
    prefix="/comments",
    tags=["Comentários"]
)

api_router.include_router(
    notifications.router,
    prefix="/notifications",
    tags=["Notificações"]
)

api_router.include_router(
    search.router,
    prefix="/search",
    tags=["Busca"]
)

api_router.include_router(
    websockets.router,
    prefix="/ws",
    tags=["WebSockets"]
)
