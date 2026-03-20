import os
import ssl
import traceback
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

print("--- BACKEND DB CONFIG DEBUG ---")

# Intentar primero con variables separadas
DB_USER = os.getenv("DB_USER", "").strip()
DB_PASSWORD = os.getenv("DB_PASSWORD", "").strip()
DB_HOST = os.getenv("DB_HOST", "").strip()
DB_PORT = os.getenv("DB_PORT", "20351").strip()
DB_NAME = os.getenv("DB_NAME", "").strip()

if DB_USER and DB_PASSWORD and DB_HOST and DB_NAME:
    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(f"DEBUG: Variables separadas detectadas. Host: {DB_HOST}, DB: {DB_NAME}")
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://vacantes_user:cambiame@localhost:5432/vacantes_colombia").strip()
    
    # Normalización del prefijo para SQLAlchemy Async
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
    
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
        try:
            # Información extra de diagnóstico
            res = await session.execute(text("SELECT current_database(), current_user, current_schema()"))
            db_now, user_now, schema_now = res.one()
            print(f"DEBUG: Conexión activa a DB: {db_now}, Usuario: {user_now}, Esquema: {schema_now}")
            
            # Aseguramos el search_path por si acaso
            await session.execute(text("SET search_path TO public"))
            
            # Prueba de existencia de tabla crítica
            await session.execute(text("SELECT 1 FROM vacantes LIMIT 1"))
            print("DEBUG: Tabla 'vacantes' encontrada y accesible.")
            
            yield session
        except Exception as e:
            print("--- CRITICAL DB CONNECTION ERROR ---")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            traceback.print_exc()
            print("-------------------------------------")
            raise e
