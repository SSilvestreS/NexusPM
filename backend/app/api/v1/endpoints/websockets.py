"""
Endpoints para WebSockets e comunicação em tempo real
"""
from typing import Dict, Set, Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json
import logging

from app.core.database import get_async_db
from app.core.security import get_current_user_from_token
from app.models.user import User
from app.models.project import ProjectMember
from app.core.websocket import websocket_manager

router = APIRouter()
logger = logging.getLogger(__name__)

# Esquema de autenticação para WebSocket
security = HTTPBearer()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int,
    token: str = None
):
    """
    Endpoint WebSocket para comunicação em tempo real
    """
    await websocket.accept()
    
    try:
        # Autenticar usuário via token
        if not token:
            # Tentar obter token do header ou query parameter
            token = websocket.headers.get("authorization", "").replace("Bearer ", "")
            if not token:
                token = websocket.query_params.get("token")
        
        if not token:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": "Token de autenticação não fornecido"
            }))
            await websocket.close()
            return
        
        # Verificar token e obter usuário
        try:
            user = await get_current_user_from_token(token)
            if user.id != user_id:
                raise HTTPException(status_code=403, detail="Acesso negado")
        except Exception as e:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": "Token inválido ou expirado"
            }))
            await websocket.close()
            return
        
        # Registrar conexão WebSocket
        await websocket_manager.connect(websocket, user.id)
        
        # Enviar mensagem de confirmação
        await websocket.send_text(json.dumps({
            "type": "connection_established",
            "user_id": user.id,
            "message": "Conexão WebSocket estabelecida com sucesso"
        }))
        
        # Enviar notificações pendentes
        pending_notifications = await websocket_manager.get_pending_notifications(user.id)
        for notification in pending_notifications:
            await websocket.send_text(json.dumps({
                "type": "notification",
                "data": notification
            }))
        
        # Loop principal para receber mensagens
        while True:
            try:
                # Receber mensagem do cliente
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Processar mensagem baseada no tipo
                await process_websocket_message(websocket, user, message)
                
            except WebSocketDisconnect:
                logger.info(f"WebSocket desconectado para usuário {user.id}")
                break
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Formato de mensagem inválido"
                }))
            except Exception as e:
                logger.error(f"Erro ao processar mensagem WebSocket: {str(e)}")
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Erro interno do servidor"
                }))
    
    except Exception as e:
        logger.error(f"Erro na conexão WebSocket: {str(e)}")
        try:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": "Erro na conexão"
            }))
        except:
            pass
        await websocket.close()
    
    finally:
        # Desconectar usuário
        await websocket_manager.disconnect(user.id)


async def process_websocket_message(websocket: WebSocket, user: User, message: dict):
    """
    Processar mensagem recebida via WebSocket
    """
    message_type = message.get("type")
    
    if message_type == "join_project":
        # Usuário quer receber atualizações de um projeto específico
        project_id = message.get("project_id")
        if project_id:
            # Verificar se o usuário é membro do projeto
            db = await get_async_db()
            member = await db.execute(
                select(ProjectMember).where(
                    ProjectMember.project_id == project_id,
                    ProjectMember.user_id == user.id
                )
            )
            if member.scalar_one_or_none():
                await websocket_manager.join_project(user.id, project_id)
                await websocket.send_text(json.dumps({
                    "type": "project_joined",
                    "project_id": project_id,
                    "message": f"Entrou no projeto {project_id}"
                }))
            else:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Usuário não é membro do projeto"
                }))
    
    elif message_type == "leave_project":
        # Usuário quer sair das atualizações de um projeto
        project_id = message.get("project_id")
        if project_id:
            await websocket_manager.leave_project(user.id, project_id)
            await websocket.send_text(json.dumps({
                "type": "project_left",
                "project_id": project_id,
                "message": f"Saiu do projeto {project_id}"
            }))
    
    elif message_type == "ping":
        # Responder ao ping do cliente
        await websocket.send_text(json.dumps({
            "type": "pong",
            "timestamp": message.get("timestamp")
        }))
    
    elif message_type == "get_status":
        # Enviar status atual da conexão
        user_projects = await websocket_manager.get_user_projects(user.id)
        await websocket.send_text(json.dumps({
            "type": "status",
            "user_id": user.id,
            "connected_projects": user_projects,
            "connection_status": "active"
        }))
    
    else:
        # Mensagem de tipo desconhecido
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": f"Tipo de mensagem desconhecido: {message_type}"
        }))


@router.get("/ws/status/{user_id}")
async def get_websocket_status(
    user_id: int,
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Obter status da conexão WebSocket de um usuário
    """
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado"
        )
    
    is_connected = websocket_manager.is_user_connected(user_id)
    connected_projects = await websocket_manager.get_user_projects(user_id)
    
    return {
        "user_id": user_id,
        "is_connected": is_connected,
        "connected_projects": connected_projects,
        "last_seen": websocket_manager.get_user_last_seen(user_id)
    }


@router.post("/ws/broadcast")
async def broadcast_message(
    message: dict,
    project_id: Optional[int] = None,
    user_ids: Optional[list] = None,
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Enviar mensagem broadcast via WebSocket (apenas para superusuários)
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas superusuários podem enviar mensagens broadcast"
        )
    
    if project_id:
        # Broadcast para projeto específico
        await websocket_manager.broadcast_to_project(project_id, message)
        return {"message": f"Mensagem enviada para projeto {project_id}"}
    
    elif user_ids:
        # Broadcast para usuários específicos
        for user_id in user_ids:
            await websocket_manager.send_to_user(user_id, message)
        return {"message": f"Mensagem enviada para {len(user_ids)} usuários"}
    
    else:
        # Broadcast global
        await websocket_manager.broadcast_to_all(message)
        return {"message": "Mensagem enviada para todos os usuários"}


@router.get("/ws/connections")
async def get_active_connections(
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Obter lista de conexões WebSocket ativas (apenas para superusuários)
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas superusuários podem ver conexões ativas"
        )
    
    active_connections = websocket_manager.get_active_connections()
    return {
        "total_connections": len(active_connections),
        "connections": active_connections
    }
