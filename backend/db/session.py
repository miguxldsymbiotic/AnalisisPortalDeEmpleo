import os
import ssl
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

print("--- BACKEND DB CONFIG DEBUG ---")

# Intentar primero con variables separadas
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

if DB_USER and DB_PASSWORD and DB_HOST and DB_NAME:
    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(f"DEBUG: Usando variables separadas. Host: {DB_HOST}, DB: {DB_NAME}")
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://vacantes_user:cambiame@localhost:5432/vacantes_colombia")
    if "@" in DATABASE_URL:
        masked_url = DATABASE_URL.split("@")[-1]
        print(f"DEBUG: Usando DATABASE_URL. Host: {masked_url}")
    else:
        print("CRITICAL: DATABASE_URL NO ESTÁ CONFIGURADA O TIENE FORMATO INVÁLIDO")

db_ssl_val = os.getenv("DB_SSL")
print(f"DB_SSL valor: {db_ssl_val}")
print("-------------------------------")

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
