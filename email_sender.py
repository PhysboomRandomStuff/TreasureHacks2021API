import smtplib, ssl
import os
from data_classes.responses import BaseResponse

class EmailSender:
    PORT = 465
    PASSWORD = password = os.environ['EMAIL_PW']
    SENDER_EMAIL = "treasurehacksrf@gmail.com"
    def __init__(self):
        self.context = ssl.create_default_context()

    def send_email(self, receiver, message):
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", EmailSender.PORT, context=self.context) as server:
                server.login(EmailSender.SENDER_EMAIL, EmailSender.PASSWORD)
                server.sendmail(EmailSender.SENDER_EMAIL, receiver, message)
            return BaseResponse(True)
        except Exception as e:
            return BaseResponse(False, errors=[str(e)])





