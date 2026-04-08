"""System info widget composing individual labels."""

from __future__ import annotations

import asyncio

from i3ipc import ModeEvent, WindowEvent, WorkspaceEvent
from i3ipc.aio import Connection
from i3ipc.events import IpcBaseEvent
from PyQt6.QtCore import QEvent, QTimer
from PyQt6.QtGui import QEnterEvent
from PyQt6.QtWidgets import QHBoxLayout

from nobar.core.panel import Panel
from nobar.modules.info.battery import BatteryLabel
from nobar.modules.info.clock import ClockLabel
from nobar.modules.info.keyboard import KeyboardLabel
from nobar.modules.info.workspace import WorkspaceLabel


class Info(Panel):
    """Panel widget showing system information."""

    name = "info"
    events = (ModeEvent, WindowEvent, WorkspaceEvent)

    def __init__(self, connection: Connection, config: dict) -> None:
        """Initialize info widget with individual labels."""
        super().__init__(connection, config)
        self.setWindowTitle("nobar_info")

        self._focused_workspace = "?"

        self._workspace = WorkspaceLabel(self._font, self._style_sheet)
        self._keyboard = KeyboardLabel(self._font, self._style_sheet)
        self._battery = BatteryLabel(self._font, self._style_sheet, config)
        self._clock = ClockLabel(self._font, self._style_sheet)

        _layout = QHBoxLayout()
        _layout.setSpacing(8)
        _layout.addWidget(self._workspace)
        _layout.addWidget(self._keyboard)
        _layout.addWidget(self._battery)
        _layout.addWidget(self._clock)
        self.setLayout(_layout)

        self._update_timer = QTimer(self)
        self._update_timer.timeout.connect(
            lambda: asyncio.ensure_future(self.set_content())
        )
        self._update_timer.start(1000)

        self.setFixedHeight(self._config["height"])

    async def init(self) -> None:
        """Fetch initial workspace and populate content."""
        tree = await self._connection.get_tree()
        focused = tree.find_focused()
        self._focused_workspace = focused.workspace().name if focused else "?"
        await self.set_content()
        self.show()

    async def set_content(self) -> None:
        """Update all info labels."""
        self._workspace.update_content(self._focused_workspace, self._state)
        self._keyboard.update_content()
        self._battery.update_content()
        self._clock.update_content()
        self.adjustSize()
        self.set_position()

    async def process_event(self, event: IpcBaseEvent) -> None:
        """Handle mode and workspace events."""
        if isinstance(event, ModeEvent):
            self._state = event.change

        if isinstance(event, WorkspaceEvent):
            self._focused_workspace = event.current.name

        if isinstance(event, (ModeEvent, WorkspaceEvent)):
            await self.set_content()

        await super().process_event(event)

    def enterEvent(self, event: QEnterEvent | None) -> None:  # noqa: N802
        """Hide widget on mouse hover."""
        if self._fade_out_on_hover:
            self.setWindowOpacity(0)

    def leaveEvent(self, a0: QEvent | None) -> None:  # noqa: N802
        """Show widget when mouse leaves."""
        if self._fade_out_on_hover:
            self.setWindowOpacity(1)
