import json
from data_classes.timed_data import TimedData
from firebase_interactor import pushToDB
from securer import hash

class Chat:
  def __init__(self, users, messages=[]):
    self.users = users
    self.messages = messages

  def push(self):
    pushToDB(self.to_json(), ['Chats', hash("".join(self.users))])

  def to_json(self):
    return json.dumps(self, indent=4, default=lambda o: o.__dict__)