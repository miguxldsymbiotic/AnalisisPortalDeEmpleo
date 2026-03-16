import asyncio
from db.session import AsyncSessionLocal
from db.models import ScrapingSession
from sqlalchemy import update

async def resume():
    async with AsyncSessionLocal() as db:
        stmt = update(ScrapingSession).where(ScrapingSession.id == 5).values(estado="en_progreso")
        await db.execute(stmt)
        await db.commit()
        print("Set session 5 to en_progreso. Ready to resume.")

if __name__ == "__main__":
    asyncio.run(resume())
