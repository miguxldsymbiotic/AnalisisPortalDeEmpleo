from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

from scraper.scheduler import start_scheduler, stop_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_scheduler()
    yield
    # Shutdown
    stop_scheduler()

app = FastAPI(title="Vacantes Colombia API — BID Analytics", lifespan=lifespan)

origins = [
    os.getenv("CORS_ORIGINS", "http://localhost:5173"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from api.routers import vacantes, estadisticas, scraper, exportar

app.include_router(vacantes.router, prefix="/api/v1")
app.include_router(estadisticas.router, prefix="/api/v1")
app.include_router(scraper.router, prefix="/api/v1")
app.include_router(exportar.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Vacantes Colombia API — BID Analytics is running!"}

