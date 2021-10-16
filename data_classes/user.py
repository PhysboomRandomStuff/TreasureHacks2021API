import json
from firebase_interactor import pushToDB, loginEmail, registerUserEmail, getFromDB, uploadToStorage
from data_classes.responses import BaseResponse


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

    def push(self):
        pushToDB(self.to_json(), ['Users', self.uuid])

    def to_json(self):
        return json.dumps(self, indent=4, default=lambda o: o.__dict__)

    def change_profile_pic(self, profile_pic):
        try:
            filepath, dbpath, resp = uploadToStorage(profile_pic, [self.uuid, 'profile'])
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
    def register(email, pw):
        uuid, resp = registerUserEmail(email, pw)
        if resp.success:
            user = User(uuid, email)
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
