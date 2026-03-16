from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.session import get_db
from db.models import ScrapingSession
from scraper.runner import ScraperRunner
import asyncio

router = APIRouter(prefix="/scraper", tags=["scraper"])

# Instancia global del scraper para manejar el estado en memoria
scraper_runner = ScraperRunner()

@router.post("/iniciar")
async def start_scraper(background_tasks: BackgroundTasks):
    if scraper_runner.is_running:
        raise HTTPException(status_code=400, detail="El scraper ya está ejecutándose")
        
    background_tasks.add_task(scraper_runner.run)
    return {"message": "Scraper iniciado en segundo plano"}

@router.post("/iniciar-completo")
async def start_full_scraper(start_page: int = 1, background_tasks: BackgroundTasks = None, db: AsyncSession = Depends(get_db)):
    """
    Inicia un scrape completo, 
    limpiando cualquier sesión previa 'en_progreso'.
    Permite empezar desde una página específica (offset).
    """
    if scraper_runner.is_running:
        raise HTTPException(status_code=400, detail="El scraper ya está ejecutándose")
    
    # Marcamos sesiones previas en progreso como canceladas para no interferir
    from sqlalchemy import update
    stmt = update(ScrapingSession).where(ScrapingSession.estado == "en_progreso").values(estado="cancelado")
    await db.execute(stmt)
    await db.commit()
    
    # Creamos nueva sesión limpia
    from db.crud import create_session
    session = await create_session(db, start_page=start_page)
    
    if background_tasks:
        background_tasks.add_task(scraper_runner.run)
    else:
        asyncio.create_task(scraper_runner.run())
        
    return {"message": f"Scrape completo iniciado (Sesión {session.id}) desde la página {start_page}"}

@router.post("/cancelar")
async def cancel_scraper(db: AsyncSession = Depends(get_db)):
    if not scraper_runner.is_running:
        raise HTTPException(status_code=400, detail="El scraper no está en ejecución")
        
    scraper_runner.stop()
    
    from db.crud import get_active_session, update_session
    session = await get_active_session(db)
    if session:
        await update_session(db, session.id, estado="cancelado")
        
    return {"message": "Scraper detenido (pausado). Los datos guardados se mantienen."}

@router.get("/estado")
async def get_scraper_estado(db: AsyncSession = Depends(get_db)):
    from db.crud import get_active_session
    session = await get_active_session(db)
    
    # Si no hay activa, buscamos la última de cualquier tipo
    if not session:
        stmt = select(ScrapingSession).order_by(ScrapingSession.id.desc()).limit(1)
        res = await db.execute(stmt)
        session = res.scalar_one_or_none()
        
    if not session:
        return {"estado": "Sin sesiones", "running": False}
        
    return {
        "id_sesion": session.id,
        "running": scraper_runner.is_running,
        "estado": session.estado,
        "pagina_actual": session.pagina_actual,
        "total_registros": session.total_registros,
        "registros_nuevos": session.registros_nuevos,
        "fecha_inicio": session.fecha_inicio
    }


@router.get("/sesiones")
async def list_sesiones(db: AsyncSession = Depends(get_db)):
    stmt = select(ScrapingSession).order_by(ScrapingSession.id.desc()).limit(20)
    result = await db.execute(stmt)
    return result.scalars().all()
