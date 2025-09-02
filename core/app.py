import json
from typing import Any, List, Optional

import i3ipc
from i3ipc import Event
from i3ipc.aio import Connection
from i3ipc.events import TickEvent

from core.widgets import Widgets
from interfaces.app import AppABC


class App(AppABC):
    def __init__(self, arguments, config):
        self._i3 = None
        self._connection = i3ipc.Connection()
        self._widgets = Widgets(arguments, self._connection, config).widgets

    @property
    def i3(self) -> Optional[Connection]:
        return self._i3

    @property
    def connection(self) -> i3ipc.Connection:
        return self._connection

    @property
    def widgets(self) -> List[Any]:
        return self._widgets

    async def start(self):
        self._i3 = await Connection(auto_reconnect=True).connect()

        self._i3.on(Event.WINDOW_FOCUS, self.event_handler)
        self._i3.on(Event.WORKSPACE_FOCUS, self.event_handler)
        self._i3.on(Event.WINDOW_FULLSCREEN_MODE, self.event_handler)
        self._i3.on(Event.MODE, self.event_handler)
        self._i3.on("tick", self.on_tick)

        await self._i3.main()

    def event_handler(self, conn, event):
        for widget in self.widgets:
            widget.process_event(event)

    def on_tick(self, conn, event):
        if not isinstance(event, TickEvent):
            return

        try:
            data = json.loads(event.payload)

            if data.get("nobar"):
                for widget in self.widgets:
                    if widget.name == data["widget"]:
                        method = getattr(widget, data["method"])
                        method()

        except json.JSONDecodeError:
            pass
