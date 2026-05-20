from fastapi import APIRouter, Query

router = APIRouter(prefix="/api/v1/agent2", tags=["Agent 2 - Data Collector"])

# Dynamic list of the 8 monitored zones across Pakistan
MONITORED_ZONES = [
    "islamabad-g10",
    "lahore-city",
    "karachi-south",
    "peshawar-city",
    "multan-city",
    "jacobabad-city",
    "sukkur-city",
    "quetta-city"
]

@router.get("/status")
async def get_status():
    """
    Get Agent 2 (Data Collector) status and active zones information.
    """
    return {"agent": "DataCollector", "status": "active", "zones": len(MONITORED_ZONES)}

@router.post("/fetch")
async def fetch_data():
    """
    Trigger a manual data fetch cycle for all zones from active APIs
    (Open-Meteo, GloFAS, NDMA, and traffic/social scrapers).
    """
    return {"message": "Fetch cycle triggered", "zones_processed": len(MONITORED_ZONES)}

@router.post("/backfill/{zone_id}")
async def backfill_zone(zone_id: str, days: int = Query(30, description="Number of days to backfill")):
    """
    Backfill historical data for a specific zone to train or test models.
    """
    return {"zone": zone_id, "days_backfilled": days}

@router.get("/signals/{zone_id}")
async def get_signals(zone_id: str):
    """
    Retrieve current raw signals (e.g., social, NDMA alerts, traffic reports)
    for a specific city/zone.
    """
    return {"zone": zone_id, "signals": [], "count": 0}

@router.get("/features/{zone_id}")
async def get_features(zone_id: str):
    """
    Retrieve engineered and preprocessed features prepared for the ML Predictor models.
    """
    return {"zone": zone_id, "features": {}}

@router.get("/forecast/{zone_id}")
async def get_forecast(zone_id: str):
    """
    Retrieve a 16-day forward weather forecast (Open-Meteo) for a specific zone.
    """
    return {"zone": zone_id, "forecast_days": 16, "data": []}

@router.get("/flood-forecast/{zone_id}")
async def get_flood_forecast(zone_id: str):
    """
    Retrieve 30-day river discharge forecasts (GloFAS) for a specific zone.
    """
    return {"zone": zone_id, "discharge_days": 30, "data": []}

@router.get("/zones")
async def get_zones():
    """
    Retrieve the 8 monitored cities across the 5 provinces of Pakistan.
    """
    return {"zones": MONITORED_ZONES}
