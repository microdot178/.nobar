"""Entry point for the nobar widget system."""

from __future__ import annotations

import asyncio
import sys

from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop
from setproctitle import setproctitle

from nobar.core.app import App
from nobar.core.arguments import Arguments
from nobar.core.config import Config


async def main() -> None:
    """Initialize and start the application."""
    arguments = Arguments().arguments
    config = Config(arguments.config).config
    app = App(arguments, config)
    await app.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    setproctitle("nobar")

    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    with event_loop:
        sys.exit(event_loop.run_until_complete(main()))
