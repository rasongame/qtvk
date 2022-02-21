from PyQt6 import uic
from PyQt6.QtCore import QThread, pyqtSlot
from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QLineEdit, QScrollArea
from vk_api import vk_api
from vk_api.longpoll import Event
import utils
from LongPollListener import LongPollListener
from widgets.ChatHistoryItem import ChatHistoryItem
from widgets.ChatListItem import ChatListItem
from widgets.Communicate import Communicate
from widgets.ProfileWindow import ProfileWindow


class MainWindow(QMainWindow):
    def get_user_in_chat(self, user_id: int) -> str:
        if user_id in self.current_chat_users:
            user = self.current_chat_users[user_id]
            name = utils.build_username(user)
            return name
        else:
            users = self.vk.users.get(user_ids=user_id)
            if len(users) != 0:
                user = users[0]
                print("is user called")
                self.current_chat_users[user['id']] = user
                name = utils.build_username(user)
                return name
            else:
                # is a bot aka group
                group = self.vk.groups.getById(group_id=-user_id)[0]
                print("is group called " + group['name'])
                self.current_chat_users[group['id']] = group
                name = group['name']
                return name

    @pyqtSlot(int)
    def chat_list_on_clicked(self, peer_id: int):
        print("mainwindow switch_chat")
        self.current_chat_id = peer_id
        self.load_chat_history(peer_id)
        if peer_id in self.loaded_chat_titles:
            for_title = self.loaded_chat_titles[peer_id]
            self.setWindowTitle(utils.build_window_title("QtVK", for_title))

    @pyqtSlot(Event)
    def render_new_message(self, event: Event):
        name = "DELETED"
        if event.from_user:
            user_id = event.peer_id
        elif event.from_chat:
            user_id = event.user_id

        else:
            return

        name = self.get_user_in_chat(user_id)

        print("new message")

        item = ChatHistoryItem(name, event.message)
        self.chat_history.addWidget(item)

    def send_button_on_clicked(self):
        if self.current_chat_id == 0: return  # Chat unselected
        if len(self.textEdit.text()) <= 0: return  # textEdit is unfilled
        self.vk.messages.send(peer_id=self.current_chat_id, random_id=0, message=self.textEdit.text())
        self.textEdit.clear()

    def load_chat_history(self, peer_id: int):
        for i in reversed(range(self.chat_history.count())):
            self.chat_history.itemAt(i).widget().setParent(None)

        history = self.vk.messages.getHistory(peer_id=peer_id, count=200, fields=["photo"])
        users_ids = [message["from_id"] for message in history["items"][::-1]]
        if not set(users_ids).issubset(self.current_chat_users):
            print("good")
            users = self.vk.users.get(user_ids=users_ids)
            for user in users:
                user_id = user['id']
                self.current_chat_users[user_id] = user
        else:
            print("fuck")
        # self.chat_history.
        print(peer_id)
        for message in history['items'][::-1]:
            text = message['text']
            for attachment in message["attachments"]:
                if attachment['type'] == "audio_message":
                    if attachment["audio_message"]['transcript_state'] == "done":
                        transcript = attachment["audio_message"].get("transcript", "WTF?")
                        text += f'\n ТРАНСКРИПТ: {transcript}'

            from_user = self.get_user_in_chat(message['from_id'])
            item = ChatHistoryItem(from_user, text)
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
                self.loaded_chat_titles[peer['id']] = title
                conversation_message_id = conversation['last_conversation_message_id']
                last_message = self.vk.messages.getByConversationMessageId(peer_id=peer['id'], conversation_message_ids=conversation_message_id)['items'][0]
                item = ChatListItem(title, last_message['text'], communicate=self.c)
                item.setPeerID(peer['id'])
                self.chat_list.addWidget(item)

        users = self.vk.users.get(user_ids=user_ids)
        for user in users:
            name = utils.build_username(user)
            item = ChatListItem(name, "", self.c)
            item.setPeerID(user['id'])
            self.loaded_chat_titles[user['id']] = name
            self.chat_list.addWidget(item)

    def init_vk(self):
        user_info = self.vk.account.getProfileInfo()
        self.load_chat_list()
        self.username_label.setText(f"{user_info['first_name']} {user_info['last_name']}")

    def open_profile_window(self):
        myself = self.vk.users.get(fields=["photo_200_orig", "nickname", "status", "screen_name"])
        ProfileWindow(myself[0])

    @pyqtSlot(str)
    def init_logic(self, token):

        self.token = token
        self.vk_session = vk_api.VkApi(token=self.token)
        self.vk = self.vk_session.get_api()
        self.init_vk()
        self.long_poll_listener_thread = QThread()
        self.long_poll_listener = LongPollListener(self.vk_session)
        self.long_poll_listener.moveToThread(self.long_poll_listener_thread)
        self.long_poll_listener.newMessage.connect(self.render_new_message)
        self.long_poll_listener_thread.started.connect(self.long_poll_listener.run)
        self.long_poll_listener_thread.start()
        self.show()

    def __init__(self, communicate=Communicate()):
        super(MainWindow, self).__init__()
        self.c = communicate
        self.current_chat_id = 0
        self.current_chat_users = {}
        self.loaded_chat_titles: dict = {}
        uic.loadUi("kicker.ui", self)
        self.username_label: QLabel = self.findChild(QLabel, "label")
        self.send_button: QPushButton = self.findChild(QPushButton, "sendButton")
        self.chat_list: QVBoxLayout = self.findChild(QVBoxLayout, "chatList")
        self.chat_history: QVBoxLayout = self.findChild(QVBoxLayout, "chatHistory")
        self.textEdit: QLineEdit = self.findChild(QLineEdit, "textEdit")
        self.profileButton: QPushButton = self.findChild(QPushButton, "profileButton")
        self.c.switch_chat.connect(self.chat_list_on_clicked)
        self.send_button.clicked.connect(self.send_button_on_clicked)
        self.profileButton.clicked.connect(self.open_profile_window)
        self.c.login_vk.connect(self.init_logic)
        # self.show()
