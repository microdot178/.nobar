from PyQt6.QtWidgets import QWidget
from abc import abstractmethod
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt

class Panel(QWidget):
    def __init__(self, config):
        super(Panel, self).__init__()
        self.setWindowFlag(Qt.WindowType.ToolTip)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(config['background']))
        self.setPalette(palette)
        # self.setAutoFillBackground(True)

        self.font = QFont()
        self.font.setFamily(config['font'])
        self.font.setPointSize(config['font-size'])

        self.styleSheet = 'color: {}'.format(config['color'])

        self.config = config

    @abstractmethod
    def update(self):
        pass

