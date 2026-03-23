import os
import ssl
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(env_path, override=True)

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
if "postgres://" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

aiven_host = "pg-1bd8e7df-uniminuto-4de2.k.aivencloud.com"
aiven_ip = "146.190.131.22"
if aiven_host in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace(aiven_host, aiven_ip)
if "?" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?")[0]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

engine = create_async_engine(DATABASE_URL, connect_args={
    "ssl": ctx,
    "server_hostname": aiven_host
})
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
