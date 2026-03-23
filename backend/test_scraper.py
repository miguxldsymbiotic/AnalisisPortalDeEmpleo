import asyncio
import os
import sys

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper.runner import ScraperRunner

async def main():
    print("Testing Scraper for 2 pages...")
    runner = ScraperRunner()
    await runner.run(max_pages=2)
    print("Test finished.")

if __name__ == "__main__":
    asyncio.run(main())
