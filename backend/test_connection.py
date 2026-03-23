import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv
import ssl

load_dotenv(override=True)

async def test():
    db_url = os.getenv("DATABASE_URL")
    aiven_host = "pg-1bd8e7df-uniminuto-4de2.k.aivencloud.com"
    aiven_ip = "146.190.131.22"
    
    if aiven_host in db_url:
        db_url = db_url.replace(aiven_host, aiven_ip)
    if "?" in db_url:
        db_url = db_url.split("?")[0]

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    print(f"Connecting to: {db_url}")
    try:
        engine = create_async_engine(db_url, connect_args={
            "ssl": ctx,
            "server_hostname": aiven_host
        })
        async with engine.connect() as conn:
            res = await conn.execute(text("SELECT version()"))
            print(f"✅ Success: {res.scalar()}")
        await engine.dispose()
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test())
