from PyQt6.QtWidgets import QHBoxLayout, QLabel
from PyQt6.QtCore import QTimer, QDateTime
import psutil
from xkbgroup import XKeyboard
from core.panel import Panel


class Info(Panel):
    def __init__(self, connection, config):
        super(Info, self).__init__(connection, config)
        self.setWindowTitle("microbar_info")

        self.label = QLabel()
        self.label.setFont(self.font)
        self.label.setStyleSheet(self.styleSheet)

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.set_content)
        self.timer.start(1000)

        self.setFixedHeight(self.config["height"])

    def set_content(self, event=None):
        connection = self.connection
        focused_workspace = connection.get_tree().find_focused().workspace().name

        info = focused_workspace
        layout = XKeyboard().group_symbol.upper()
        percentage = round(psutil.sensors_battery().percent)
        time = QDateTime.currentDateTime().toString("hh:mm:ss")

        label = "{0} {1} {2} {3}".format(info, layout, percentage, time)

        self.label.setText(label)

        self.adjustSize()
        self.set_position()
