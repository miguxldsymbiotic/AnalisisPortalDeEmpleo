import httpx
import asyncio
import json

async def check():
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get('http://localhost:8000/api/v1/scraper/estado')
            if r.status_code == 200:
                print(json.dumps(r.json(), indent=2))
            else:
                print(f"Error: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check())
