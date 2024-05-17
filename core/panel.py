from PyQt6.QtWidgets import QWidget
from abc import abstractmethod
from PyQt6.QtGui import QGuiApplication, QFont, QPalette, QColor
from PyQt6.QtCore import Qt


class Panel(QWidget):
    def __init__(self, config):
        super(Panel, self).__init__()
        self.setWindowFlag(Qt.WindowType.ToolTip)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(config["background"]))
        self.setPalette(palette)
        # self.setAutoFillBackground(True)

        self.font = QFont()
        self.styleSheet = "color: {}".format(config["color"])
        self.config = config

        if "font" in config:
            self.font.setFamily(config["font"])

        if "font-size" in config:
            self.font.setPointSize(config["font-size"])

        self.show()

    def set_position(self):
        position = self.config["position"]

        screen = QGuiApplication.primaryScreen().size()
        width = screen.width()
        height = screen.height()

        x = width - self.width() if position[0] == "right" else position[0]
        y = height - self.height() if position[1] == "bottom" else position[1]

        self.move(x, y)
        self.adjustSize()

    @abstractmethod
    def set_content(self, content=None):
        pass
