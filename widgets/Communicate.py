from PyQt6.QtCore import QObject, pyqtSignal


class Communicate(QObject):

    switch_chat = pyqtSignal(int)
    login_vk = pyqtSignal(str)
