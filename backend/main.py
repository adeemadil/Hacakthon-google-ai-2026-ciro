import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config.settings import settings

# Configure logging formats
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("CIRO.Gateway")

# Lifespan context manager controlling background scheduler startup after database checks
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing SQLite Signal Store database and checking schemas...")
    # SQL DB migrations/tables would check here before background workers boot
    
    logger.info("Configuring background scheduler for periodic crisis checks...")
    scheduler = AsyncIOScheduler()
    
    async def scheduled_collector_job():
        logger.info("Triggering periodic multi-agent crisis evaluation cycle...")
        
    scheduler.add_job(
        scheduled_collector_job,
        trigger="interval",
        hours=settings.ORCHESTRATOR_INTERVAL_HOURS,
        id="orchestration_cycle_job",
        replace_existing=True
    )
    
    scheduler.start()
    logger.info(f"CIRO background scheduler booted successfully (interval: {settings.ORCHESTRATOR_INTERVAL_HOURS} hours).")
    
    yield
    
    logger.info("Deactivating CIRO background scheduler tasks...")
    scheduler.shutdown()
    logger.info("CIRO backend services stopped cleanly.")

app = FastAPI(
    title="CIRO — Crisis Intelligence & Response Orchestrator",
    description="Multi-Agent AI System for Urban Crisis Prediction & Response in Pakistan",
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan
)

# CORS Policy: Permissive credentials & origins configured for hackathon demo compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router includes (commented placeholders for now as requested)
# from agents import data_collector_router, predictor_router
# app.include_router(data_collector_router)
# app.include_router(predictor_router)

# Mount and locate static view components if they exist
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_control_room():
    """
    Serve the control room static dashboard.
    """
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r") as file:
            return HTMLResponse(content=file.read())
    return HTMLResponse(content="<h3>CIRO Control Room Online. Dashboard static page is missing.</h3>")

@app.get("/health")
async def health_check():
    """
    Standard health check endpoint reporting active prediction nodes.
    """
    return {
        "status": "ok",
        "agents": ["agent2", "agent3"]
    }

@app.websocket("/ws/signals")
async def websocket_signals(
    websocket: WebSocket,
    zone: str = Query(None, description="Monitored urban zone ID"),
    min_severity: str = Query("low", description="Minimum severity alert threshold")
):
    """
    Real-time signal feed gateway accepting zone and severity filters.
    """
    await websocket.accept()
    logger.info(f"WebSocket client connected: zone={zone}, min_severity={min_severity}")
    try:
        # Send initial filter settings back to the client
        await websocket.send_json({
            "connection": "established",
            "filter_zone": zone,
            "filter_min_severity": min_severity
        })
        while True:
            # Await client frames to keep session alive
            data = await websocket.receive_text()
            await websocket.send_json({
                "echo": data,
                "applied_zone": zone,
                "applied_min_severity": min_severity
            })
    except WebSocketDisconnect:
        logger.info("WebSocket client session disconnected.")
    except Exception as e:
        logger.error(f"WebSocket gateway exception: {e}")
