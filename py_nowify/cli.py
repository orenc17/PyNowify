"""py_nowify/cli.py - Command Line Entry Point."""

from .app import NowifyApp


def main() -> None:
    app = NowifyApp()
    app.run()


if __name__ == "__main__":
    main()
