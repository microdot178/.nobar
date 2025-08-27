import asyncio
import sys

import i3ipc
from i3ipc import Event
from i3ipc.aio import Connection
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop
from setproctitle import setproctitle

from core.arguments import Arguments
from core.config import Config
from core.widgets import Widgets


async def main():
    i3 = await Connection(auto_reconnect=True).connect()
    connection = i3ipc.Connection()

    arguments = Arguments().arguments
    config = Config(arguments.config).config
    widgets = Widgets(arguments, connection, config).widgets

    def event_handler(i3=None, event=None):
        for widget in widgets:
            widget.process_event(event)

    i3.on(Event.WINDOW_FOCUS, event_handler)
    i3.on(Event.WORKSPACE_FOCUS, event_handler)
    i3.on(Event.WINDOW_FULLSCREEN_MODE, event_handler)
    i3.on(Event.MODE, event_handler)

    for widget in widgets:
        widget.set_content()

    await i3.main()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    setproctitle("nobar")

    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    with event_loop:
        sys.exit(event_loop.run_until_complete(main()))
