"""Abstract interface for panel widgets."""

from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod

import i3ipc
from i3ipc.events import IpcBaseEvent
from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QEnterEvent
from PyQt6.QtWidgets import QWidget


class PanelMeta(ABCMeta, type(QWidget)):
    """Metaclass resolving ABC and QWidget metaclass conflict."""


class PanelABC(ABC):
    """Abstract base class defining the panel widget interface."""

    @property
    @abstractmethod
    def config(self) -> dict:
        """Widget configuration dict."""

    @property
    @abstractmethod
    def connection(self) -> i3ipc.Connection:
        """Synchronous i3 IPC connection."""

    @property
    @abstractmethod
    def state(self) -> str:
        """Current widget state."""

    @property
    @abstractmethod
    def options(self) -> list[str]:
        """Active widget options."""

    @abstractmethod
    def read_config(self, config: dict) -> None:
        """Apply configuration options."""

    @abstractmethod
    def set_auto_hide_timer(self, delay_seconds: int) -> None:
        """Set up auto-hide timer."""

    @abstractmethod
    def set_position(self) -> None:
        """Position widget on screen."""

    @abstractmethod
    def set_content(self) -> None:
        """Update widget content."""

    @abstractmethod
    def process_event(self, event: IpcBaseEvent) -> None:
        """Handle incoming i3 event."""

    @abstractmethod
    def handle_fullscreen_mode(self) -> None:
        """Handle fullscreen mode changes."""

    @abstractmethod
    def enterEvent(self, event: QEnterEvent | None) -> None:  # noqa: N802
        """Handle mouse enter event."""

    @abstractmethod
    def leaveEvent(self, a0: QEvent | None) -> None:  # noqa: N802
        """Handle mouse leave event."""
