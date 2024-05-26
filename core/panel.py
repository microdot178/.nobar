from PyQt6.QtWidgets import QWidget
from abc import abstractmethod
from PyQt6.QtGui import QGuiApplication, QFont, QPalette, QColor
from PyQt6.QtCore import Qt, QTimer


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

        if "font-size" in config:
            self.font.setPointSize(config["font-size"])

        if "fade-out" in config:
            self.mode = "fade-out"
            self.set_auto_hide_timer(config["fade-out"])

        if "fade-out-on-hover" in config:
            if config["fade-out-on-hover"]:
                self.mode = "fade-out-on-hover"

        self.config = config

    def enterEvent(self, event):
        if self.mode == "fade-out-on-hover":
            self.setWindowOpacity(0)

    def leaveEvent(self, event):
        if self.mode == "fade-out-on-hover":
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
