import httpx
import asyncio
import json

async def check():
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get('http://localhost:8000/api/v1/scraper/sesiones')
            data = r.json()
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check())
