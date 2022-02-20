from PyQt6.QtWidgets import QListWidgetItem


class ChatHistoryItem(QListWidgetItem):
    def __init__(self):
        super(ChatHistoryItem, self).__init__()
        self.user_id = None

    def setFromID(self, user_id):
        self.user_id = user_id

    def getFromID(self):
        return self.user_id
