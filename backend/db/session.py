import os
import ssl
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(env_path, override=True)

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
if "postgres://" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

if "?" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?")[0]

# Aiven Specifics for Local DNS Bypass
aiven_host = "pg-1bd8e7df-uniminuto-4de2.k.aivencloud.com"
aiven_ip = "146.190.131.22"

connect_args = {}
is_render = os.getenv("RENDER") == "true"

if not is_render and aiven_host in DATABASE_URL:
    # Local Windows often fails to resolve Aiven hostname, so we use IP + SNI
    DATABASE_URL = DATABASE_URL.replace(aiven_host, aiven_ip)
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    connect_args["ssl"] = ctx
    connect_args["server_hostname"] = aiven_host
else:
    # Standard SSL for Render/Cloud (Aiven requires SSL)
    connect_args["ssl"] = True

engine = create_async_engine(DATABASE_URL, connect_args=connect_args)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
