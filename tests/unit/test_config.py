from unittest.mock import patch

import pytest
from pathlib import Path
from tasks.config import set_config, read_config


def test_set_config(tmp_path: Path) -> None:
    with (
        patch("tasks.config.APP_PATH", tmp_path),
        patch("tasks.config.CONFIG_PATH", tmp_path / "config.json"),
    ):
        set_config("storage_type", "dummy")
        config = read_config()
    assert config.storage_type == "dummy"
