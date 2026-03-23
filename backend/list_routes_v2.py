from api.main import app
import sys

print(f"Python path: {sys.path}")
print(f"Routes found: {len(app.routes)}")

for i, route in enumerate(app.routes):
    methods = getattr(route, "methods", "N/A")
    print(f"{i}: Path={route.path}, Name={route.name}, Methods={methods}")
