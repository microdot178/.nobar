"""Abstract interface for the main application."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import i3ipc
from i3ipc.aio import Connection
from i3ipc.events import IpcBaseEvent


class AppABC(ABC):
    """Abstract base class defining the application interface."""

    @property
    @abstractmethod
    def i3(self) -> Connection | None:
        """Async i3 IPC connection."""

    @property
    @abstractmethod
    def connection(self) -> i3ipc.Connection:
        """Synchronous i3 IPC connection."""

    @property
    @abstractmethod
    def widgets(self) -> list[Any]:
        """List of active widget instances."""

    @abstractmethod
    async def start(self) -> None:
        """Connect to i3 and start the event loop."""

    @abstractmethod
    def event_handler(self, conn: Connection, event: IpcBaseEvent) -> None:
        """Route i3 events to widgets."""

    @abstractmethod
    def on_tick(self, conn: Connection, event: IpcBaseEvent) -> None:
        """Handle tick events for widget commands."""
