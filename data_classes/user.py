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

  @staticmethod
  def register(email, pw):
    uuid, resp = registerUserEmail(email, pw)
    if resp.success:
      user = User(uuid, email, [], [])
      user.push()
    return resp

