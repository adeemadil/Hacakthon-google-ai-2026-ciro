import logging
from typing import List, Any

logger = logging.getLogger(__name__)

# Graceful import of WebSocket from FastAPI
try:
    from fastapi import WebSocket
except ImportError:
    # Safe fallback stub for type hinting in environments where FastAPI is not yet installed
    class WebSocket:
        async def accept(self): pass
        async def send_json(self, data: Any): pass

class WebSocketManager:
    """
    WebSocketManager tracks active client connections (such as from the Flutter app)
    and handles real-time broadcasting of alerts and predictions.
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
        Accept and store a new active connection.
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New client connected. Active connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """
        Remove a disconnected client from the active registry.
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"Client disconnected. Active connections: {len(self.active_connections)}")

    async def broadcast(self, message: Any):
        """
        Broadcast a JSON-compatible dictionary to all active clients.
        """
        logger.info(f"Broadcasting message to {len(self.active_connections)} connected clients.")
        disconnected_clients = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client connection: {e}")
                disconnected_clients.append(connection)
                
        # Clean up stale connections
        for client in disconnected_clients:
            self.disconnect(client)
