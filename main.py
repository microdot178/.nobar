from PyQt6.QtWidgets import QApplication
import sys
from modules.info import Info
from modules.workspaces import Workspaces
from core.config import config

app = QApplication(sys.argv)

workspaces = Workspaces(config['workspaces'])
info = Info(config['info'])

app.exec()

