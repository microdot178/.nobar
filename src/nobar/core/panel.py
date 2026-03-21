"""Base panel widget with common functionality."""

from __future__ import annotations

import i3ipc
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QEnterEvent, QFont, QGuiApplication, QPalette
from PyQt6.QtWidgets import QWidget

from nobar.interfaces.panel import PanelABC, PanelMeta


class Panel(PanelABC, QWidget, metaclass=PanelMeta):
    """Base widget panel handling config, positioning, and auto-hide."""

    def __init__(self, connection: i3ipc.Connection, config: dict) -> None:
        """Initialize panel with i3 connection and widget config.

        Args:
            connection: Synchronous i3 IPC connection.
            config: Widget-specific configuration dict.
        """
        super().__init__()
        self.setWindowFlag(Qt.WindowType.ToolTip)
        self._connection = connection

        self._state = "default"
        self._options: list[str] = []

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(config["background"]))
        self.setPalette(palette)

        self.font = QFont()
        self.styleSheet = f"color: {config['color']}"

        self.read_config(config)
        self.show()

    @property
    def config(self) -> dict:
        """Widget configuration dict."""
        return self._config

    @property
    def connection(self) -> i3ipc.Connection:
        """Synchronous i3 IPC connection."""
        return self._connection

    @property
    def state(self) -> str:
        """Current widget state."""
        return self._state

    @property
    def options(self) -> list[str]:
        """Active widget options."""
        return self._options

    def read_config(self, config: dict) -> None:
        """Apply configuration options to the panel.

        Args:
            config: Widget-specific configuration dict.
        """
        if "font" in config:
            self.font.setFamily(config["font"])

        if "font_size" in config:
            self.font.setPointSize(config["font_size"])

        if "fade_out" in config:
            self.options.append("fade_out")
            self.set_auto_hide_timer(config["fade_out"])

        if "fade_out_on_hover" in config:
            self.options.append("fade_out_on_hover")

        self._config = config

    def set_auto_hide_timer(self, delay_seconds: int) -> None:
        """Set up a timer to auto-hide the panel.

        Args:
            delay_seconds: Delay in milliseconds before hiding.
        """
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.hide())
        self.timer.start(delay_seconds)

    def set_position(self) -> None:
        """Position the panel on screen based on config."""
        position = self.config["position"]
        screen = self.config["screen"]

        geometry = QGuiApplication.screens()[screen].geometry()
        width = geometry.x() + geometry.width()
        height = geometry.y() + geometry.height()

        x = width - self.width() if position[0] == "right" else position[0]
        y = height - self.height() if position[1] == "bottom" else position[1]

        self.move(x, y)

    def handle_fullscreen_mode(self) -> None:
        """Hide panel when a window is fullscreen on the same screen."""
        outputs = self.connection.get_outputs()
        tree = self.connection.get_tree()
        screen = self.config["screen"]

        for workspace in tree.workspaces():
            if workspace.name == outputs[screen].current_workspace:
                if any(con.fullscreen_mode != 0 for con in workspace.leaves()):
                    self.hide()
                else:
                    self.show()
                    self.set_content()

    def process_event(self, event: i3ipc.events.IpcBaseEvent) -> None:
        """Handle common events for all panel-type widgets.

        Args:
            event: Incoming i3 event.
        """
        self.handle_fullscreen_mode()

    def enterEvent(self, event: QEnterEvent | None) -> None:  # noqa: N802
        """Handle mouse enter event."""

    def leaveEvent(self, a0: QEnterEvent | None) -> None:  # noqa: N802
        """Handle mouse leave event."""
