import httpx
import asyncio

async def check():
    async with httpx.AsyncClient() as client:
        r = await client.get('https://www.buscadordeempleo.gov.co/backbue/v1//vacantes/resultados?page=1')
        data = r.json()
        results = data.get('resultados', [])
        if results:
            first = results[0]
            print(f"Keys: {first.keys()}")
            print(f"CODIGO_VACANTE: {first.get('CODIGO_VACANTE')}")
            print(f"ID: {first.get('id')}")
        else:
            print("No results found.")

if __name__ == "__main__":
    asyncio.run(check())
