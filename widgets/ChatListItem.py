from PyQt6 import QtGui
from PyQt6.QtWidgets import QListWidgetItem, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QGridLayout

from widgets.Communicate import Communicate


class ChatListItem(QWidget):
    def __init__(self, chat_name, last_message_text="", communicate=Communicate()):
        super(ChatListItem, self).__init__()
        self.peer_id = chat_name

        self.label = QLabel()
        self.last_message_text = QLabel()
        self.label.setText(chat_name)
        self.last_message_text.setText(last_message_text)
        self.c = communicate
        self.layout = QGridLayout()
        self.layout.addWidget(self.label, 0, 0)
        self.layout.addWidget(self.last_message_text, 1, 0)
        # self.setStyleSheet(stylesheet)
        self.setLayout(self.layout)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        print("switch chat")
        self.c.switch_chat.emit(self.getPeerID())

    def setTitle(self, text: str):
        return self.label.setText(text)

    def setPeerID(self, peer_id: int):
        self.peer_id = peer_id

    def getPeerID(self):
        return self.peer_id
