import json
from firebase_interactor import pushToDB, loginEmail, registerUserEmail, getFromDB, uploadToStorage
from data_classes.responses import BaseResponse
from email_sender import EmailSender

class User:
    def __init__(self, uuid, email, first_name='Anon', last_name='Ymous',
                 profile_pic="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
                 chats=[''], projects_applied=[''], field_of_study='Science', experience='0 yrs'):
        self.uuid = uuid
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.chats = chats
        self.profile_pic = profile_pic
        self.projects_applied = projects_applied
        self.field_of_study = field_of_study
        self.experience = experience

    def update(self, data):
        try:
            self.first_name = data['first_name']
        except KeyError:
            pass
        try:
            self.last_name = data['last_name']
        except KeyError:
            pass
        try:
            self.field_of_study = data['field_of_study']
        except KeyError:
            pass
        try:
            self.experience = data['experience']
        except KeyError:
            pass

    def add_projects_applied(self, proj):
        self.projects_applied.append(proj)
        email = EmailSender()
        email.send_email(self.email, "You have successfully applied for project# " + proj + ". The project leader has been notified")

    def push(self):
        pushToDB(self.to_json(), ['Users', self.uuid])

    def to_json(self):
        return json.dumps(self, indent=4, default=lambda o: o.__dict__)

    def change_profile_pic(self, profile_pic, id_token):
        try:
            filepath, dbpath, resp = uploadToStorage(profile_pic, [self.uuid, 'profile'], id_token)
            if resp.success:
                self.profile_pic = filepath
                self.push()
            return resp
        except Exception as e:
            return BaseResponse(False, errors=[str(e)])

    @staticmethod
    def login(email, pw):
        return loginEmail(email, pw)

    @staticmethod
    def register(email, pw, obj=None):
        uuid, resp = registerUserEmail(email, pw)
        if resp.success:
            user = User(uuid, email)
            if obj:
                user.update(obj)
            user.push()
        return resp

    @staticmethod
    def load(uuid):
        userData = json.loads(json.dumps(getFromDB(['Users', uuid])))
        return User.decode(userData)

    @staticmethod
    def decode(obj):
        try:
            return User(obj['uuid'], obj['email'], obj['first_name'], obj['last_name'], obj['profile_pic'],
                        obj['chats'], obj['projects_applied'], obj['field_of_study'], obj['experience'])
        except:
            return None
