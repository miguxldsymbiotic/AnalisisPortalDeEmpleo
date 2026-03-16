import httpx
import asyncio

async def pause():
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post('http://localhost:8000/api/v1/scraper/cancelar')
            print(f"Status: {r.status_code}")
            print(f"Response: {r.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(pause())
