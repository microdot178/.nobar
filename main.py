from PyQt6.QtWidgets import QApplication
import sys
from modules.info import Info

app = QApplication(sys.argv)

panel = Info() 

app.exec()

