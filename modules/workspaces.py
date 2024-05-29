from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget

from core.panel import Panel


class Workspace(QWidget):
    def __init__(self, workspace, config):
        super(Workspace, self).__init__()
        self.name = workspace.name

        color = config["color"]
        focused = config["focused"]
        height = config["height"]

        styleSheet = "color: {}".format(focused if workspace.focused else color)

        self.label = QLabel(workspace.name, self)
        self.label.setStyleSheet(styleSheet)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(0, 0, height, height)

        self.setFixedSize(height, height)

    def mousePressEvent(self, event):
        self.connection.command(f"workspace {self.name}")


class Workspaces(Panel):
    def __init__(self, connection, config):
        super(Workspaces, self).__init__(connection, config)
        self.setWindowTitle("microbar_workspaces")

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)

    def set_content(self):
        workspaces = self.connection.get_workspaces()

        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        for workspace in workspaces:
            widget = Workspace(workspace, self.config)
            widget.label.setFont(self.font)
            widget.connection = self.connection

            self.layout.addWidget(widget)

        if self.mode == "fade_out":
            delay_seconds = self.config["fade_out"]

            self.timer.setInterval(delay_seconds)

        if not self.windowOpacity():
            self.setWindowOpacity(1)

        self.adjustSize()
        self.set_position()
