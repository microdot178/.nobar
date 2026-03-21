"""System info widget displaying workspace, layout, battery, and time."""

from __future__ import annotations

import i3ipc
import psutil
from i3ipc import ModeEvent
from i3ipc.events import IpcBaseEvent
from PyQt6.QtCore import QDateTime, QTimer
from PyQt6.QtGui import QEnterEvent
from PyQt6.QtWidgets import QHBoxLayout, QLabel
from xkbgroup import XKeyboard

from nobar.core.panel import Panel


class Info(Panel):
    """Panel widget showing system information."""

    def __init__(self, connection: i3ipc.Connection, config: dict) -> None:
        """Initialize info widget with label and update timer.

        Args:
            connection: Synchronous i3 IPC connection.
            config: Widget-specific configuration dict.
        """
        super().__init__(connection, config)
        self.name = "info"
        self.setWindowTitle("nobar_info")

        self.label = QLabel()
        self.label.setFont(self.font)
        self.label.setStyleSheet(self.styleSheet)

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.set_content)
        self.timer.start(1000)

        self.setFixedHeight(self.config["height"])
        self.set_content()

    def set_content(self) -> None:
        """Update label with current workspace, layout, battery, and time."""
        connection = self.connection
        focused_workspace = connection.get_tree().find_focused().workspace().name

        layout = XKeyboard().group_symbol.upper()
        percentage = round(psutil.sensors_battery().percent)
        time = QDateTime.currentDateTime().toString("hh:mm:ss")

        if self.state == "resize":
            info = self.state
        else:
            info = focused_workspace

        label = f"{info} {layout} {percentage} {time}"

        self.label.setText(label)

        self.adjustSize()
        self.set_position()

    def process_event(self, event: IpcBaseEvent) -> None:
        """Handle mode change events to display resize state.

        Args:
            event: Incoming i3 event.
        """
        match event:
            case ModeEvent():
                self._state = event.change
                self.set_content()

        super().process_event(event)

    def enterEvent(self, event: QEnterEvent | None) -> None:  # noqa: N802
        """Hide widget on mouse enter when fade_out_on_hover is enabled."""
        if "fade_out_on_hover" in self.options:
            self.setWindowOpacity(0)

    def leaveEvent(self, a0: QEnterEvent | None) -> None:  # noqa: N802
        """Show widget on mouse leave when fade_out_on_hover is enabled."""
        if "fade_out_on_hover" in self.options:
            self.setWindowOpacity(1)
