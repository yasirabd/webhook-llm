import yaml
from pathlib import Path

def load_yaml_config(relative_path: str) -> dict:
    # Relative to the app/ folder
    config_path = Path(__file__).resolve().parent.parent / relative_path

    if not config_path.exists():
        raise FileNotFoundError(f"YAML config not found at: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)