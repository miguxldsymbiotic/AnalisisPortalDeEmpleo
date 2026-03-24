import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
import os
import sys
from dotenv import load_dotenv
import ssl

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(env_path, override=True)

from db.models import Base
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

db_url = os.getenv("DATABASE_URL", "")
if not db_url:
    # Fallback to config if env var is missing
    db_url = config.get_main_option("sqlalchemy.url", "")

if "postgres://" in db_url:
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)

if "?" in db_url:
    db_url = db_url.split("?")[0]

aiven_host = "pg-1bd8e7df-uniminuto-4de2.k.aivencloud.com"
aiven_ip = "146.190.131.22"

# Global SSL Context
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

connect_args = {"ssl": ctx}
is_render = os.getenv("RENDER") == "true"

if not is_render and aiven_host in db_url:
    db_url = db_url.replace(aiven_host, aiven_ip)
    connect_args["server_hostname"] = aiven_host

async def run_async_migrations() -> None:
    connectable = create_async_engine(db_url, poolclass=pool.NullPool, connect_args=connect_args)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    pass
else:
    run_migrations_online()
