"""Workspace navigation widget displaying i3 workspaces."""

from __future__ import annotations

import i3ipc
from i3ipc import WorkspaceEvent
from i3ipc.events import IpcBaseEvent
from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QEnterEvent, QMouseEvent
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget

from nobar.core.panel import Panel


class Workspace(QWidget):
    """Single clickable workspace button."""

    def __init__(self, workspace: i3ipc.WorkspaceReply, config: dict) -> None:
        """Initialize workspace button with label and styling.

        Args:
            workspace: i3 workspace reply object.
            config: Widget-specific configuration dict.
        """
        super().__init__()
        self.name = workspace.name

        color = config["color"]
        focused = config["focused"]
        height = config["height"]

        style_sheet = f"color: {focused if workspace.focused else color}"

        self.label = QLabel(workspace.name, self)
        self.label.setStyleSheet(style_sheet)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(0, 0, height, height)

        self.setFixedSize(height, height)

    def mousePressEvent(self, a0: QMouseEvent | None) -> None:  # noqa: N802
        """Switch to this workspace on click."""
        self.connection.command(f"workspace {self.name}")


class Workspaces(Panel):
    """Panel widget displaying all i3 workspaces as clickable buttons."""

    def __init__(self, connection: i3ipc.Connection, config: dict) -> None:
        """Initialize workspaces panel with horizontal layout.

        Args:
            connection: Synchronous i3 IPC connection.
            config: Widget-specific configuration dict.
        """
        super().__init__(connection, config)
        self.name = "workspaces"
        self.setWindowTitle("nobar_workspaces")

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)
        self.set_content()

    def set_content(self) -> None:
        """Rebuild workspace buttons from current i3 state."""

        def sort_key(workspace: i3ipc.WorkspaceReply) -> tuple[int, int | str]:
            try:
                return (0, int(workspace.name))
            except ValueError:
                return (1, workspace.name)

        workspaces = sorted(self.connection.get_workspaces(), key=sort_key)

        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        for workspace in workspaces:
            widget = Workspace(workspace, self.config)
            widget.label.setFont(self.font)
            widget.connection = self.connection

            self.layout.addWidget(widget)

        if "fade_out" in self.options:
            delay_seconds = self.config["fade_out"]

            self.timer.setInterval(delay_seconds)

        self.adjustSize()
        self.set_position()

    def process_event(self, event: IpcBaseEvent) -> None:
        """Rebuild workspace buttons on workspace events.

        Args:
            event: Incoming i3 event.
        """
        match event:
            case WorkspaceEvent():
                self.set_content()

        super().process_event(event)

    def enterEvent(self, event: QEnterEvent | None) -> None:  # noqa: N802
        """Stop auto-hide timer on mouse enter."""
        if "fade_out" in self.options:
            self.timer.stop()

    def leaveEvent(self, a0: QEvent | None) -> None:  # noqa: N802
        """Restart auto-hide timer on mouse leave."""
        if "fade_out" in self.options:
            delay_seconds = self.config["fade_out"]

            self.timer.start(delay_seconds)
