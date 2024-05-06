from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop
import sys
import asyncio
from modules.info import Info
from modules.workspaces import Workspaces
from core.config import config
from i3ipc.aio import Connection
from i3ipc import Event

def update_workspaces(i3, event, workspaces_panel):
    workspaces_panel.update()

async def main():
    i3 = await Connection().connect()

    workspaces_panel = Workspaces(config['workspaces'])
    info_panel = Info(config['info'])

    i3.on(Event.WINDOW, lambda i3, event: update_workspaces(i3, event, workspaces_panel))
    await i3.main()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)

    with event_loop:
        sys.exit(event_loop.run_until_complete(main()))

