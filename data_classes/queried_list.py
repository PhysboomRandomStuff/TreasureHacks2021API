import json
from firebase_interactor import getFromDB, pushToDB, noKeyPush


class QueriedList:
    def __init__(self, key, data=None):
        self.data = data or []
        self.key = key

    def to_json(self):
        return json.dumps(self, indent=4, default=lambda o: o.__dict__)

    def pushData(self, data, key=None):
        if key:
            pushToDB(data, self.key + key)
        else:
            noKeyPush(data, self.key)

    def push(self):
        pushToDB(self.to_json(), self.key)

    @staticmethod
    def fetch(key, query_dict):
        return QueriedList(key, getFromDB(key, query_dict))

    @staticmethod
    def decode(obj):
        try:
            data = obj['data']
        except KeyError:
            data = []
        return QueriedList(obj['key'], data)