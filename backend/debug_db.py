import asyncio
from db.session import AsyncSessionLocal
from sqlalchemy import text

async def check():
    async with AsyncSessionLocal() as db:
        res = await db.execute(text('SELECT count(*) FROM vacantes'))
        count = res.scalar()
        print(f"Total vacantes: {count}")
        
        res = await db.execute(text('SELECT departamento, count(*) FROM vacantes GROUP BY departamento ORDER BY count(*) DESC LIMIT 10'))
        print("Top 10 Departamentos:")
        for row in res:
            print(f" - {row[0]}: {row[1]}")

if __name__ == "__main__":
    asyncio.run(check())
