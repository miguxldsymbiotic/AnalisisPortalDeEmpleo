import httpx
import asyncio

async def check():
    async with httpx.AsyncClient() as client:
        # Check page 3
        r = await client.get('https://www.buscadordeempleo.gov.co/backbue/v1//vacantes/resultados?page=3')
        data = r.json()
        print(f"Page 3 results: {len(data.get('resultados', []))}")
        
        # Check if page 3 is different from page 1
        r1 = await client.get('https://www.buscadordeempleo.gov.co/backbue/v1//vacantes/resultados?page=1')
        data1 = r1.json()
        
        id1 = data1.get('resultados', [{}])[0].get('id_vacante')
        id3 = data.get('resultados', [{}])[0].get('id_vacante')
        print(f"Page 1 ID: {id1}, Page 3 ID: {id3}")
        if id1 == id3:
            print("WARNING: Pagination might be ignored by server!")

if __name__ == "__main__":
    asyncio.run(check())
