"""Edit task screen"""

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, Input, Label
from textual.containers import Grid

from tasks.models import Task


class EditScreen(ModalScreen[Task]):
    BINDINGS = [("escape", "escape", "Back")]

    def __init__(
        self,
        task: Task,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        # NOTE: double underscore since '_task' is already taken
        self.__task = task

    def compose(self) -> ComposeResult:
        yield Grid(
            Header(),
            Label("Name:"),
            Input(value=self.__task.name, id="name"),
            # TODO: Add more content 
            Footer(), id="dialog")
    
    def _update_task(self) -> None:
        name_input: Input = self.query_one("#name")

        self.__task.name = name_input.value

    def action_escape(self) -> None:
        self._update_task()
        self.dismiss(self.__task)
