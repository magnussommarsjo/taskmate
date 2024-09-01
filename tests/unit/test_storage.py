from datetime import datetime
from pathlib import Path
import pytest

from taskmate.models import Task
from taskmate.storage import tasks_from_json, tasks_to_json


@pytest.fixture
def tasks() -> list[Task]:
    return [
        Task(
            name="task_1",
            done=False,
            priority=10,
            description="description",
            created=datetime.now(),
            finished=None,
            due=None,
        ),
        Task(
            name="task_2",
            done=False,
            priority=10,
            description="description",
            created=datetime.now(),
            finished=None,
            due=None,
        ),
    ]


def test_to_from_json(tasks: list[Task], tmp_path: Path) -> None:
    json_file_path = tmp_path / "data.json"
    tasks_to_json(json_file_path, tasks)
    tasks_read = tasks_from_json(json_file_path)

    assert tasks_read == tasks
