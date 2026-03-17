import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://vacantes_user:cambiame@localhost:5432/vacantes_colombia")

db_ssl = os.getenv("DB_SSL", "").strip().lower() in {"1", "true", "yes", "on", "require", "required"}
connect_args = {"ssl": True} if db_ssl else {}

engine = create_async_engine(DATABASE_URL, echo=False, connect_args=connect_args)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
