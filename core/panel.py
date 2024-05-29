from abc import abstractmethod

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QGuiApplication, QPalette
from PyQt6.QtWidgets import QWidget


class Panel(QWidget):
    def __init__(self, connection, config):
        super(Panel, self).__init__()
        self.setWindowFlag(Qt.WindowType.ToolTip)
        self.connection = connection

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(config["background"]))
        self.setPalette(palette)

        self.font = QFont()
        self.styleSheet = "color: {}".format(config["color"])

        self.read_config(config)
        self.show()

    def read_config(self, config):
        if "font" in config:
            self.font.setFamily(config["font"])

        if "font_size" in config:
            self.font.setPointSize(config["font_size"])

        if "fade_out" in config:
            self.mode = "fade_out"
            self.set_auto_hide_timer(config["fade_out"])

        if "fade_out_on_hover" in config:
            if config["fade_out_on_hover"]:
                self.mode = "fade_out_on_hover"

        self.config = config

    def enterEvent(self, event):
        if self.mode == "fade_out_on_hover":
            self.setWindowOpacity(0)

    def leaveEvent(self, event):
        if self.mode == "fade_out_on_hover":
            self.setWindowOpacity(1)

    def set_auto_hide_timer(self, delay_seconds):
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.setWindowOpacity(0))
        self.timer.start(delay_seconds)

    def set_position(self):
        position = self.config["position"]

        screen = QGuiApplication.primaryScreen().size()
        width = screen.width()
        height = screen.height()

        x = width - self.width() if position[0] == "right" else position[0]
        y = height - self.height() if position[1] == "bottom" else position[1]

        self.move(x, y)

    @abstractmethod
    def set_content(self, content=None):
        pass
