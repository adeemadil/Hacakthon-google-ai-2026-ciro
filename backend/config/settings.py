import os
from dotenv import load_dotenv

# Load active environment configurations
load_dotenv()

class Settings:
    """
    CIRO Application Settings managing API keys and server controls
    populated from local environment variables.
    """
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    EE_PROJECT_ID: str = os.getenv("EE_PROJECT_ID", "")
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
    NDMA_API_KEY: str = os.getenv("NDMA_API_KEY", "")
    FLOODHUB_API_KEY: str = os.getenv("FLOODHUB_API_KEY", "")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()
