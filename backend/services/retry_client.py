import asyncio
import logging
import random
from typing import Any, Dict, Optional
import httpx

logger = logging.getLogger("CIRO.RetryClient")

class RetryClient:
    """
    RetryClient wraps httpx.AsyncClient with automated HTTP request retries
    and exponential backoff with jitter to survive transient network timeouts.
    """
    def __init__(self, client: Optional[httpx.AsyncClient] = None):
        self.client = client or httpx.AsyncClient()

    async def get(self, url: str, max_retries: int = 3, base_backoff: float = 1.5, **kwargs) -> httpx.Response:
        """
        Execute an HTTP GET request with exponential backoff and jitter.
        """
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"HTTP GET -> {url} (Attempt {attempt}/{max_retries})")
                response = await self.client.get(url, **kwargs)
                response.raise_for_status()
                return response
            except (httpx.HTTPError, Exception) as e:
                logger.warning(f"HTTP GET failed on attempt {attempt}: {e}")
                if attempt == max_retries:
                    logger.error(f"All HTTP GET retries exhausted for: {url}")
                    raise e
                
                # Exponential backoff with random jitter: (base * 2^(attempt-1)) + jitter
                sleep_duration = (base_backoff * (2 ** (attempt - 1))) + random.uniform(0.1, 0.5)
                await asyncio.sleep(sleep_duration)

    async def post(self, url: str, max_retries: int = 3, base_backoff: float = 1.5, **kwargs) -> httpx.Response:
        """
        Execute an HTTP POST request with exponential backoff and jitter.
        """
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"HTTP POST -> {url} (Attempt {attempt}/{max_retries})")
                response = await self.client.post(url, **kwargs)
                response.raise_for_status()
                return response
            except (httpx.HTTPError, Exception) as e:
                logger.warning(f"HTTP POST failed on attempt {attempt}: {e}")
                if attempt == max_retries:
                    logger.error(f"All HTTP POST retries exhausted for: {url}")
                    raise e
                
                sleep_duration = (base_backoff * (2 ** (attempt - 1))) + random.uniform(0.1, 0.5)
                await asyncio.sleep(sleep_duration)
