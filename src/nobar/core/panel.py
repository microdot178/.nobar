"""Base panel widget with common functionality."""

from __future__ import annotations

from abc import ABCMeta, abstractmethod

import i3ipc
from i3ipc.aio import Connection
from i3ipc.events import IpcBaseEvent
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QGuiApplication, QPalette
from PyQt6.QtWidgets import QWidget

REQUIRED_CONFIG = ("height", "color", "background", "position", "screen")


class _PanelMeta(ABCMeta, type(QWidget)):
    """Metaclass resolving ABC and QWidget metaclass conflict."""


class Panel(QWidget, metaclass=_PanelMeta):
    """Base widget panel handling config, positioning, and auto-hide."""

    name: str
    events: tuple[type, ...]

    def __init__(self, connection: Connection, config: dict) -> None:
        """Initialize panel with i3 connection and widget config."""
        super().__init__()

        for key in REQUIRED_CONFIG:
            if key not in config:
                raise ValueError(f"Missing required config key: '{key}'")

        self.setWindowFlag(Qt.WindowType.ToolTip)
        self._connection = connection
        self._config = config
        self._state = "default"
        self._manually_hidden = False
        self._fade_out = "fade_out" in config
        self._fade_out_on_hover = "fade_out_on_hover" in config

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(config["background"]))
        self.setPalette(palette)

        self._font = QFont()
        self._style_sheet = f"color: {config['color']}"

        if "font" in config:
            self._font.setFamily(config["font"])

        if "font_size" in config:
            self._font.setPointSize(config["font_size"])

        self._auto_hide_timer: QTimer | None = None
        if self._fade_out:
            self._auto_hide_timer = QTimer(self)
            self._auto_hide_timer.timeout.connect(self.hide)
            self._auto_hide_timer.start(config["fade_out"])

    async def init(self) -> None:
        """Perform async initialization after construction."""
        await self.set_content()
        self.show()

    def set_position(self) -> None:
        """Position the panel on screen based on config."""
        position = self._config["position"]
        screen = self._config["screen"]

        geometry = QGuiApplication.screens()[screen].geometry()
        screen_right = geometry.x() + geometry.width()
        screen_bottom = geometry.y() + geometry.height()

        x = screen_right - self.width() if position[0] == "right" else position[0]
        y = screen_bottom - self.height() if position[1] == "bottom" else position[1]

        self.move(x, y)

    async def handle_fullscreen_mode(self) -> None:
        """Hide or show panel based on fullscreen state."""
        outputs = await self._connection.get_outputs()
        tree = await self._connection.get_tree()
        screen = self._config["screen"]

        for workspace in tree.workspaces():
            if workspace.name == outputs[screen].current_workspace:
                if any(con.fullscreen_mode != 0 for con in workspace.leaves()):
                    self.hide()
                elif not self._manually_hidden:
                    self.show()
                    await self.set_content()

    async def toggle(self) -> None:
        """Toggle panel visibility with manual hide tracking."""
        if self._manually_hidden:
            self._manually_hidden = False
            self.show()
            await self.set_content()
        else:
            self._manually_hidden = True
            self.hide()

    async def process_event(self, event: IpcBaseEvent) -> None:
        """Handle fullscreen and workspace events."""
        is_workspace = isinstance(event, i3ipc.WorkspaceEvent)
        is_fullscreen = (
            isinstance(event, i3ipc.WindowEvent) and event.change == "fullscreen_mode"
        )

        if is_workspace or is_fullscreen:
            await self.handle_fullscreen_mode()

    @abstractmethod
    async def set_content(self) -> None:
        """Update widget content."""
