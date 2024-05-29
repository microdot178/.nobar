import asyncio
import sys

import i3ipc
from i3ipc import Event
from i3ipc.aio import Connection
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

from core.config import get_config
from modules.info import Info
from modules.workspaces import Workspaces


async def main():
    i3 = await Connection(auto_reconnect=True).connect()
    connection = i3ipc.Connection()
    config = get_config("config.toml")

    workspaces_panel = Workspaces(connection, config["workspaces"])
    info_panel = Info(connection, config["info"])

    async def event_handler(i3=None, event=None):
        workspaces_panel.set_content()
        info_panel.set_content()

    await event_handler()

    i3.on(Event.WORKSPACE_FOCUS, event_handler)
    i3.on("mode", event_handler)
    await i3.main()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    with event_loop:
        sys.exit(event_loop.run_until_complete(main()))
