
import asyncio
import asyncpg
import sys

async def test_conn():
    user = 'alex'
    password = '7W8uDqN4YyPk'
    host = 'ep-falling-math-a5a6w8xe.us-east-2.aws.neon.tech'
    database = 'neondb'
    
    print(f"Testing direct connection to {host}")
    try:
        # Try with ssl='require'
        conn = await asyncpg.connect(
            user=user,
            password=password,
            host=host,
            database=database,
            ssl='require'
        )
        print("Success with ssl='require'")
        await conn.close()
    except Exception as e:
        print(f"Failed with ssl='require': {e}")

if __name__ == "__main__":
    asyncio.run(test_conn())
