from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop
import sys
import asyncio
from modules.info import Info
from modules.workspaces import Workspaces
from core.config import get_config
from i3ipc.aio import Connection
from i3ipc import Event

async def update_workspaces(i3, event, workspaces_panel):
    workspaces = await i3.get_workspaces()

    workspaces_panel.update(workspaces)

async def main():
    i3 = await Connection(auto_reconnect=True).connect()
    config = get_config('config.toml')

    workspaces_panel = Workspaces(config['workspaces'])
    info_panel = Info(config['info'])

    async def event_handler(i3, event):
        await update_workspaces(i3, event, workspaces_panel)

    i3.on(Event.WORKSPACE_FOCUS, event_handler)
    await i3.main()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    with event_loop:
        sys.exit(event_loop.run_until_complete(main()))

