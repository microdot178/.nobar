from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
import i3ipc
from core.panel import Panel

class Workspace(QWidget):
    def __init__(self, workspace, config):
        super(Workspace, self).__init__()

        color = config['color']
        focused = config['focused']
        height = config['height']

        styleSheet = 'color: {}'.format(focused if workspace.focused else color)

        self.label = QLabel(workspace.name, self)
        self.label.setStyleSheet(styleSheet)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setGeometry(0, 0, height, height)

        self.setFixedSize(height, height)

class Workspaces(Panel):
    def __init__(self, config):
        super(Workspaces, self).__init__(config)
        self.setWindowTitle('microbar_workspaces')

    def update(self):
        i3 = i3ipc.Connection()
        workspaces = i3.get_workspaces()

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        for workspace in workspaces:
            widget = Workspace(workspace, self.config)
            widget.label.setFont(self.font)

            layout.addWidget(widget)

        self.setLayout(layout)
        self.show()

