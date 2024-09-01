"""Edit task screen"""

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Input, Label, Checkbox
from textual.containers import Vertical, Horizontal

from taskmate.models import Task


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
        with Vertical(id="dialog"):
            yield Header()
            with Horizontal():
                yield Label("Done:")
                yield Checkbox(value=self.__task.done, id="done")
            with Horizontal():
                yield Label("Name:")
                yield Input(value=self.__task.name, id="name")
            with Horizontal():
                yield Label("Priority:")
                yield Input(value=str(self.__task.priority), id="priority", type="integer")
            with Horizontal():
                yield Label("Description:")
                yield Input(value=self.__task.description, id="description")

            # TODO: Add more content 
            yield Footer()
    
    def _update_task(self) -> None:
        done_checkbox = self.query_one("#done", Checkbox)
        name_input = self.query_one("#name", Input)
        priority_input = self.query_one("#priority", Input)
        description_input = self.query_one("#description", Input)

        self.__task.name = name_input.value
        self.__task.done = done_checkbox.value
        self.__task.priority = int(priority_input.value)
        self.__task.description = description_input.value



    def action_escape(self) -> None:
        # TODO: Potentially 'esc' should cancel the creation?
        self._update_task()
        self.dismiss(self.__task)
