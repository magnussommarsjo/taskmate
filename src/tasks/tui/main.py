import sys
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Header, Footer, Static, Checkbox, Label

from tasks.models import Task
from tasks import config, storage

# TODO: Move get and write tasks to a more centralised location together with cli functions. 
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



class TaskWidget(Static):
    def __init__(self, task: Task) -> None:
        super().__init__()
        self._task_item = task # Note: attribute 'task' seems to be already taken
    
    def compose(self) -> ComposeResult:
        yield Checkbox(value = self._task_item.done)
        yield Label(self._task_item.name)


class TaskApp(App):
    BINDINGS = [("q", "quit", "Quit application")]

    CSS_PATH = "taskapp.tcss"

    def compose(self) -> ComposeResult:

        tasks = _get_tasks()
        yield Header()
        yield VerticalScroll(*[TaskWidget(task) for task in tasks])
        yield Footer()

    def action_quit(self) -> None:
        sys.exit()


def main() -> int:
    app = TaskApp()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
