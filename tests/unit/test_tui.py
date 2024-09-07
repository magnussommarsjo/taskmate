from collections.abc import Iterator
from taskmate.models import Task
from taskmate.tui.task_app import TaskApp, TaskWidget
from textual.keys import Keys


from textual.widgets import ListView
import pytest
from unittest.mock import patch


@pytest.fixture
def app() -> Iterator[TaskApp]:
    """Fixture for application that mocks storage"""
    dummy_tasks = [Task.new("dummy_1"), Task.new("dummy_2")]
    with (
        patch("taskmate.tui.task_app.storage.get_tasks", lambda: dummy_tasks),
        patch("taskmate.tui.task_app.storage.write_tasks", lambda *_: None),
    ):
        yield TaskApp()


@pytest.mark.asyncio
async def test_app_start(app: TaskApp) -> None:
    """Make sure app can start and quit successfully."""
    async with app.run_test() as pilot:
        assert app.is_running
        # Quitting application
        await pilot.press("q")
        assert not app.is_running


@pytest.mark.asyncio
async def test_create_task(app: TaskApp) -> None:
    async with app.run_test() as pilot:
        list_view = app.query_one(ListView)
        length_before = len(list_view)

        await pilot.press("n")  # New task
        await pilot.press(Keys.Escape)  # Exit new task ModalScreen
        await pilot.press("q")  # Quit & Save

        assert len(list_view) == length_before + 1


@pytest.mark.asyncio
async def test_remove_task(app: TaskApp) -> None:
    async with app.run_test() as pilot:
        list_view = app.query_one(ListView)
        length_before = len(list_view)

        await pilot.press("r")  # Remove task
        await pilot.press("enter")  # Confirm deletion
        await pilot.press("q")  # Quit & Save

        assert len(list_view) == length_before - 1


@pytest.mark.asyncio
async def test_remove_task_while_empty(app: TaskApp) -> None:
    """This teste that the application does not crash while trying to remove while no items are left."""
    async with app.run_test() as pilot:
        list_view = app.query_one(ListView)
        length_before = len(list_view)

        # Remove all tasks
        for _ in range(length_before):
            await pilot.press("r")  # Remove task

        # Ensure list is empty
        assert len(list_view) == 0

        # Try removing task when list is empty
        await pilot.press("r")

        # Ensure application is still running and list is still empty
        assert app.is_running
        assert len(list_view) == 0


@pytest.mark.asyncio
async def test_edit_task(app: TaskApp) -> None:
    async with app.run_test() as pilot:
        await pilot.press("e")
        await pilot.press(Keys.Tab)  # Move to task name
        await pilot.press("e", "x", "t", "r", "a")  # Add to task name
        await pilot.press(Keys.Escape)

        task_names = [
            task_widget.get_task().name for task_widget in app.query(TaskWidget)
        ]
        assert any(["extra" in name for name in task_names])
