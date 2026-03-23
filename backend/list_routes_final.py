from api.main import app

with open("routes_final.txt", "w") as f:
    for route in app.routes:
        methods = getattr(route, "methods", "N/A")
        f.write(f"Path: {route.path}, Methods: {methods}\n")
