import yaml
from pathlib import Path


def load_config() -> dict:

    config_path = Path("config/config.yaml")

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )

    with config_path.open("r") as file:
        config = yaml.safe_load(file)

    return config