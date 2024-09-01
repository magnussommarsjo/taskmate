from textual.app import ComposeResult
from textual.widgets import Static, Checkbox, Label

from taskmate.models import Task



class TaskWidget(Static):
    def __init__(self, task: Task) -> None:
        super().__init__()
        self.__task = task  # Note: attribute 'task' seems to be already taken

    def compose(self) -> ComposeResult:
        yield Checkbox(value=self.__task.done)
        yield Label(self.__task.name)
    
    def get_task(self) -> Task:
        return self.__task
    
    def set_task(self, task: Task) -> None:
        self.__task = task
        self.refresh(recompose=True)  # TODO: Can we avoid recompose? Reactive params?

