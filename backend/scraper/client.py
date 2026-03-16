import httpx
import os
import asyncio
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

BASE_URL = "https://www.buscadordeempleo.gov.co/backbue/v1//vacantes/resultados"
RATE_LIMIT_RPS = int(os.getenv("SCRAPER_RATE_LIMIT_RPS", 5))
MAX_RETRIES = int(os.getenv("SCRAPER_MAX_RETRIES", 3))

class ScraperClient:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.semaphore = asyncio.Semaphore(1) # Secuencial según requerimientos
        self.delay_between_requests = 1.0 / RATE_LIMIT_RPS if RATE_LIMIT_RPS > 0 else 0

    async def fetch_page(self, page: int) -> dict:
        url = f"{BASE_URL}?page={page}"
        
        for attempt in range(MAX_RETRIES):
            try:
                async with self.semaphore:
                    response = await self.client.get(url)
                    response.raise_for_status()
                    await asyncio.sleep(self.delay_between_requests)
                    return response.json()
            except Exception as e:
                print(f"Error fetching page {page} attempt {attempt + 1}: {e}")
                if attempt == MAX_RETRIES - 1:
                    raise e
                await asyncio.sleep(2 ** (attempt + 1)) # Backoff exponencial 2s, 4s, 8s

        return {}

    async def close(self):
        await self.client.aclose()
