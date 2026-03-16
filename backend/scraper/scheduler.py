"""
Scheduler para scrapes periódicos usando APScheduler.
Configurable via .env: SCRAPER_CRON_HOURS (default=24 = una vez al día)
"""
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from .runner import ScraperRunner

CRON_HOURS = int(os.getenv("SCRAPER_CRON_HOURS", 24))

scheduler = AsyncIOScheduler()
scheduled_runner = ScraperRunner()


async def scheduled_scrape_job():
    """Job que ejecuta el scraper. Si ya está corriendo, no hace nada."""
    if scheduled_runner.is_running:
        print("[Scheduler] Scraper ya está en ejecución, saltando este ciclo.")
        return
    print(f"[Scheduler] Iniciando scrape programado...")
    await scheduled_runner.run()
    print(f"[Scheduler] Scrape programado finalizado.")


def start_scheduler():
    """Arranca el scheduler con el intervalo configurado."""
    scheduler.add_job(
        scheduled_scrape_job,
        trigger=IntervalTrigger(hours=CRON_HOURS),
        id="scrape_periodico",
        name="Scrape periódico del SPE",
        replace_existing=True,
    )
    scheduler.start()
    print(f"[Scheduler] Activo — scrape cada {CRON_HOURS} horas")


def stop_scheduler():
    """Detiene el scheduler limpiamente."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        print("[Scheduler] Detenido.")
