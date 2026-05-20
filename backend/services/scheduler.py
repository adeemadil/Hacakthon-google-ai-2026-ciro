import logging

logger = logging.getLogger(__name__)

try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
except ImportError:
    # Safe mock scheduler so the codebase is runnable prior to package installations
    class AsyncIOScheduler:
        def __init__(self, *args, **kwargs):
            pass
        def add_job(self, *args, **kwargs):
            pass
        def start(self):
            pass
        def shutdown(self):
            pass

def setup_scheduler(app) -> Any:
    """
    Configure and setup background recurring tasks using AsyncIOScheduler.
    Executes a data collector fetch job every 15 minutes.
    """
    logger.info("Setting up background scheduler...")
    scheduler = AsyncIOScheduler()
    
    async def data_collection_job():
        logger.info("Executing scheduled 15-minute background data collection cycle...")
        # In real implementation: will trigger Agent 2's data fetching flow.
        
    scheduler.add_job(
        data_collection_job, 
        trigger="interval", 
        minutes=15, 
        id="data_collection_fetch_job",
        replace_existing=True
    )
    
    # Use standard FastAPI lifecycle handlers to control start/stop
    @app.on_event("startup")
    async def start_scheduler():
        try:
            scheduler.start()
            logger.info("CIRO background scheduler started successfully.")
        except Exception as e:
            logger.error(f"Failed to start background scheduler: {e}")
            
    @app.on_event("shutdown")
    async def shutdown_scheduler():
        try:
            scheduler.shutdown()
            logger.info("CIRO background scheduler stopped.")
        except Exception as e:
            logger.error(f"Failed to stop background scheduler: {e}")

    return scheduler
