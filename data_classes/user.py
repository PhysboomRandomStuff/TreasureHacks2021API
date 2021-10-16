import json
from firebase_interactor import pushToDB, loginEmail, registerUserEmail, getFromDB

class User:
  def __init__(self, uuid, email, chats=[], projects_applied=[]):
    self.uuid = uuid
    self.email = email
    self.chats = chats
    self.projects_applied = projects_applied

  def push(self):
    pushToDB(self.to_json(), ['Users', self.uuid])

  def to_json(self):
    return json.dumps(self, indent=4, default=lambda o: o.__dict__)

  @staticmethod
  def login(email, pw):
      return loginEmail(email, pw)


  @staticmethod
  def register(email, pw):
    uuid, resp = registerUserEmail(email, pw)
    if resp.success:
      user = User(uuid, email, [], [])
      user.push()
    return resp

