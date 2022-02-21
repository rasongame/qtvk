from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QListWidgetItem, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGridLayout


class ChatHistoryItem(QWidget):
    def __init__(self, user_id: int, message_text: str, user: dict = {}):
        super(ChatHistoryItem, self).__init__()
        self.user_id = user_id
        self.message_text = message_text
        self.layout = QGridLayout()
        self.avatar_image = QImage()
        self.author_label = QLabel()
        self.message_label = QLabel()

        self.author_label.setText(str(self.getFromID()))
        self.message_label.setText(message_text)

        #self.layout.addWidget(self.avatar_image)
        self.layout.addWidget(self.author_label)

        self.layout.addWidget(self.message_label)
        self.layout.setSpacing(1)
        self.setLayout(self.layout)

    def setText(self, text: str):
        return self.message_label.setText(text)
    def setFromID(self, user_id):
        self.user_id = user_id

    def getFromID(self):
        return self.user_id
