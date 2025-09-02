from typing import List

import i3ipc
from i3ipc import ModeEvent, WindowEvent, WorkspaceEvent
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QGuiApplication, QPalette
from PyQt6.QtWidgets import QWidget

from interfaces.panel import PanelABC, PanelMeta


class Panel(PanelABC, QWidget, metaclass=PanelMeta):
    def __init__(self, connection, config):
        super(Panel, self).__init__()
        self.setWindowFlag(Qt.WindowType.ToolTip)
        self._connection = connection

        self._state = "default"
        self._options = []

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(config["background"]))
        self.setPalette(palette)

        self.font = QFont()
        self.styleSheet = "color: {}".format(config["color"])

        self.read_config(config)
        self.show()

    @property
    def config(self) -> dict:
        return self._config

    @property
    def connection(self) -> i3ipc.Connection:
        return self._connection

    @property
    def state(self) -> str:
        return self._state

    @property
    def options(self) -> List[str]:
        return self._options

    def read_config(self, config):
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

    def set_auto_hide_timer(self, delay_seconds):
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.hide())
        self.timer.start(delay_seconds)

    def set_position(self):
        position = self.config["position"]

        screen = QGuiApplication.primaryScreen().size()
        width = screen.width()
        height = screen.height()

        x = width - self.width() if position[0] == "right" else position[0]
        y = height - self.height() if position[1] == "bottom" else position[1]

        self.move(x, y)

    def process_event(self, event):
        if isinstance(event, WindowEvent):
            if event.container.fullscreen_mode:
                self.hide()
            else:
                self.show()
                self.set_content()

        if isinstance(event, ModeEvent):
            self._state = event.change

            self.set_content()

        if isinstance(event, WorkspaceEvent):
            self.set_content()
