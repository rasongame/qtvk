from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QLineEdit
from vk_api import vk_api

from widgets.ChatHistoryItem import ChatHistoryItem
from widgets.ChatListItem import ChatListItem
from widgets.Communicate import Communicate
from widgets.ProfileWindow import ProfileWindow


class MainWindow(QMainWindow):

    def chat_list_on_clicked(self, peer_id: int):
        print("mainwindow switch_chat")
        self.current_chat_id = peer_id
        self.load_chat_history(peer_id)

    def send_button_on_clicked(self):
        if self.current_chat_id == 0: return  # Chat unselected
        if len(self.textEdit.text()) <= 0: return  # textEdit is unfilled
        self.vk.messages.send(peer_id=self.current_chat_id, random_id=0, message=self.textEdit.text())
        item = ChatHistoryItem(-9999, "Я: " + self.textEdit.text())
        self.chat_history.addItem(item)
        self.textEdit.clear()

    def load_chat_history(self, peer_id: int):
        for i in reversed(range(self.chat_history.count())):
            self.chat_history.itemAt(i).widget().setParent(None)

        history = self.vk.messages.getHistory(peer_id=peer_id, count=200, fields=["photo"])
        users_ids = [message["from_id"] for message in history["items"][::-1]]
        users = self.vk.users.get(user_ids=users_ids)
        for user in users:
            user_id = user['id']
            self.current_chat_users[user_id] = user

        # self.chat_history.
        print(peer_id)
        for message in history['items'][::-1]:
            text = message['text']
            for attachment in message["attachments"]:
                if attachment['type'] == "audio_message":
                    if attachment["audio_message"]['transcript_state'] == "done":
                        transcript = attachment["audio_message"].get("transcript", "WTF?")
                        text += f'\n ТРАНСКРИПТ: {transcript}'
            from_user = self.current_chat_users.get(message['from_id'], {"first_name": "DELETED", "last_name": ""})
            item = ChatHistoryItem(f'{from_user["first_name"]} {from_user["last_name"]}', text)
            self.chat_history.addWidget(item)

    def load_chat_list(self):
        chat_list = self.vk.messages.getConversations()
        user_ids = [item['conversation']['peer']['id'] for item in chat_list['items'] if
                    item['conversation']['peer']["type"] == "user"]
        print(user_ids)
        for item in chat_list["items"]:
            conversation = item["conversation"]
            peer = conversation["peer"]
            if peer["type"] == "chat":
                chat_settings = conversation["chat_settings"]
                title = chat_settings['title']

                item = ChatListItem(title, communicate=self.c)
                item.setPeerID(peer['id'])
                self.chat_list.addWidget(item)

        users = self.vk.users.get(user_ids=user_ids)
        for user in users:
            item = ChatListItem(f"{user['first_name']} {user['last_name']}", self.c)
            item.setPeerID(user['id'])
            self.chat_list.addWidget(item)

    def init_vk(self):
        user_info = self.vk.account.getProfileInfo()
        self.load_chat_list()
        self.username_label.setText(f"{user_info['first_name']} {user_info['last_name']}")

    def open_profile_window(self):
        myself = self.vk.users.get(fields=["photo", "nickname", "status", "screen_name"])
        ProfileWindow(myself[0])

    def __init__(self, token: str):
        super(MainWindow, self).__init__()
        self.current_chat_id = 0
        self.current_chat_users = {}
        self.token = token
        uic.loadUi("kicker.ui", self)

        self.vk_session = vk_api.VkApi(token=self.token)
        self.vk = self.vk_session.get_api()
        self.username_label: QLabel = self.findChild(QLabel, "label")
        self.send_button: QPushButton = self.findChild(QPushButton, "sendButton")
        self.chat_list: QVBoxLayout = self.findChild(QVBoxLayout, "chatList")
        self.chat_history: QVBoxLayout = self.findChild(QVBoxLayout, "chatHistory")
        self.textEdit: QLineEdit = self.findChild(QLineEdit, "textEdit")
        self.profileButton: QPushButton = self.findChild(QPushButton, "profileButton")
        self.c = Communicate()
        self.c.switch_chat.connect(self.chat_list_on_clicked)
        self.send_button.clicked.connect(self.send_button_on_clicked)
        self.profileButton.clicked.connect(self.open_profile_window)

        # self.chat_list.

        self.init_vk()
        self.show()
