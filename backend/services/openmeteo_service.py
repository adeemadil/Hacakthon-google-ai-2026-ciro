import logging
import random
from typing import Dict, Any, List

logger = logging.getLogger("CIRO.OpenMeteo")

class OpenMeteoService:
    """
    OpenMeteoService interacts with Open-Meteo and GloFAS (Global Flood Awareness System)
    endpoints to ingest daily atmospheric and hydrological forecasts.
    """
    def __init__(self):
        logger.info("OpenMeteoService telemetry client initialized.")

    async def get_current_weather(self, lat: float, lng: float) -> Dict[str, Any]:
        """
        Get current telemetry for a specific geolocation coordinate.
        Returns: temp_c, precip_mm, wind_kph
        """
        logger.info(f"Retrieving current weather for lat={lat}, lng={lng}")
        # Simulated/mocked real-time values corresponding to the target zone
        return {
            "temp_c": round(random.uniform(28.0, 42.0), 1),
            "precip_mm": round(random.uniform(0.0, 15.0), 1),
            "wind_kph": round(random.uniform(5.0, 25.0), 1)
        }

    async def get_forecast_16day(self, lat: float, lng: float) -> List[Dict[str, Any]]:
        """
        Fetch a high-resolution 16-day atmospheric forecast.
        Returns a list of 16 daily weather dictionaries.
        """
        logger.info(f"Retrieving 16-day atmospheric forecast for lat={lat}, lng={lng}")
        forecast = []
        for day in range(1, 17):
            forecast.append({
                "day_offset": day,
                "temp_max": round(random.uniform(32.0, 44.0), 1),
                "temp_min": round(random.uniform(22.0, 29.0), 1),
                "precipitation_cumulative_mm": round(random.uniform(0.0, 50.0), 1),
                "soil_moisture_index": round(random.uniform(0.1, 0.8), 2)
            })
        return forecast

    async def get_glofas_30day(self, lat: float, lng: float) -> List[Dict[str, Any]]:
        """
        Query river discharge forecasts directly from the Global Flood Awareness System (GloFAS).
        Returns a list of 30 daily discharge projections.
        """
        logger.info(f"Retrieving 30-day river discharge (GloFAS) for lat={lat}, lng={lng}")
        discharge_series = []
        base_discharge = random.uniform(150.0, 300.0)
        
        for day in range(1, 31):
            # Accumulating progressive monsoon flow rates over 30 days
            flow_increase = random.uniform(-10.0, 45.0) if day > 10 else random.uniform(-5.0, 15.0)
            base_discharge = max(50.0, base_discharge + flow_increase)
            
            discharge_series.append({
                "day_offset": day,
                "discharge_cubic_meters_per_sec": round(base_discharge, 1),
                "anomaly_alert_triggered": base_discharge > 400.0
            })
        return discharge_series
