from .models import Task
from .config import read_config

from dataclasses import asdict
from datetime import datetime
import json
from pathlib import Path


class _TaskJSONEncoder(json.JSONEncoder):
    def default(self, o: object):
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, Task):
            return asdict(Task)

        return super().default(o)


class _DatetimeJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, source):
        for k, v in source.items():
            if isinstance(v, str):
                try:
                    source[k] = datetime.fromisoformat(str(v))
                except ValueError:
                    # Here we assume that
                    pass
        return source


def tasks_from_json(path: str) -> list[Task]:
    if not Path(path).exists():
        return []

    with open(path, "r") as file:
        data = json.load(file, cls=_DatetimeJSONDecoder)

    return [Task(**item) for item in data]


def tasks_to_json(path: str, tasks: list[Task]) -> None:
    data = [asdict(task) for task in tasks]

    with open(path, "w") as file:
        json.dump(data, file, cls=_TaskJSONEncoder)


def get_tasks() -> list[Task]:
    conf = read_config()
    if conf.storage_type == "json":
        return tasks_from_json(conf.storage_path)
    else:
        NotImplementedError(f"Storage type '{conf.storage_type}' is not supported")


def write_tasks(tasks: list[Task]) -> None:
    conf = read_config()
    if conf.storage_type == "json":
        tasks_to_json(conf.storage_path, tasks)
    else:
        NotImplementedError(f"Storage type '{conf.storage_type}' is not supported")
