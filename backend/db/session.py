import os
import ssl
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

print("--- BACKEND DB CONFIG DEBUG ---")
db_url_raw = os.getenv("DATABASE_URL")
if db_url_raw:
    # Mostramos solo el host y el puerto por seguridad
    masked_url = db_url_raw.split("@")[-1] if "@" in db_url_raw else "INVALID_FORMAT"
    print(f"DATABASE_URL detectada. Host: {masked_url}")
else:
    print("CRITICAL: DATABASE_URL NO ESTÁ CONFIGURADA EN RENDER")

db_ssl_val = os.getenv("DB_SSL")
print(f"DB_SSL valor: {db_ssl_val}")
print("-------------------------------")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://vacantes_user:cambiame@localhost:5432/vacantes_colombia")

db_ssl = os.getenv("DB_SSL", "").strip().lower() in {"1", "true", "yes", "on", "require", "required"}

if db_ssl:
    # Creamos un contexto SSL que no verifique hostnames si hay problemas con certificados internos
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    connect_args = {"ssl": ctx}
    print("DEBUG: SSL Habilitado (Modo Resiliente)")
else:
    connect_args = {}
    print("DEBUG: SSL Deshabilitado")

engine = create_async_engine(DATABASE_URL, echo=False, connect_args=connect_args)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
