import pyrebase
import json
from functools import wraps
from data_classes.responses import BaseResponse
import firebase_admin
from firebase_admin import credentials, auth
from werkzeug.utils import secure_filename
from securer import hash

firebaseconfig = {  # The config for FB, this is not private info
    "apiKey": "AIzaSyDuqjzjQ4IoN5RHq2ltBEHNnMLkhPbzjcw",
    "authDomain": "research-finder-9f54c.firebaseapp.com",
    "databaseURL": "https://research-finder-9f54c-default-rtdb.firebaseio.com/",
    "storageBucket": "research-finder-9f54c.appspot.com",
    "serviceAccount": "firebase-admin-conf.json"
}


def noquote(s, safe=None):
    return s

pyrebase.pyrebase.quote = noquote

ALLOWED_EXTENSIONS = ['png', 'jpg', 'pdf']  # For legal document upload

cred = credentials.Certificate('firebase-admin-conf.json')
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


def check_token(request, admin_overwrite=True):
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
            return None, BaseResponse(success=False, errors=['No file selected']).to_json()
        elif file and allowed_file(file.filename):
            if children:
                path = "/".join(children) + "/" + secure_filename(file.filename)
            else:
                path = secure_filename(file.filename)
            storage.child(path).put(file)
            return path, BaseResponse(success=True)
    except:
        return None, BaseResponse(success=False)


def sendPasswordReset(email):
    try:
        pbauth.send_password_reset_email(email)
        return BaseResponse(True, info=["A password reset email has been sent if the email exists"])
    except:
        return BaseResponse(False, errors=["A password reset email could not be sent."])
