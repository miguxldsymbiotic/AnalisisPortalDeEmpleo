import asyncio
from db.session import AsyncSessionLocal
from db.models import ScrapingSession
from sqlalchemy import update

async def fast_forward():
    async with AsyncSessionLocal() as db:
        # Cancel any hanging sessions
        stmt = update(ScrapingSession).where(ScrapingSession.estado == 'en_progreso').values(estado='cancelado')
        await db.execute(stmt)
        
        # Create a new session starting at page 4455
        new_session = ScrapingSession(pagina_actual=4455, estado='en_progreso', total_registros=289000, registros_nuevos=0)
        db.add(new_session)
        await db.commit()
        await db.refresh(new_session)
        print(f"Created new session {new_session.id} starting at page 4455")

if __name__ == "__main__":
    asyncio.run(fast_forward())
