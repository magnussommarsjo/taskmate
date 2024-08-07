from datetime import datetime
from typing import Optional, Annotated
import typer
from tasks import storage, config
from tasks.models import Task

from .commads import list_tasks
from rich.console import Console

typer.Argument()
app = typer.Typer()
console = Console()


def _get_tasks() -> list[Task]:
    conf = config.read_config()
    if conf.storage_type == "json":
        return storage.tasks_from_json(conf.storage_path)
    else:
        NotImplementedError(f"Storage type '{conf.storage_type}' is not supported")


def _write_tasks(tasks: list[Task]) -> None:
    conf = config.read_config()
    if conf.storage_type == "json":
        storage.tasks_to_json(conf.storage_path, tasks)
    else:
        NotImplementedError(f"Storage type '{conf.storage_type}' is not supported")


@app.command()
def list():
    """List all availible tasks."""
    tasks = _get_tasks()

    list_tasks(tasks)


@app.command()
def create(
    name: str,
    priority: Annotated[int, typer.Option("--priority", "-p")] = 10,
    description: Annotated[str, typer.Option("--description", "-d")] = "",
    due: Optional[datetime] = None,
):
    """Create a new task."""
    tasks = _get_tasks()

    task = Task.new(name=name, priority=priority, description=description, due=due)
    tasks.append(task)

    _write_tasks(tasks)


@app.command()
def remove(num: int) -> None:
    """Remove task by specifying its number in the list."""
    tasks = _get_tasks()
    if num < 1 or num > len(tasks):
        console.print(f"Number must be between 1 and {len(tasks)}.")
        raise typer.Exit(code=1)

    _ = tasks.pop(num - 1)
    _write_tasks(tasks)


@app.command()
def done(num: int) -> None:
    "Mark a task as 'done'."
    # TODO: Maybe a better name for this command?
    tasks = _get_tasks()
    if num < 1 or num > len(tasks):
        console.print(f"Number must be between 1 and {len(tasks)}.")
        raise typer.Exit(code=1)
    tasks[num - 1].set_done()
    _write_tasks(tasks)
