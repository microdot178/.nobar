"""Main application class for i3 event handling."""

from __future__ import annotations

import argparse
import json

from i3ipc import Event
from i3ipc.aio import Connection
from i3ipc.events import IpcBaseEvent, TickEvent

from nobar.core.widgets import create_widgets

ALLOWED_TICK_METHODS = {"toggle", "set_content"}


class App:
    """Core application managing i3 IPC connection and widget routing."""

    def __init__(self, arguments: argparse.Namespace, config: dict) -> None:
        """Initialize app with parsed arguments and configuration."""
        self._arguments = arguments
        self._config = config

    async def start(self) -> None:
        """Connect to i3 and start the event loop."""
        connection = await Connection(auto_reconnect=True).connect()
        self._widgets = await create_widgets(self._arguments, connection, self._config)

        connection.on(Event.WINDOW_FOCUS, self._on_event)  # type: ignore[arg-type]
        connection.on(Event.WORKSPACE_FOCUS, self._on_event)  # type: ignore[arg-type]
        connection.on(Event.WINDOW_FULLSCREEN_MODE, self._on_event)  # type: ignore[arg-type]
        connection.on(Event.MODE, self._on_event)  # type: ignore[arg-type]
        connection.on("tick", self._on_tick)  # type: ignore[arg-type]

        await connection.main()

    async def _on_event(self, conn: Connection, event: IpcBaseEvent) -> None:
        for widget in self._widgets:
            if widget.events and isinstance(event, widget.events):
                await widget.process_event(event)

    async def _on_tick(self, conn: Connection, event: IpcBaseEvent) -> None:
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
                await getattr(widget, method_name)()
