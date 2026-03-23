import httpx
import asyncio
import json

async def check():
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get('http://localhost:8000/api/v1/scraper/estado')
            data = r.json()
            with open('status_check.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print("Status saved to status_check.json")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check())
