from dataclasses import dataclass, asdict
from pathlib import Path
import json

APP_PATH = Path.home() / "tasks"
CONFIG_PATH = APP_PATH / "config.json"


@dataclass
class Config:
    storage_type: str = "json"
    storage_path: str = str(APP_PATH / "storage.json")


def write_config(config: Config) -> None:
    APP_PATH.mkdir(exist_ok=True)
    with CONFIG_PATH.open("w") as file:
        json.dump(asdict(config), file)


def write_default_config() -> None:
    write_config(Config())


def read_config() -> Config:
    if not CONFIG_PATH.exists():
        write_default_config()
    with CONFIG_PATH.open("r") as file:
        data = json.load(file)

    return Config(**data)


def set_config(key: str, value: str) -> None:
    config = read_config()
    if not hasattr(config, key):
        raise ValueError(f"Configuration does not have an attribute named {key}")

    config.__setattr__(key, value)

    write_config(config)
