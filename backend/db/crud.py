from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
import datetime
from .models import Vacante, ScrapingSession

async def create_or_update_vacantes(db: AsyncSession, vacantes_data: list[dict]):
    if not vacantes_data:
        return 0
    
    # insert with on_conflict_do_update for postgres
    stmt = insert(Vacante).values(vacantes_data)
    
    update_dict = {
        col.name: col for col in stmt.excluded 
        if col.name not in ['id', 'codigo_vacante']
    }
    
    stmt = stmt.on_conflict_do_update(
        index_elements=['codigo_vacante'],
        set_=update_dict
    )
    
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount

async def get_active_session(db: AsyncSession) -> ScrapingSession | None:
    from sqlalchemy import select
    stmt = select(ScrapingSession).where(ScrapingSession.estado == "en_progreso").order_by(ScrapingSession.id.desc()).limit(1)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def create_session(db: AsyncSession, start_page: int = 1) -> ScrapingSession:
    new_session = ScrapingSession(pagina_actual=start_page)
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session

async def update_session(db: AsyncSession, session_id: int, **kwargs):
    from sqlalchemy import update
    stmt = update(ScrapingSession).where(ScrapingSession.id == session_id).values(**kwargs)
    await db.execute(stmt)
    await db.commit()
