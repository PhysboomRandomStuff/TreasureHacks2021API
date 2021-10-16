import json
from firebase_interactor import pushToDB
from securer import hash
import time
from datetime import datetime

class Message:
    def __init__(self, message, sender, time=time.mktime(datetime.now().timetuple())):
        self.message=message
        self.sender=sender
        self.time=time

    def to_json(self):
        return json.dumps(self, indent=4, default=lambda o: o.__dict__)

class Chat:
    def __init__(self, users, messages=[]):
        self.users = users
        self.messages = messages

    def push(self):
        pushToDB(self.to_json(), ['Chats', hash("".join(self.users))])

    def to_json(self):
        return json.dumps(self, indent=4, default=lambda o: o.__dict__)

    def add_message(self, message):
        self.messages.append(message)