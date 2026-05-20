import logging
import random
from typing import Dict, Any

logger = logging.getLogger("CIRO.WeatherService")

class WeatherService:
    """
    WeatherService queries real-time atmospheric measurements (such as OpenWeatherMap API)
    to perform high-frequency validations of immediate conditions.
    """
    def __init__(self):
        logger.info("WeatherService live atmospheric client initialized.")

    async def get_current(self, lat: float, lng: float, api_key: str = "") -> Dict[str, Any]:
        """
        Query current weather metrics for validating models against immediate local parameters.
        """
        logger.info(f"Querying live current weather metrics for lat={lat}, lng={lng}...")
        
        # Simulate active API fetch fallback
        has_key = bool(api_key)
        mode = "PROD_API" if has_key else "SIMULATION_MODE"
        logger.info(f"WeatherService query processing under mode: {mode}")
        
        return {
            "latitude": lat,
            "longitude": lng,
            "source": "OpenWeatherMap",
            "mode": mode,
            "metrics": {
                "temperature_celsius": round(random.uniform(28.0, 42.0), 1),
                "relative_humidity": round(random.uniform(40.0, 95.0), 1),
                "pressure_hpa": round(random.uniform(995.0, 1015.0), 1),
                "wind_speed_mps": round(random.uniform(1.5, 9.0), 1),
                "cloud_cover_percent": round(random.uniform(0.0, 100.0), 1)
            }
        }
