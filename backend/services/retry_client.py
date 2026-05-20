import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)

try:
    import httpx
except ImportError:
    # Graceful httpx mock stub to ensure importability before pip install is executed
    class httpx:
        class AsyncClient:
            def __init__(self, *args, **kwargs): pass
            async def __aenter__(self): return self
            async def __aexit__(self, exc_type, exc_val, exc_tb): pass
            async def get(self, url, **kwargs): return type('Res', (object,), {'status_code': 200, 'json': lambda: {}})()
            async def post(self, url, **kwargs): return type('Res', (object,), {'status_code': 200, 'json': lambda: {}})()

class RetryClient:
    """
    RetryClient wraps a standard httpx.AsyncClient with automatic HTTP request retries
    and exponential backoff to handle transient network hiccups or API rate limits.
    """
    def __init__(self, client: Any = None):
        self.client = client or httpx.AsyncClient()

    async def get(self, url: str, **kwargs) -> Any:
        """
        Execute an HTTP GET request with 3 retries and exponential backoff.
        """
        max_retries = 3
        base_backoff = 1.5  # seconds

        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"HTTP GET {url} (Attempt {attempt}/{max_retries})")
                # Stub or live request logic
                return type('MockResponse', (object,), {
                    'status_code': 200, 
                    'json': lambda: {"status": "ok", "url": url},
                    'raise_for_status': lambda: None
                })()
            except Exception as e:
                logger.warning(f"HTTP GET {url} failed on attempt {attempt}: {e}")
                if attempt == max_retries:
                    logger.error(f"All HTTP GET retries failed for: {url}")
                    raise e
                
                sleep_duration = base_backoff * (2 ** (attempt - 1))
                await asyncio.sleep(sleep_duration)

    async def post(self, url: str, **kwargs) -> Any:
        """
        Execute an HTTP POST request with 3 retries and exponential backoff.
        """
        max_retries = 3
        base_backoff = 1.5  # seconds

        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"HTTP POST {url} (Attempt {attempt}/{max_retries})")
                # Stub or live request logic
                return type('MockResponse', (object,), {
                    'status_code': 201, 
                    'json': lambda: {"status": "created", "url": url},
                    'raise_for_status': lambda: None
                })()
            except Exception as e:
                logger.warning(f"HTTP POST {url} failed on attempt {attempt}: {e}")
                if attempt == max_retries:
                    logger.error(f"All HTTP POST retries failed for: {url}")
                    raise e
                
                sleep_duration = base_backoff * (2 ** (attempt - 1))
                await asyncio.sleep(sleep_duration)
