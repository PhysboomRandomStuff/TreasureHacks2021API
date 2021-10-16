import pyrebase
import json
from functools import wraps
from data_classes.responses import BaseResponse
import firebase_admin
from firebase_admin import credentials, auth
from werkzeug.utils import secure_filename
from securer import hash

SERVICE_ACCOUNT={
  "type": "service_account",
  "project_id": "research-finder-9f54c",
  "private_key_id": "584fbe1623dff429fd016506950d3713ed1ebf71",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDhPSHt2PZ95Q26\nzUIU0X/3YHg/CoP/rI3qFqv1p7RbrWmHIkOyQRlW/LKKnQ8lx/tbpoSwFpeQvJlq\nBqT05fx7gWuR2E9LlYK44+yMwK5PzgQHz8plUH4Nx+8aqI0JFvtzG1cVT5qi+QQ7\nPSMoI1BgysYx7xJDsgVhizqvvwwYzVsuL6VHr+GveSukqTbyEBW0b8sli/5CwIk7\n+hWxhq0x89Rhp7d41xI7nYXB/L5s9D7lhNfyOimkk8Qz2KHzwbunDY6DYxtTI1MY\ncnormkRU2bf0c3FzmRb1LO7/w/Hs2N7jntvN2sNVW2hwmHrKlXNlcP5iljs/hP65\nzoQi01I5AgMBAAECggEACjjubidpiX1wrfSUnhIDiShGUNMi+kK8Np50i7vCpGIG\njvDjymZotmFV35Ng/X2Z53cTYNQHqTScEFswl6JL/xV4urfq4mLs2cQTZ3BzwNC4\nb1vTg11fuTOkowy5COtzek4IeeHA4opjciZUTwUqR9hQHjJL3Ylp89tALLuCmqn6\ngEuMkWw17oFLvdFDviIpqGLGV4z+400oulskluhfrMW68g4FygoWGR8Gc9qBPoVH\nZcaFq4BuJOETeW7Hjm5QI66ZVZRnmpiKL4lS/18LrDI2sPVJcZ9CjH+NRriaZXZV\nw7uxAusQacy6rU2BChKQ8rX41O1o2Xze7YBRWOcAEQKBgQDxcPMGXbgx4tY+s6CG\nNgiSqyC9TIB1SOOYMIDo5ydvLJ9np31/fOGnVVE/MnIV5IXpg+D3PXxAD4080JS2\n3aTYeR5YuGxzQoJ/9+AsB9ftaaKDLqNQH7soGUy80aRcxzbfOZ8p+CNXZXQqa8ys\nZiNF2/Xmrp2fQfnJB9f66bMBsQKBgQDu0hJiN2/9oTeAaQCNPXEEfW6JGii6c1r/\nRC6cr5ufexcljmmfHwgSZH78MnvV20fbcG3oIJv9KFhWvJ1l8RqW/NrXv2NjZJui\n6VuS0PfhkKutYgd7DRReDwYpLxzfQdJkh80WPCyu1bcnSz0FevnidiIP012IePJy\nB4l6j9IzCQKBgQDaG0G/F3ykvBj0jYpOk5NNA4BQ4UIOMWlAe1iIjQCHotTha2Go\ngGTMp/r8TxLWihkaqQLZ9lY+/I2HSZl+VF1tHIT4eqmluYhwF7kPrYo3Mz0WqlPn\ntrJ4d9plnDCRi3kbUE9jN4Cdm83D4JwFhUMKAblyyX0keBIws4A9b05BEQKBgC6q\ncdkrSADhbbzzx53RsbHU6LJ1oBu+yrsykYEgd2JUZRN7nnvvTl55sK6LFtOVA5eH\ngpJnPNPc/FYGiSMQV8fFJOYficY0NI1C2Bf6KVW0NTet/hQ3XBF9EhEeGaAudnQa\nbSK5I2oObLmK5COcAhQUTVeWT6KJL6bEfkKqs8IxAoGAB6+t7Ei+tkFXvBwXYMT2\nulEfbzuvA1fJ8uTB+8l2a+5dNnBh8alpVui8R2i+Dw3dPt9SBwQHVFU6YfVrbJa4\na20+bLSC1Ke7X9sSYgH5Q5cZJXvnkaGr+/KdFHCWb8u/Y3TALhwXvbJXkyjfTCqF\nO+0u331JF6Pc0z1hHgQ7M6k=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-hkwsq@research-finder-9f54c.iam.gserviceaccount.com",
  "client_id": "116967976584661284970",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-hkwsq%40research-finder-9f54c.iam.gserviceaccount.com"
}

firebaseconfig = {  # The config for FB, this is not private info
    "apiKey": "AIzaSyDuqjzjQ4IoN5RHq2ltBEHNnMLkhPbzjcw",
    "authDomain": "research-finder-9f54c.firebaseapp.com",
    "databaseURL": "https://research-finder-9f54c-default-rtdb.firebaseio.com/",
    "storageBucket": "research-finder-9f54c.appspot.com",
    "serviceAccount": SERVICE_ACCOUNT
}


