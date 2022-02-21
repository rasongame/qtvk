from PyQt6.QtWidgets import QDialog, QGridLayout, QLineEdit, QPushButton, QCheckBox

import utils
from widgets.Communicate import Communicate


class LoginWindow(QDialog):
    def read_token(self):
        with open("secret.txt", 'r') as file:
            r = file.read()
            return r

    def submit_data(self):
        token = self.tokenEdit.text()
        if self.saveTokenCheckBox.isChecked():
            with open("secret.txt", 'w') as file:
                file.write(token)
        self.c.login_vk.emit(token)
        self.close()

    def __init__(self, communicate=Communicate()):
        super().__init__()
        self.c = communicate
        self.layout = QGridLayout()
        self.tokenEdit = QLineEdit()
        self.tokenEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.submitButton = QPushButton()
        self.submitButton.setText("Я хочу слить свои персональные данные")
        token = self.read_token()
        if len(token) != 0:
            self.tokenEdit.setText(token)

        self.tokenEdit.setPlaceholderText("Вставь токен")
        self.saveTokenCheckBox = QCheckBox("Сохранить токен")
        self.layout.addWidget(self.tokenEdit, 1, 0)
        self.layout.addWidget(self.saveTokenCheckBox, 2, 0)
        self.layout.addWidget(self.submitButton, 3, 0)

        self.submitButton.clicked.connect(self.submit_data)
        self.setWindowTitle(utils.build_window_title("QtVK", "Авторизация"))
        self.setLayout(self.layout)
        self.show()
