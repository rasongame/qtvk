from PyQt6 import QtGui
from PyQt6.QtWidgets import QListWidgetItem, QVBoxLayout, QLabel, QWidget, QHBoxLayout

from widgets.Communicate import Communicate


class ChatListItem(QWidget):
    def __init__(self, chat_name, communicate=Communicate()):
        super(ChatListItem, self).__init__()
        self.peer_id = chat_name

        self.label = QLabel()
        self.label.setText(chat_name)
        self.c = communicate
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        stylesheet = \
        """
        QWidget::hover {
            background-color: lightgreen;
        }
        """
        self.setStyleSheet(stylesheet)
        self.setLayout(self.layout)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        print("switch chat")
        self.c.switch_chat.emit(self.getPeerID())

    def setText(self, text: str):
        return self.label.setText(text)

    def setPeerID(self, peer_id: int):
        self.peer_id = peer_id

    def getPeerID(self):
        return self.peer_id
