from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
import i3ipc
from core.panel import Panel

class Workspace(QWidget):
    def __init__(self, workspace):
        super(Workspace, self).__init__()

        styleSheet = 'color: {}'.format('white' if workspace.focused else 'gray')

        self.label = QLabel(workspace.name, self)
        self.label.setStyleSheet(styleSheet)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(0, 0, 50, 50)

        self.setFixedSize(50, 50)

class Workspaces(Panel):
    def __init__(self):
        super(Workspaces, self).__init__()
        self.setWindowTitle('microbar_workspaces')

    def update(self):
        i3 = i3ipc.Connection()
        workspaces = i3.get_workspaces()

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        for workspace in workspaces:
            widget = Workspace(workspace)
            widget.label.setFont(self.font)

            layout.addWidget(widget)

        self.setLayout(layout)
        self.show()

