import sys

from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem

from taskmate.models import Task
from taskmate import storage

from taskmate.tui.edit import EditScreen
from taskmate.tui.taskwidget import TaskWidget


class TaskApp(App):
    BINDINGS = [
        ("q", "quit", "Save & Quit"),
        ("n", "new", "New"),
        ("e", "edit", "Edit"),
        ("r", "remove", "Remove"),
        # ("c", "config", "Config"),
    ]

    CSS_PATH = "taskapp.tcss"

    def compose(self) -> ComposeResult:
        tasks = storage.get_tasks()
        yield Header()
        yield ListView(*[ListItem(TaskWidget(task)) for task in tasks])
        yield Footer()

    def action_quit(self) -> None:
        self._save()
        self.exit()

    @work
    async def action_new(self) -> None:
        """Adds a new task and directly opens it for editing"""
        list_view = self.query_one(ListView)
        task_widget = TaskWidget(Task.new(""))
        list_item = ListItem(task_widget)

        # Requires @work and await to make sure that we get results before processing
        await self.push_screen_wait(
            EditScreen(task_widget.get_task(), task_widget.set_task)
        )

        list_view.append(list_item)
        list_view.index = len(list_view) - 1  # Highlight created
        list_item.scroll_visible()  # FIXME: Does not scroll any longer

    def action_edit(self) -> None:
        """Opens a new window for editing the selected task"""
        list_view = self.query_one(ListView)
        task_widget = list_view.highlighted_child.query_one(TaskWidget)

        self.push_screen(
            EditScreen(task_widget.get_task()), task_widget.set_task
        )  # TODO: Send whole task widget?

    def _save(self) -> None:
        """Saves tasks to disk"""
        tasks = []
        for taskwidget in self.query(TaskWidget):
            tasks.append(taskwidget.get_task())

        storage.write_tasks(tasks)

    def action_remove(self) -> None:
        """Removes the selected task"""
        list_view = self.query_one(ListView)
        if list_view.highlighted_child:
            list_view.highlighted_child.remove()

        # TODO: Removes even if nothing is highlighted...
        # since it doesnt update visuals after removal.

    def action_config(self) -> None:
        """Opens a new window for modifying configurations"""
        raise NotImplementedError()
