from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout


class ProfileWindow(QWidget):
    def __init__(self, user: dict):
        super().__init__()
        self.name = QLabel()
        # self.avatar = QImage()
        self.status = QLabel()
        self.layout = QGridLayout()
        self.name.setText(f"{user['first_name']} {user['nickname']} {user['last_name']} // {user['screen_name']}")
        # self.layout.addWidget(self.avatar)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.status)

        self.setLayout(self.layout)
        self.setWindowTitle("Профиль")
        self.show()
