
from PyQt6.QtWidgets import QApplication
import sys

from widgets.MainWindow import MainWindow

TOKEN = ""

app = QApplication(sys.argv)
window = MainWindow(TOKEN)
app.exec()
