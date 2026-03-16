import httpx
import os

URLs = [
    "https://raw.githubusercontent.com/gmarulanda/colombia-geojson/master/colombia.geo.json",
    "https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/colombia.geo.json", # Previous one, maybe URL was slightly different
    "https://raw.githubusercontent.com/strotul/colombia-departamentos-geojson/master/colombia-departamentos.json"
]

output_path = r"c:\Users\migux\Downloads\PROYECTO\frontend\public\colombia.json"

async def download_geojson():
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    async with httpx.AsyncClient(follow_redirects=True) as client:
        for url in URLs:
            try:
                print(f"Trying {url}...")
                r = await client.get(url)
                if r.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(r.content)
                    print(f"Success! Saved to {output_path}")
                    return True
            except Exception as e:
                print(f"Failed {url}: {e}")
    return False

if __name__ == "__main__":
    import asyncio
    asyncio.run(download_geojson())
