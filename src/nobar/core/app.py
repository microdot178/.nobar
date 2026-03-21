"""Main application class for i3 event handling."""

from __future__ import annotations

import json
from typing import Any

import i3ipc
from i3ipc import Event
from i3ipc.aio import Connection
from i3ipc.events import IpcBaseEvent, TickEvent

from nobar.core.widgets import Widgets
from nobar.interfaces.app import AppABC


class App(AppABC):
    """Core application managing i3 IPC connection and widget routing."""

    def __init__(self, arguments: Any, config: dict) -> None:
        """Initialize app with parsed arguments and configuration.

        Args:
            arguments: Parsed CLI arguments.
            config: Loaded TOML configuration dict.
        """
        self._i3: Connection | None = None
        self._connection = i3ipc.Connection()
        self._widgets = Widgets(arguments, self._connection, config).widgets

    @property
    def i3(self) -> Connection | None:
        """Async i3 IPC connection."""
        return self._i3

    @property
    def connection(self) -> i3ipc.Connection:
        """Synchronous i3 IPC connection."""
        return self._connection

    @property
    def widgets(self) -> list[Any]:
        """List of active widget instances."""
        return self._widgets

    async def start(self) -> None:
        """Connect to i3 and start the event loop."""
        self._i3 = await Connection(auto_reconnect=True).connect()

        self._i3.on(Event.WINDOW_FOCUS, self.event_handler)
        self._i3.on(Event.WORKSPACE_FOCUS, self.event_handler)
        self._i3.on(Event.WINDOW_FULLSCREEN_MODE, self.event_handler)
        self._i3.on(Event.MODE, self.event_handler)
        self._i3.on("tick", self.on_tick)

        await self._i3.main()

    def event_handler(self, conn: Connection, event: IpcBaseEvent) -> None:
        """Route i3 events to all registered widgets.

        Args:
            conn: i3 IPC connection.
            event: Incoming i3 event.
        """
        for widget in self.widgets:
            widget.process_event(event)

    def on_tick(self, conn: Connection, event: IpcBaseEvent) -> None:
        """Handle tick events for widget command execution.

        Args:
            conn: i3 IPC connection.
            event: Tick event with JSON payload.
        """
        if not isinstance(event, TickEvent):
            return

        try:
            data = json.loads(event.payload)
        except json.JSONDecodeError:
            return

        if "nobar" not in data:
            return

        command = data["nobar"]

        if not isinstance(command, dict):
            return

        for widget in self.widgets:
            if widget.name == command["widget"]:
                if hasattr(widget, command["method"]):
                    method = getattr(widget, command["method"])
                    method()
                else:
                    print(
                        f"Widget {widget.name} does not have method {command['method']}"
                    )
