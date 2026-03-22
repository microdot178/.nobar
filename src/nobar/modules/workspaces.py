"""Workspace navigation widget displaying i3 workspaces."""

from __future__ import annotations

import i3ipc
from i3ipc import WindowEvent, WorkspaceEvent
from i3ipc.events import IpcBaseEvent
from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QEnterEvent, QFont, QMouseEvent
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget

from nobar.core.panel import Panel


class Workspace(QWidget):
    """Single clickable workspace button."""

    def __init__(
        self,
        connection: i3ipc.Connection,
        workspace: i3ipc.WorkspaceReply,
        config: dict,
        font: QFont,
    ) -> None:
        """Initialize workspace button."""
        super().__init__()
        self._connection = connection
        self._name = workspace.name

        height = config["height"]
        color = config["focused"] if workspace.focused else config["color"]

        self._label = QLabel(workspace.name, self)
        self._label.setFont(font)
        self._label.setStyleSheet(f"color: {color}")
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setGeometry(0, 0, height, height)

        self.setFixedSize(height, height)

    def mousePressEvent(self, a0: QMouseEvent | None) -> None:  # noqa: N802
        """Switch to this workspace on click."""
        self._connection.command(f"workspace {self._name}")


class Workspaces(Panel):
    """Panel widget displaying all i3 workspaces as clickable buttons."""

    name = "workspaces"
    events = (WorkspaceEvent, WindowEvent)

    def __init__(self, connection: i3ipc.Connection, config: dict) -> None:
        """Initialize workspaces panel."""
        super().__init__(connection, config)
        self.setWindowTitle("nobar_workspaces")

        self._box_layout = QHBoxLayout()
        self._box_layout.setSpacing(0)
        self._box_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self._box_layout)
        self.set_content()
        self.show()

    def set_content(self) -> None:
        """Rebuild workspace buttons from current i3 state."""

        def sort_key(ws: i3ipc.WorkspaceReply) -> tuple[int, int | str]:
            try:
                return (0, int(ws.name))
            except ValueError:
                return (1, ws.name)

        workspaces = sorted(self._connection.get_workspaces(), key=sort_key)

        for i in reversed(range(self._box_layout.count())):
            self._box_layout.itemAt(i).widget().setParent(None)

        for ws in workspaces:
            widget = Workspace(self._connection, ws, self._config, self._font)
            self._box_layout.addWidget(widget)

        if self._auto_hide_timer:
            self._auto_hide_timer.setInterval(self._config["fade_out"])

        self.adjustSize()
        self.set_position()

    def process_event(self, event: IpcBaseEvent) -> None:
        """Rebuild workspace buttons on workspace events."""
        if isinstance(event, WorkspaceEvent):
            if not self._manually_hidden:
                self.show()
            self.set_content()
            if self._auto_hide_timer:
                self._auto_hide_timer.start(self._config["fade_out"])

        super().process_event(event)

    def enterEvent(self, event: QEnterEvent | None) -> None:  # noqa: N802
        """Stop auto-hide timer on mouse enter."""
        if self._auto_hide_timer:
            self._auto_hide_timer.stop()

    def leaveEvent(self, a0: QEvent | None) -> None:  # noqa: N802
        """Restart auto-hide timer on mouse leave."""
        if self._auto_hide_timer:
            self._auto_hide_timer.start(self._config["fade_out"])
