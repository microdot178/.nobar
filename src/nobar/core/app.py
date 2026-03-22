"""Main application class for i3 event handling."""

from __future__ import annotations

import json

import i3ipc
from i3ipc import Event
from i3ipc.aio import Connection
from i3ipc.events import IpcBaseEvent, TickEvent

from nobar.core.widgets import create_widgets

ALLOWED_TICK_METHODS = {"toggle", "set_content"}


class App:
    """Core application managing i3 IPC connection and widget routing."""

    def __init__(self, arguments: object, config: dict) -> None:
        """Initialize app with parsed arguments and configuration."""
        self._connection = i3ipc.Connection()
        self._widgets = create_widgets(arguments, self._connection, config)

    async def start(self) -> None:
        """Connect to i3 and start the event loop."""
        i3 = await Connection(auto_reconnect=True).connect()

        i3.on(Event.WINDOW_FOCUS, self._on_event)
        i3.on(Event.WORKSPACE_FOCUS, self._on_event)
        i3.on(Event.WINDOW_FULLSCREEN_MODE, self._on_event)
        i3.on(Event.MODE, self._on_event)
        i3.on("tick", self._on_tick)

        await i3.main()

    def _on_event(self, conn: Connection, event: IpcBaseEvent) -> None:
        for widget in self._widgets:
            if widget.events and isinstance(event, widget.events):
                widget.process_event(event)

    def _on_tick(self, conn: Connection, event: IpcBaseEvent) -> None:
        if not isinstance(event, TickEvent):
            return

        try:
            data = json.loads(event.payload)
        except json.JSONDecodeError:
            return

        if "nobar" not in data or not isinstance(data["nobar"], dict):
            return

        command = data["nobar"]
        method_name = command.get("method")
        widget_name = command.get("widget")

        if method_name not in ALLOWED_TICK_METHODS:
            return

        for widget in self._widgets:
            if widget.name == widget_name and hasattr(widget, method_name):
                getattr(widget, method_name)()
