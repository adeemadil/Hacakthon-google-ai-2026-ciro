import os
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from config.settings import settings
from agents import data_collector_router, predictor_router
from services.scheduler import setup_scheduler
from services.websocket_manager import WebSocketManager

# Configure logging formats
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("CIRO")

app = FastAPI(
    title="CIRO — Crisis Intelligence & Response Orchestrator",
    description="Multi-Agent AI System for Urban Crisis Prediction & Response in Pakistan",
    version="1.0.0",
    debug=settings.DEBUG
)

# Instantiate websocket registry
ws_manager = WebSocketManager()

# Register API Routers
app.include_router(data_collector_router)
app.include_router(predictor_router)

# Locate and serve Control Room static views
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_control_room():
    """
    Serve the control room dark-mode dashboard.
    """
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r") as file:
            return HTMLResponse(content=file.read())
    return HTMLResponse(content="<h3>CIRO Control Room online. Dashboards staging is missing.</h3>")

@app.websocket("/ws")
async def websocket_gateway(websocket: WebSocket):
    """
    WebSocket client interface handling real-time push streams.
    """
    await ws_manager.connect(websocket)
    try:
        while True:
            # Await client signals to keep connection frames open
            payload = await websocket.receive_text()
            await websocket.send_json({"echo": payload})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket session failure: {e}")
        ws_manager.disconnect(websocket)

# Start periodic data background collection cycles
setup_scheduler(app)

if __name__ == "__main__":
    import uvicorn
    logger.info(f"CIRO services booting on {settings.HOST}:{settings.PORT}...")
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
