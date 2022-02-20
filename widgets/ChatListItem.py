from PyQt6.QtWidgets import QListWidgetItem


class ChatListItem(QListWidgetItem):
    def __init__(self):
        super(ChatListItem, self).__init__()
        self.peer_id = None

    def setPeerID(self, peer_id: int):
        self.peer_id = peer_id

    def getPeerID(self):
        return self.peer_id

