from PyQt6.QtWidgets import QWidget
from abc import abstractmethod
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt

class Panel(QWidget):
    def __init__(self):
        super(Panel, self).__init__()
        self.setWindowFlag(Qt.WindowType.ToolTip)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0))
        self.setPalette(palette)
        # self.setAutoFillBackground(True)

        self.font = QFont()
        self.font.setFamily('Terminus')
        self.font.setPointSize(13)

        self.styleSheet = 'color: white'

    @abstractmethod
    def update(self):
        pass

