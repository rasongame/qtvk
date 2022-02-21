from PyQt6.QtCore import QObject, pyqtSignal
from vk_api.longpoll import VkLongPoll, Event, VkEventType


class LongPollListener(QObject):
    running = False
    newMessage = pyqtSignal(Event)

    def __init__(self, vk):
        super().__init__()
        self.vk = vk
        self.lp = VkLongPoll(self.vk)

    def run(self):
        for event in self.lp.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                self.newMessage.emit(event)
