import sys

from taskmate.tui.task_app import TaskApp


def main() -> int:
    app = TaskApp()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
