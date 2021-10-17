import json
from firebase_interactor import pushToDB, noKeyPush, getFromDB
import time
from datetime import datetime
import uuid
from data_classes.user import User
from data_classes.responses import BaseResponse
from email_sender import EmailSender

class ResearchProject:
    def __init__(self, user_created, title, description, project_id=None, iat = int(datetime.now().timestamp())):
        self.user_created = user_created
        self.title = title
        self.description = description
        self.project_id = project_id or str(uuid.uuid4())
        self.iat = iat


    def push(self):
        pushToDB(self.to_json(), ['ResearchProjects', self.project_id])

    def to_json(self):
        return json.dumps(self, indent=4, default=lambda o: o.__dict__)

    def apply(self, sender_user, message):
        try:
            receiver_user = User.load(self.user_created)
            email = EmailSender()
            message = sender_user.first_name + " " + sender_user.last_name + " has applied to your \"" + self.title + "\" project!\n\nTheir message:\n" + message + "\n\nReply back to them at " + sender_user.email
            email_resp = email.send_email(receiver_user.email, message)
            return email_resp
        except Exception as e:
            return BaseResponse(False, errors=[str(e)])


    @staticmethod
    def load(project_id):
        chat_data = json.loads(json.dumps(getFromDB(['ResearchProjects', project_id])))
        return ResearchProject.decode(chat_data)

    @staticmethod
    def decode(obj):
        try:
            return ResearchProject(obj['user_created'], obj['title'], obj['description'], obj['project_id'], obj['iat'])
        except:
            return ResearchProject(None, None, None, -1, None)