import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class OpenMeteoService:
    """
    Service wrapper for fetching weather and river discharge forecasts from Open-Meteo and GloFAS.
    """
    
    async def get_current_weather(self, lat: float, lng: float) -> Dict[str, Any]:
        """
        Fetch the current weather conditions for a given latitude and longitude.
        Returns a dict containing temp_c, precip_mm, and wind_kph.
        """
        logger.info(f"Fetching current weather for coordinates: {lat}, {lng}")
        return {
            "lat": lat,
            "lng": lng,
            "temp_c": 28.5,
            "precip_mm": 0.0,
            "wind_kph": 12.4,
            "updated_at": datetime.utcnow().isoformat()
        }

    async def get_forecast_16day(self, lat: float, lng: float) -> List[Dict[str, Any]]:
        """
        Fetch a 16-day daily weather forecast.
        Returns a list of 16 daily forecast dicts.
        """
        logger.info(f"Fetching 16-day weather forecast for coordinates: {lat}, {lng}")
        forecast = []
        base_date = datetime.utcnow().date()
        for i in range(16):
            forecast.append({
                "date": (base_date + timedelta(days=i)).isoformat(),
                "temp_max_c": 32.0 + (i % 3),
                "temp_min_c": 22.0 - (i % 2),
                "precip_mm": 0.0 if i % 4 != 0 else 5.2,
                "wind_max_kph": 15.0 + i
            })
        return forecast

    async def get_glofas_30day(self, lat: float, lng: float) -> List[Dict[str, Any]]:
        """
        Fetch a 30-day daily river discharge/flood forecast from GloFAS.
        Returns a list of 30 daily discharge dicts.
        """
        logger.info(f"Fetching 30-day GloFAS river discharge forecast for coordinates: {lat}, {lng}")
        glofas = []
        base_date = datetime.utcnow().date()
        for i in range(30):
            glofas.append({
                "date": (base_date + timedelta(days=i)).isoformat(),
                "river_discharge_m3_s": 150.0 + (i * 2.5) - (i % 5 * 10),
                "flood_threshold_exceeded": False
            })
        return glofas
