import asyncio
from db.session import AsyncSessionLocal
from sqlalchemy import text

async def check():
    async with AsyncSessionLocal() as db:
        res = await db.execute(text('SELECT id, pagina_actual, total_registros, estado FROM scrape_sessions ORDER BY id DESC LIMIT 5'))
        print("Recent Sessions:")
        for row in res:
            print(f" ID: {row[0]}, Page: {row[1]}, Records: {row[2]}, Status: {row[3]}")

if __name__ == "__main__":
    asyncio.run(check())
