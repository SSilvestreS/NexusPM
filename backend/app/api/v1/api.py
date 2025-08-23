"""
API Router principal para versão 1
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, projects, tasks, comments, notifications, search, websockets, files

api_router = APIRouter()

# Incluir routers dos endpoints
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["autenticação"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["usuários"]
)

api_router.include_router(
    projects.router,
    prefix="/projects",
    tags=["projetos"]
)

api_router.include_router(
    tasks.router,
    prefix="/tasks",
    tags=["tarefas"]
)

api_router.include_router(
    comments.router,
    prefix="/comments",
    tags=["comentários"]
)

api_router.include_router(
    notifications.router,
    prefix="/notifications",
    tags=["notificações"]
)

api_router.include_router(
    search.router,
    prefix="/search",
    tags=["busca"]
)

api_router.include_router(
    websockets.router,
    prefix="/ws",
    tags=["websockets"]
)

api_router.include_router(
    files.router,
    prefix="/files",
    tags=["arquivos"]
)
