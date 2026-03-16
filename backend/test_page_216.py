import httpx
import asyncio

async def test_page():
    url = "https://www.buscadordeempleo.gov.co/backbue/v1//vacantes/resultados?page=216"
    print(f"Fetching {url}...")
    try:
        async with httpx.AsyncClient(timeout=40.0) as client:
            r = await client.get(url)
            print(f"Status: {r.status_code}")
            data = r.json()
            print(f"Results: {len(data.get('resultados', []))}")
            print(f"Total reported: {data.get('total')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_page())
