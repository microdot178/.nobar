from PyQt6.QtWidgets import QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer, QDateTime
import psutil
from core.panel import Panel

class Info(Panel):
    def __init__(self, config):
        super(Info, self).__init__(config)
        self.setWindowTitle('microbar_info')

        self.label = QLabel()
        self.label.setFont(self.font)
        self.label.setStyleSheet(self.styleSheet)

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000) 

    def update(self):
        # print('updated: info', self.label.width())

        percentage = psutil.sensors_battery().percent
        time = QDateTime.currentDateTime().toString('hh:mm:ss')

        self.label.setText('{0} {1}'.format(percentage, time))

        self.move(1920 - self.width(), 0)
        self.show()

