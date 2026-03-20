import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv

# Load local .env if it exists
load_dotenv()

async def test_db_connection():
    # Get the connection string from environment
    # In Aiven/Neon, it must start with postgresql+asyncpg://
    db_url = os.getenv("DATABASE_URL")
    db_ssl = os.getenv("DB_SSL", "true").lower() in ("true", "1", "yes", "require")
    
    if not db_url:
        print("❌ Error: DATABASE_URL not found in environment variables.")
        return

    print(f"Connecting to: {db_url.split('@')[-1]} (SSL: {db_ssl})")

    connect_args = {"ssl": True} if db_ssl else {}
    
    try:
        engine = create_async_engine(db_url, connect_args=connect_args)
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"✅ Success! Connected to: {version}")
            
            # Check if vacantes table exists and count
            try:
                result = await conn.execute(text("SELECT count(*) FROM vacantes;"))
                count = result.scalar()
                print(f"📊 The 'vacantes' table has {count} records.")
            except Exception as e:
                print(f"⚠️ Warning: Could not query 'vacantes' table. Is the schema applied? Error: {e}")
                
        await engine.dispose()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Troubleshooting Tips:")
        print("1. Ensure the URI starts with 'postgresql+asyncpg://' (NOT 'postgres://').")
        print("2. If using Aiven/Neon, ensure '?sslmode=require' is at the end of the URI.")
        print("3. Ensure DB_SSL is set to 'true' in your environment.")

if __name__ == "__main__":
    asyncio.run(test_db_connection())
