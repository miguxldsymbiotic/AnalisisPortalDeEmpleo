import httpx
import json

def normalize(s):
    if not s: return ""
    import unicodedata
    s = s.upper()
    s = "".join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return s.strip()

async def inspect_geojson():
    url = "https://data.humdata.org/dataset/b20cd185-1d48-43d4-9d62-1b12b23a54b6/resource/c621bcab-ce97-42bb-96f3-15c3507a1f53/download/geoBoundaries-COL-ADM1.geojson"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, follow_redirects=True)
        data = r.json()
        print(f"Number of features: {len(data['features'])}")
        for feature in data['features'][:5]:
            props = feature['properties']
            print(f"Properties: {props}")
            # Identify candidate name field
            name = props.get('shapeName') or props.get('name') or props.get('NAME_1')
            print(f"Candidate Name: {name} (Normalized: {normalize(name)})")

if __name__ == "__main__":
    import asyncio
    asyncio.run(inspect_geojson())
