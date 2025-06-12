from fastapi import FastAPI
from pathlib import Path
import yaml
import importlib

app = FastAPI()

def load_routes(config_path: str = "config/routes.yaml"):
    base_dir = Path(__file__).parent  # points to app/
    config_file = base_dir / config_path
    with open(config_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("routes", [])

def get_handler(handler_path: str):
    module_path, function_name = handler_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, function_name)

routes = load_routes()

for route in routes:
    if not route.get("enabled", True):
        continue

    path = route["path"]
    method = route["method"].lower()
    handler = get_handler(route["handler"])

    if method == "post":
        app.post(path)(handler)
    elif method == "get":
        app.get(path)(handler)
    else:
        raise ValueError(f"Unsupported HTTP method: {route['method']}")