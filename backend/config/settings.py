import os
import logging
from typing import Dict, Tuple
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger("CIRO.Config")

class Settings(BaseSettings):
    """
    CIRO Application Settings managing API keys, intervals,
    and server control values parsed from the environment.
    """
    GEMINI_API_KEY: str = ""
    EE_PROJECT_ID: str = ""
    OPENWEATHER_API_KEY: str = ""
    GOOGLE_MAPS_API_KEY: str = ""
    NDMA_API_KEY: str = ""
    FLOODHUB_API_KEY: str = ""
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    RISK_ALERT_THRESHOLD: float = 0.30
    ORCHESTRATOR_INTERVAL_HOURS: int = 2

    # Pydantic v2 configuration to read from local environment
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Static dictionary mapping the 8 targeted Pakistani cities to their respective coordinates
ZONES: Dict[str, Tuple[float, float]] = {
    "islamabad-g10": (33.68, 73.05),
    "lahore-city": (31.52, 74.36),
    "karachi-south": (24.86, 67.00),
    "peshawar-city": (34.02, 71.52),
    "multan-city": (30.16, 71.52),
    "jacobabad-city": (28.28, 68.44),
    "sukkur-city": (27.71, 68.86),
    "quetta-city": (30.18, 66.98),
}

settings = Settings()

# Validate API keys and warn about fallbacks at startup
missing_keys = []
for key in ["GEMINI_API_KEY", "EE_PROJECT_ID", "OPENWEATHER_API_KEY", "GOOGLE_MAPS_API_KEY", "NDMA_API_KEY", "FLOODHUB_API_KEY"]:
    if not getattr(settings, key):
        missing_keys.append(key)

if missing_keys:
    print(f"\n[WARNING] Missing credentials in environment: {', '.join(missing_keys)}")
    print("CIRO will gracefully fall back to simulation/mock data for these modules.\n")
