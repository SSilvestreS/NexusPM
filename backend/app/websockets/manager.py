"""
WebSocket manager for real-time communication
"""

import json
import asyncio
from typing import Dict, List, Set, Optional, Any
from fastapi import WebSocket, WebSocketDisconnect
import structlog
from datetime import datetime

logger = structlog.get_logger()

class ConnectionManager:
    """Manages WebSocket connections and broadcasting"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_rooms: Dict[str, Set[str]] = {}  # user_id -> set of room_ids
        self.room_connections: Dict[str, Set[str]] = {}  # room_id -> set of user_ids
        self.message_queue: asyncio.Queue = asyncio.Queue(maxsize=1000)
        
    async def connect(self, websocket: WebSocket, user_id: str = None):
        """Connect a new WebSocket client"""
        await websocket.accept()
        
        if user_id:
            self.active_connections[user_id] = websocket
            self.user_rooms[user_id] = set()
            logger.info("User connected", user_id=user_id)
        else:
            # Anonymous connection
            connection_id = f"anon_{len(self.active_connections)}"
            self.active_connections[connection_id] = websocket
            logger.info("Anonymous user connected", connection_id=connection_id)
    
    async def disconnect(self, websocket: WebSocket, user_id: str = None):
        """Disconnect a WebSocket client"""
        if user_id and user_id in self.active_connections:
            # Remove from all rooms
            if user_id in self.user_rooms:
                for room_id in self.user_rooms[user_id]:
                    if room_id in self.room_connections:
                        self.room_connections[room_id].discard(user_id)
                        if not self.room_connections[room_id]:
                            del self.room_connections[room_id]
                del self.user_rooms[user_id]
            
            del self.active_connections[user_id]
            logger.info("User disconnected", user_id=user_id)
        else:
            # Find and remove anonymous connection
            for conn_id, conn in self.active_connections.items():
                if conn == websocket:
                    del self.active_connections[conn_id]
                    logger.info("Anonymous user disconnected", connection_id=conn_id)
                    break
    
    async def join_room(self, user_id: str, room_id: str):
        """Add user to a room"""
        if user_id not in self.user_rooms:
            self.user_rooms[user_id] = set()
        
        self.user_rooms[user_id].add(room_id)
        
        if room_id not in self.room_connections:
            self.room_connections[room_id] = set()
        
        self.room_connections[room_id].add(user_id)
        logger.info("User joined room", user_id=user_id, room_id=room_id)
    
    async def leave_room(self, user_id: str, room_id: str):
        """Remove user from a room"""
        if user_id in self.user_rooms:
            self.user_rooms[user_id].discard(room_id)
        
        if room_id in self.room_connections:
            self.room_connections[room_id].discard(user_id)
            if not self.room_connections[room_id]:
                del self.room_connections[room_id]
        
        logger.info("User left room", user_id=user_id, room_id=room_id)
    
    async def send_personal_message(self, message: str, user_id: str):
        """Send message to specific user"""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(message)
                logger.debug("Personal message sent", user_id=user_id)
            except Exception as e:
                logger.error("Failed to send personal message", user_id=user_id, error=str(e))
                await self.disconnect(self.active_connections[user_id], user_id)
    
    async def broadcast_to_room(self, message: str, room_id: str, exclude_user: str = None):
        """Broadcast message to all users in a room"""
        if room_id in self.room_connections:
            disconnected_users = set()
            
            for user_id in self.room_connections[room_id]:
                if user_id != exclude_user and user_id in self.active_connections:
                    try:
                        await self.active_connections[user_id].send_text(message)
                    except Exception as e:
                        logger.error("Failed to send room message", user_id=user_id, room_id=room_id, error=str(e))
                        disconnected_users.add(user_id)
            
            # Remove disconnected users
            for user_id in disconnected_users:
                await self.disconnect(self.active_connections[user_id], user_id)
            
            logger.debug("Room message broadcasted", room_id=room_id, recipients=len(self.room_connections[room_id]))
    
    async def broadcast(self, message: str):
        """Broadcast message to all connected users"""
        disconnected_users = set()
        
        for user_id, connection in self.active_connections.items():
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error("Failed to broadcast message", user_id=user_id, error=str(e))
                disconnected_users.add(user_id)
        
        # Remove disconnected users
        for user_id in disconnected_users:
            await self.disconnect(self.active_connections[user_id], user_id)
        
        logger.debug("Message broadcasted to all users", total_users=len(self.active_connections))
    
    async def send_notification(self, user_id: str, notification: Dict[str, Any]):
        """Send notification to specific user"""
        message = {
            "type": "notification",
            "data": notification,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.send_personal_message(json.dumps(message), user_id)
    
    async def send_project_update(self, room_id: str, update: Dict[str, Any], exclude_user: str = None):
        """Send project update to room"""
        message = {
            "type": "project_update",
            "data": update,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast_to_room(json.dumps(message), room_id, exclude_user)
    
    async def send_comment_update(self, room_id: str, comment: Dict[str, Any], exclude_user: str = None):
        """Send comment update to room"""
        message = {
            "type": "comment_update",
            "data": comment,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast_to_room(json.dumps(message), room_id, exclude_user)
    
    async def send_user_activity(self, room_id: str, user_id: str, activity: str):
        """Send user activity to room"""
        message = {
            "type": "user_activity",
            "data": {
                "user_id": user_id,
                "activity": activity,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        await self.broadcast_to_room(json.dumps(message), room_id, user_id)
    
    def get_connection_count(self) -> int:
        """Get total number of active connections"""
        return len(self.active_connections)
    
    def get_room_users(self, room_id: str) -> Set[str]:
        """Get users in a specific room"""
        return self.room_connections.get(room_id, set())
    
    def get_user_rooms(self, user_id: str) -> Set[str]:
        """Get rooms for a specific user"""
        return self.user_rooms.get(user_id, set())

# Global WebSocket manager instance
websocket_manager = ConnectionManager()

# WebSocket message handlers
async def handle_websocket_message(websocket: WebSocket, message: str, user_id: str = None):
    """Handle incoming WebSocket messages"""
    try:
        data = json.loads(message)
        message_type = data.get("type")
        
        if message_type == "join_room":
            room_id = data.get("room_id")
            if room_id and user_id:
                await websocket_manager.join_room(user_id, room_id)
                await websocket_manager.send_personal_message(
                    json.dumps({"type": "room_joined", "room_id": room_id}),
                    user_id
                )
        
        elif message_type == "leave_room":
            room_id = data.get("room_id")
            if room_id and user_id:
                await websocket_manager.leave_room(user_id, room_id)
                await websocket_manager.send_personal_message(
                    json.dumps({"type": "room_left", "room_id": room_id}),
                    user_id
                )
        
        elif message_type == "ping":
            await websocket_manager.send_personal_message(
                json.dumps({"type": "pong", "timestamp": datetime.utcnow().isoformat()}),
                user_id
            )
        
        else:
            logger.warning("Unknown message type", message_type=message_type, user_id=user_id)
    
    except json.JSONDecodeError:
        logger.error("Invalid JSON message", user_id=user_id)
    except Exception as e:
        logger.error("Error handling WebSocket message", error=str(e), user_id=user_id)
