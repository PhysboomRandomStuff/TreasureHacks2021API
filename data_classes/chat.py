import json
from firebase_interactor import pushToDB, noKeyPush, getFromDB
from data_classes.queried_list import QueriedList
from securer import hash
from data_classes.responses import BaseResponse
import time
from datetime import datetime


class Message:
    def __init__(self, message, sender, time=time.mktime(datetime.now().timetuple())):
        self.message = message
        self.sender = sender
        self.time = time

    def to_json(self):
        return json.dumps(self, indent=4, default=lambda o: o.__dict__)


class Chat:
    def __init__(self, users):
        self.users = users

    def push(self):
        pushToDB(self.to_json(), ['Chats', hash("".join(self.users))])

    def to_json(self):
        return json.dumps(self, indent=4, default=lambda o: o.__dict__)

    def add_message(self, message):
        try:
            QueriedList(['Messages', hash("".join(self.users))]).pushData(message.to_json())
            return BaseResponse(True)
        except Exception as e:
            return BaseResponse(False, errors=[str(e)])


    @staticmethod
    def load(chat_id):
        chat_data = json.loads(json.dumps(getFromDB(['Chats', chat_id])))
        return Chat.decode(chat_data)

    @staticmethod
    def decode(obj):
        return Chat(obj['users'])
