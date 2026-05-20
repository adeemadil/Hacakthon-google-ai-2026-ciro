import asyncio
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class GeminiRetryClient:
    """
    GeminiRetryClient wraps interactions with the Gemini API to provide robust retry logic
    and exponential backoff when encountering transient errors or rate limits.
    """

    async def generate(self, prompt: str, model: str = "gemini-2.0-flash") -> Optional[str]:
        """
        Generate content using Gemini model with up to 3 retries and exponential backoff.
        """
        max_retries = 3
        base_backoff = 2.0  # seconds

        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"Gemini API Request (model: {model}, attempt {attempt}/{max_retries})...")
                # Stub behavior. Under active implementation this would call the google-genai or google-generativeai SDK.
                return f"[Mock Gemini Response] Evaluated proposal. Confidence is high. Prompt starts with: '{prompt[:40]}...'"
            except Exception as e:
                logger.warning(f"Gemini API attempt {attempt} failed with error: {e}")
                if attempt == max_retries:
                    logger.error("All Gemini API retry attempts exhausted.")
                    raise e
                
                # Exponential backoff: 2s, 4s, 8s...
                sleep_duration = base_backoff * (2 ** (attempt - 1))
                logger.info(f"Backing off for {sleep_duration} seconds before retry.")
                await asyncio.sleep(sleep_duration)
                
        return None
