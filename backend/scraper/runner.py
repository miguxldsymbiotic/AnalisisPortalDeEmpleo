import asyncio
from db.session import AsyncSessionLocal
from db.crud import create_or_update_vacantes, create_session, update_session, get_active_session
from .client import ScraperClient
from .parser import parse_vacante

class ScraperRunner:
    def __init__(self):
        self.is_running = False

    async def run(self, max_pages: int = None):
        if self.is_running:
            print("Scraper is already running")
            return
            
        self.is_running = True
        print(f"Scraper started. Max pages: {max_pages or 'Unlimited'}")
        
        async with AsyncSessionLocal() as db:
            session = await get_active_session(db)
            if not session:
                session = await create_session(db)
            
            current_page = session.pagina_actual
            client = ScraperClient()
            
            try:
                while self.is_running:
                    if max_pages and current_page > max_pages:
                        print(f"Reached max pages: {max_pages}")
                        break
                    
                    print(f"Fetching page {current_page}...")
                    data = await client.fetch_page(current_page)
                    resultados = data.get("resultados", [])
                    total_api = data.get("total", 0)
                    
                    if not resultados:
                        print(f"No more results found at page {current_page}. Finishing.")
                        await update_session(db, session.id, estado="completado")
                        break
                    
                    # Parse and save
                    parsed_vacantes = [parse_vacante(v) for v in resultados]
                    rows_affected = await create_or_update_vacantes(db, parsed_vacantes)
                    
                    # Update session progress
                    await update_session(
                        db, 
                        session.id, 
                        pagina_actual=current_page + 1,
                        total_registros=total_api,
                        registros_nuevos=session.registros_nuevos + rows_affected
                    )
                    
                    print(f"Page {current_page} processed. Added/Updated: {rows_affected} vacantes.")
                    current_page += 1
                    
            except Exception as e:
                print(f"Scraper encountered a critical error: {e}")
                await update_session(db, session.id, estado="error")
            finally:
                self.is_running = False
                await client.close()

    def stop(self):
        self.is_running = False
