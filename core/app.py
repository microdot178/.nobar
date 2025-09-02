import json

import i3ipc
from i3ipc import Event
from i3ipc.aio import Connection
from i3ipc.events import TickEvent

from core.widgets import Widgets
from interfaces.app import AppABC


class App(AppABC):
    def __init__(self, arguments, config):
        self.i3 = None
        self.connection = i3ipc.Connection()
        self.widgets = Widgets(arguments, self.connection, config).widgets

    async def start(self):
        self.i3 = await Connection(auto_reconnect=True).connect()

        self.i3.on(Event.WINDOW_FOCUS, self.event_handler)
        self.i3.on(Event.WORKSPACE_FOCUS, self.event_handler)
        self.i3.on(Event.WINDOW_FULLSCREEN_MODE, self.event_handler)
        self.i3.on(Event.MODE, self.event_handler)
        self.i3.on("tick", self.on_tick)

        await self.i3.main()

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
