import httpx
import asyncio

async def check_api():
    url1 = "https://www.buscadordeempleo.gov.co/backbue/v1//vacantes/resultados?page=1"
    url2 = "https://www.buscadordeempleo.gov.co/backbue/v1//vacantes/resultados?page=2"
    
    async with httpx.AsyncClient() as client:
        r1 = await client.get(url1)
        data1 = r1.json()
        print(f"Page 1 records: {len(data1.get('resultados', []))}")
        print(f"Keys in response: {data1.keys()}")
        if 'total' in data1:
            print(f"Total records reported by API: {data1['total']}")
        
        r2 = await client.get(url2)
        data2 = r2.json()
        print(f"Page 2 records: {len(data2.get('resultados', []))}")
        
        # Check if first record of page 1 is same as page 2 (indicates pagination not working as expected)
        res1 = data1.get('resultados', [])
        res2 = data2.get('resultados', [])
        if res1 and res2 and res1[0].get('id_vacante') == res2[0].get('id_vacante'):
            print("WARNING: Page 1 and Page 2 have the same first record! Pagination might be broken or use different params.")

if __name__ == "__main__":
    asyncio.run(check_api())
