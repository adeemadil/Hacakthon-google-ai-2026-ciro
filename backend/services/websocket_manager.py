import logging
from typing import List, Any
from fastapi import WebSocket

logger = logging.getLogger("CIRO.WebSocketManager")

class WebSocketManager:
    """
    WebSocketManager tracks, registers, and broadcasts real-time telemetry metrics
    and orchestrated crisis alerts to active frontend client connections.
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
        Accept and register a new active client connection.
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client registered. Active sessions: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """
        Deregister and clean up a disconnected client socket session.
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket client deregistered. Active sessions: {len(self.active_connections)}")

    async def broadcast(self, message: Any):
        """
        Broadcast a JSON-compatible alert payload to all registered web sockets.
        Automatically cleans up stale, broken client channels.
        """
        logger.info(f"Broadcasting websocket alert package to {len(self.active_connections)} clients...")
        stale_sessions = []
        
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"WebSocket transmission error to connection: {e}")
                stale_sessions.append(connection)
                
        # Purge dead sessions
        for session in stale_sessions:
            self.disconnect(session)
