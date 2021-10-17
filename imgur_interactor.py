import os
from imgurpython import ImgurClient
from data_classes.responses import BaseResponse


class ImgurInteractor:
    CLIENT_ID = os.environ['IMGUR_CLIENT_ID']
    CLIENT_SECRET = os.environ['IMGUR_CLIENT_SECRET']
    def __init__(self):
        self.client = ImgurClient(ImgurInteractor.CLIENT_ID, ImgurInteractor.CLIENT_SECRET)
    def upload(self, img):
        try:
            return BaseResponse(True,json=self.client.upload_from_path(img))
        except Exception as e:
            return BaseResponse(False, errors=[str(e)])