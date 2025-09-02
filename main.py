import asyncio
import sys

from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop
from setproctitle import setproctitle

from core.app import App
from core.arguments import Arguments
from core.config import Config


async def main():
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
