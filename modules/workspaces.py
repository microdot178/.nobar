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

        styleSheet = f"color: {focused if workspace.focused else color}"

        self.label = QLabel(workspace.name, self)
        self.label.setStyleSheet(styleSheet)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(0, 0, height, height)

        self.setFixedSize(height, height)

    def mousePressEvent(self, a0):
        self.connection.command(f"workspace {self.name}")


class Workspaces(Panel):
    def __init__(self, connection, config):
        super(Workspaces, self).__init__(connection, config)
        self.name = "workspaces"
        self.setWindowTitle("nobar_workspaces")

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)
        self.set_content()

    def set_content(self):
        def sort_key(workspace):
            try:
                return (0, int(workspace.name))
            except ValueError:
                return (1, workspace.name)

        workspaces = sorted(self.connection.get_workspaces(), key=sort_key)

        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        for workspace in workspaces:
            widget = Workspace(workspace, self.config)
            widget.label.setFont(self.font)
            widget.connection = self.connection

            self.layout.addWidget(widget)

        if "fade_out" in self.options:
            delay_seconds = self.config["fade_out"]

            self.timer.setInterval(delay_seconds)

        if self.isHidden():
            self.show()

        self.adjustSize()
        self.set_position()

    def enterEvent(self, event):
        if "fade_out" in self.options:
            self.timer.stop()

    def leaveEvent(self, a0):
        if "fade_out" in self.options:
            delay_seconds = self.config["fade_out"]

            self.timer.start(delay_seconds)
