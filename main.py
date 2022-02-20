import math

import vk_api
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QListWidget, QMessageBox, QListWidgetItem, \
    QTextEdit
import sys

from widgets.ChatHistoryItem import ChatHistoryItem
from widgets.ChatListItem import ChatListItem

TOKEN = ""


class MainWindow(QMainWindow):
    def chat_list_on_clicked(self, item: ChatListItem):
        self.current_chat_id = item.getPeerID()
        self.load_chat_history(item.getPeerID())

    def send_button_on_clicked(self, item: QPushButton):
        if len(self.textEdit.toPlainText()) <= 0: return
        self.vk.messages.send(peer_id=self.current_chat_id, random_id=0, message=self.textEdit.toPlainText())
        item = ChatHistoryItem()
        item.setFromID(-9999)
        item.setText("Я: "+ self.textEdit.toPlainText())
        self.chat_history.addItem(item)
        self.textEdit.clear()

    def load_chat_history(self, peer_id: int):
        history = self.vk.messages.getHistory(peer_id=peer_id, count=200)
        print(history)
        self.chat_history.clear()
        for message in history['items'][::-1]:
            item = ChatHistoryItem()
            item.setFromID(message['from_id'])
            text = message['text']
            for attachment in message["attachments"]:
                if attachment['type'] == "audio_message":
                    if attachment["audio_message"]['transcript_state'] == "done":
                        transcript = attachment["audio_message"].get("transcript", "WTF?")
                        text += f'\n ТРАНСКРИПТ: {transcript}'
            text = message['text']
            item.setText(f'{message["from_id"]}: {text}')

            self.chat_history.addItem(item)

    def load_chat_list(self):
        chat_list = self.vk.messages.getConversations()
        user_ids = [item['conversation']['peer']['id'] for item in chat_list['items'] if
                    item['conversation']['peer']["type"] == "user"]

        for item in chat_list["items"]:
            conversation = item["conversation"]
            peer = conversation["peer"]
            if peer["type"] == "chat":
                chat_settings = conversation["chat_settings"]
                title = chat_settings['title']

                item = ChatListItem()
                item.setPeerID(peer['id'])
                item.setText(title)

                self.chat_list.addItem(item)

        users = self.vk.users.get(user_ids=user_ids)
        for user in users:
            item = ChatListItem()
            item.setPeerID(user['id'])
            item.setText(f"{user['first_name']} {user['last_name']}")

            self.chat_list.addItem(item)

    def init_vk(self):
        user_info = self.vk.account.getProfileInfo()
        self.load_chat_list()
        self.username_label.setText(f"{user_info['first_name']} {user_info['last_name']}")

    def __init__(self):
        super(MainWindow, self).__init__()
        self.current_chat_id = 0
        self.current_chat_users = []
        uic.loadUi("mainwindow.ui", self)
        self.vk_session = vk_api.VkApi(token=TOKEN)
        self.vk = self.vk_session.get_api()
        self.username_label: QLabel = self.findChild(QLabel, "username")
        self.send_button: QPushButton = self.findChild(QPushButton, "sendButton")
        self.chat_list: QListWidget = self.findChild(QListWidget, "chatList")
        self.chat_history: QListWidget = self.findChild(QListWidget, "chatHistory")
        self.textEdit: QTextEdit = self.findChild(QTextEdit, "textEdit")

        self.send_button.clicked.connect(self.send_button_on_clicked)
        self.chat_list.itemDoubleClicked.connect(self.chat_list_on_clicked)

        self.init_vk()
        self.show()


app = QApplication(sys.argv)
window = MainWindow()
app.exec()
