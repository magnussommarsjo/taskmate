from tasks.models import Task
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.style import Style

default_style = Style()
warning_style = Style(color="white", bgcolor="red")
done_style = Style(color="bright_black")


def list_tasks(tasks: list[Task]) -> None:
    table = Table(title="Tasks")

    table.add_column("#")
    table.add_column("Name")
    table.add_column("Done")
    table.add_column("Priority")
    table.add_column("Description")
    table.add_column("Created")
    table.add_column("Due")
    table.add_column("Finished")

    for num, task in enumerate(tasks):
        is_passed_due = (task.due is not None) and (datetime.now() > task.due)

        # Set row style
        row_style = default_style

        if is_passed_due:
            row_style = warning_style
        if task.done:
            row_style = done_style

        table.add_row(
            str(num + 1),
            task.name,
            "True" if task.done else "False",
            str(task.priority),
            task.description,
            task.created.date().isoformat(),  # .isoformat(timespec="minutes"),
            task.due.date().isoformat() if task.due else None,
            task.finished.date().isoformat() if task.finished else None,
            style=row_style,
        )

    console = Console()
    console.print(table)
