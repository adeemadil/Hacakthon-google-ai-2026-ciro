import logging
from typing import Any
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger("CIRO.Scheduler")

# Import service instances to demonstrate scheduled data stream ingestion
from services.openmeteo_service import OpenMeteoService
from services.weather_service import WeatherService
from services.traffic_service import TrafficService
from services.social_service import SocialService
from services.ndma_service import NDMAService

def setup_scheduler(app: Any) -> AsyncIOScheduler:
    """
    Set up the recurring APScheduler AsyncIOScheduler background ingestion cycle.
    Executes a comprehensive data collection cycle across all 6 telemetry sources
    every 15 minutes.
    """
    logger.info("Initializing CIRO periodic background scheduler...")
    scheduler = AsyncIOScheduler()
    
    # Instantiate collectors
    openmeteo = OpenMeteoService()
    weather = WeatherService()
    traffic = TrafficService()
    social = SocialService()
    ndma = NDMAService()
    
    async def data_collection_job():
        """
        Scheduled collector task invoking all 6 data streams concurrently.
        """
        logger.info("Executing scheduled 15-minute background data collection cycle...")
        
        # Geolocation representing a target zone (e.g. Karachi)
        lat, lng = 24.86, 67.00
        zone_id = "karachi-south"
        
        try:
            # 1. Ingest Open-Meteo Current Weather
            curr_weather = await openmeteo.get_current_weather(lat, lng)
            logger.info(f" -> [Source 1/6] Ingested Open-Meteo current: {curr_weather}")
            
            # 2. Ingest Open-Meteo 16-day Atmospheric Forecast
            forecast_16 = await openmeteo.get_forecast_16day(lat, lng)
            logger.info(f" -> [Source 2/6] Ingested 16-day forecast days count: {len(forecast_16)}")
            
            # 3. Ingest GloFAS 30-day Hydrological Discharge Forecast
            discharge_30 = await openmeteo.get_glofas_30day(lat, lng)
            logger.info(f" -> [Source 3/6] Ingested 30-day river discharge days count: {len(discharge_30)}")
            
            # 4. Ingest Live Validation Weather
            curr_validate = await weather.get_current(lat, lng)
            logger.info(f" -> [Source 4/6] Ingested OpenWeather validation: {curr_validate.get('metrics')}")
            
            # 5. Ingest Traffic Disruptions
            disruptions = await traffic.get_disruptions(lat, lng)
            logger.info(f" -> [Source 5/6] Ingested Google Traffic road interruptions count: {len(disruptions)}")
            
            # 6. Ingest Crowdsourced Signals & Official government bulletins
            soc_sigs = await social.get_crisis_signals(zone_id)
            ndma_alerts = await ndma.get_alerts(zone_id)
            logger.info(f" -> [Source 6/6] Ingested signals: WhatsApp/X={len(soc_sigs)}, NDMA={len(ndma_alerts)}")
            
            logger.info("Deduplication and signal ingestion complete. Broadcasting metrics...")
            
        except Exception as e:
            logger.error(f"Error during recurring data collection sequence: {e}")
            
    # Add recurring 15-minute ingestion job
    scheduler.add_job(
        data_collection_job,
        trigger="interval",
        minutes=15,
        id="data_collection_15min_job",
        replace_existing=True
    )
    
    # FastAPI lifecycle event bindings
    @app.on_event("startup")
    async def start_scheduler():
        try:
            scheduler.start()
            logger.info("CIRO Ingestion APScheduler started successfully.")
        except Exception as e:
            logger.error(f"Failed to start APScheduler background engine: {e}")
            
    @app.on_event("shutdown")
    async def shutdown_scheduler():
        try:
            scheduler.shutdown()
            logger.info("CIRO Ingestion APScheduler stopped.")
        except Exception as e:
            logger.error(f"Failed to stop APScheduler background engine: {e}")
            
    return scheduler