def noquote(s, safe=None):
    return s

pyrebase.pyrebase.quote = noquote

ALLOWED_EXTENSIONS = ['png', 'jpg', 'pdf']  # For legal document upload

cred = credentials.Certificate(SERVICE_ACCOUNT)
firebase = firebase_admin.initialize_app(cred)

pb = pyrebase.initialize_app(firebaseconfig)
pbauth = pb.auth()
database = pb.database()
storage = pb.storage()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def verify_token(token):
    try:
        return True, auth.verify_id_token(token)
    except:
        return False, None  # ID token invalid


def check_token(request):
    def check_token_decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if not request.headers.get('authorization'):
                return BaseResponse(False, errors=['No token provided']).to_json()
            try:
                user = auth.verify_id_token(request.headers['authorization'])
                request.user = user

            except:
                return BaseResponse(False, errors=['Invalid token provided']).to_json()
            return f(*args, **kwargs)

        return wrap

    return check_token_decorator


def loginEmail(email, password):
    try:
        # Tries to sign in, will fail if email/password combo is wrong
        user = pbauth.sign_in_with_email_and_password(email, password)
        # Checks email verification
        if isEmailVerified(user).success == True:
            return user['idToken'], user['localId'], BaseResponse(success=True)
        try:
            # If not verified, try to send email
            pbauth.send_email_verification(user['idToken'])
            return None, user['localId'], BaseResponse(
                success=False,
                warnings=[
                    "Verify your email! Another email verification message has been sent."
                ])

        except:
            return None, user['localId'], BaseResponse(success=False, warnings=["Verify your email!"])
    except:
        return None, None, BaseResponse(
            success=False,
            errors=["Login failed! Check your email and password."])


def getUUID(email, password):
    user = pbauth.sign_in_with_email_and_password(email, password)
    try:
        return user['localId']
    except:
        return None


def isEmailVerified(user):
    if user is None:
        return BaseResponse(success=False)
    else:
        try:
            # auth.get_account_info is a dictionary, just indexing to find emailVerified
            if pbauth.get_account_info(
                    user['idToken'])['users'][0]['emailVerified'] == True:
                return BaseResponse(success=True)
            return BaseResponse(success=False)
        except Exception as e:
            print(e)
            return BaseResponse(success=False)


def registerUserEmail(email, password):
    try:
        # Create user first
        pbauth.create_user_with_email_and_password(email, password)
        # Login in this case actually only serves to send the verification email. You create account, --> attempt to login but verification is not sent, it then gets sent through the login method logic.
        _, uuid, _ = loginEmail(email, password)
        return uuid, BaseResponse(
            success=True,
            info=['Registration succeeded! Please verify your email'])
    except:
        return None, BaseResponse(success=False, errors=["User already exists"])


def sendResetEmail(email):
    try:
        pbauth.send_password_reset_email(email)
        return BaseResponse(success=True)
    except:
        return BaseResponse(success=False)


def noKeyPush(data, children, load_json=True):
    try:
        top = database
        for child in children:
            top = top.child(child)
        if load_json:
            top.push(json.loads(data))
        else:
            top.push(data)
        return BaseResponse(success=True)
    except Exception as e:
        print(e)
        return BaseResponse(success=False)


def pushToDB(data, children, load_json=True):
    try:
        top = database
        for child in children:
            top = top.child(child)
        if load_json:
            top.set(json.loads(data))
        else:
            top.set(data)
        return BaseResponse(success=True)
    except Exception as e:
        print(e)
        return BaseResponse(success=False)


def getFromDB(children, query_dict={}):
    try:
        top = database
        for child in children:
            top = top.child(child)
        methdict = {"order_by_child": top.order_by_child, "limit_to_first": top.limit_to_first,
                    "limit_to_last": top.limit_to_last, "start_at": top.start_at, "end_at": top.end_at}
        typedict = {"order_by_child": str, "limit_to_first": int, "limit_to_last": int, "start_at": noquote,
                    "end_at": noquote}
        for key in query_dict.keys():
            try:
                top = methdict[key](typedict[key](query_dict[key]))
            except Exception as e:
                print(e)
        return top.get().val()
    except Exception as e:
        print("FirebaseException: " + str(e))
        return None


def uploadToStorage(file, children):
    # Returns Firebase storage path, BaseResponse
    try:
        if file.filename == "":
            return None, None, BaseResponse(success=False, errors=['No file selected']).to_json()
        elif file and allowed_file(file.filename):
            if children:
                path = "/".join(children) + "/" + secure_filename(file.filename)
            else:
                path = secure_filename(file.filename)
            cur_file = storage.child(path).put(file)
            return storage.child(path).get_url(cur_file['downloadTokens']), path, BaseResponse(success=True)
    except:
        return None, None, BaseResponse(success=False)


def sendPasswordReset(email):
    try:
        pbauth.send_password_reset_email(email)
        return BaseResponse(True, info=["A password reset email has been sent if the email exists"])
    except:
        return BaseResponse(False, errors=["A password reset email could not be sent."])
