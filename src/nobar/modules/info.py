"""System info widget displaying workspace, layout, battery, and time."""

from __future__ import annotations

import i3ipc
import psutil
from i3ipc import ModeEvent, WindowEvent, WorkspaceEvent
from i3ipc.events import IpcBaseEvent
from PyQt6.QtCore import QDateTime, QEvent, QTimer
from PyQt6.QtGui import QEnterEvent
from PyQt6.QtWidgets import QHBoxLayout, QLabel
from xkbgroup import XKeyboard

from nobar.core.panel import Panel


class Info(Panel):
    """Panel widget showing system information."""

    name = "info"
    events = (ModeEvent, WindowEvent, WorkspaceEvent)

    def __init__(self, connection: i3ipc.Connection, config: dict) -> None:
        """Initialize info widget with label and update timer."""
        super().__init__(connection, config)
        self.setWindowTitle("nobar_info")

        self._xkb = XKeyboard()

        tree = self._connection.get_tree()
        focused = tree.find_focused()
        self._focused_workspace = focused.workspace().name if focused else "?"

        self._label = QLabel()
        self._label.setFont(self._font)
        self._label.setStyleSheet(self._style_sheet)

        _layout = QHBoxLayout()
        _layout.addWidget(self._label)
        self.setLayout(_layout)

        self._update_timer = QTimer(self)
        self._update_timer.timeout.connect(self.set_content)
        self._update_timer.start(1000)

        self.setFixedHeight(self._config["height"])
        self.set_content()
        self.show()

    def set_content(self) -> None:
        """Update label with current system info."""
        if not self.isVisible():
            return

        keyboard_layout = self._xkb.group_symbol.upper()

        battery = psutil.sensors_battery()
        percentage = round(battery.percent) if battery else "?"

        time = QDateTime.currentDateTime().toString("hh:mm:ss")

        if self._state == "resize":
            info = self._state
        else:
            info = self._focused_workspace

        self._label.setText(f"{info} {keyboard_layout} {percentage} {time}")
        self.adjustSize()
        self.set_position()

    def process_event(self, event: IpcBaseEvent) -> None:
        """Handle mode and workspace events."""
        if isinstance(event, ModeEvent):
            self._state = event.change

        if isinstance(event, WorkspaceEvent):
            self._focused_workspace = event.current.name

        if isinstance(event, (ModeEvent, WorkspaceEvent)):
            self.set_content()

        super().process_event(event)

    def enterEvent(self, event: QEnterEvent | None) -> None:  # noqa: N802
        """Hide widget on mouse hover."""
        if self._fade_out_on_hover:
            self.setWindowOpacity(0)

    def leaveEvent(self, a0: QEvent | None) -> None:  # noqa: N802
        """Show widget when mouse leaves."""
        if self._fade_out_on_hover:
            self.setWindowOpacity(1)
