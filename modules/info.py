from PyQt6.QtWidgets import QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer, QDateTime
from core.panel import Panel

class Info(Panel):
    def __init__(self):
        super(Info, self).__init__()
        self.setWindowTitle('microbar_info')

        # self.setWindowRole('microbar_info')

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel()
        self.label.setFont(self.font)
        self.label.setStyleSheet(self.styleSheet)
        self.layout.addWidget(self.label)

        self.update()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def update(self):
        print('updated: info')

        time = QDateTime.currentDateTime().toString('hh:mm:ss')

        self.label.setText(time)