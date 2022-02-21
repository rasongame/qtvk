
from PyQt6.QtWidgets import QApplication
import sys

from widgets.Communicate import Communicate
from widgets.LoginWindow import LoginWindow
from widgets.MainWindow import MainWindow


app = QApplication(sys.argv)
c = Communicate()
login_window = LoginWindow(c)
main = MainWindow(c)
app.exec()
