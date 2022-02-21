import urllib

from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel, QGridLayout, QDialog

import utils


class ProfileWindow(QDialog):

    def __init__(self, user: dict):
        super().__init__()
        data = urllib.request.urlopen(user['photo_200_orig']).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)

        self.name = QLabel()
        self.avatar = QLabel()
        self.status = QLabel()
        self.layout = QGridLayout()



        self.name.setText(f"{user['first_name']} {user['last_name']} // {user['screen_name']}")
        self.status.setText(user['status'])
        self.avatar.setPixmap(pixmap)
        self.layout.addWidget(self.avatar, 1,0 )
        self.layout.addWidget(self.name, 2, 0)
        self.layout.addWidget(self.status, 3, 0)

        self.setLayout(self.layout)
        self.setWindowTitle(utils.build_window_title("QtVK", "Профиль"))
        print("open profile")
        self.exec()

