import asyncio
import sys

import i3ipc
from i3ipc import Event
from i3ipc.aio import Connection
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop
from setproctitle import setproctitle

from core.config import Config
from modules.info import Info
from modules.workspaces import Workspaces


async def main():
    i3 = await Connection(auto_reconnect=True).connect()
    connection = i3ipc.Connection()
    config = Config(sys.argv[1]).config

    workspaces_panel = Workspaces(connection, config["workspaces"])
    info_panel = Info(connection, config["info"])

    async def event_handler_general(i3=None, event=None):
        workspaces_panel.process_event(event)
        info_panel.process_event(event)

    async def event_handler_info(i3=None, event=None):
        info_panel.process_event(event)

    async def initialize_modules():
        workspaces_panel.set_content()
        info_panel.set_content()

    i3.on(Event.WINDOW_FOCUS, event_handler_general)
    i3.on(Event.WORKSPACE_FOCUS, event_handler_general)
    i3.on(Event.WINDOW_FULLSCREEN_MODE, event_handler_general)
    i3.on(Event.MODE, event_handler_info)

    await initialize_modules()
    await i3.main()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    setproctitle("nobar")

    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    with event_loop:
        sys.exit(event_loop.run_until_complete(main()))
