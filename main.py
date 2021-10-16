from flask import Flask, request
from flask_cors import CORS, cross_origin
from firebase_interactor import check_token
from data_classes.responses import BaseResponse
from data_classes.user import User
from data_classes.chat import Chat, Message
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "fdsjfuiyujew98tcewu,x9freucterycewyrct8eu"

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def check_uid_equivalence(uid, user):
    return uid == user['user_id']


def check_chat_allowed(request, cur_chat, data):
    return request.user and cur_chat.users and request.user['user_id'] == data['sender'] and request.user[
        'user_id'] in cur_chat.users


'''
-------------------------------------------
USER METHODS
-------------------------------------------
'''

'''
Registration endpoint.
Input: {email: email, password: password}
Actions: Create user
Output: BaseResponse
'''


@app.route("/v1/user/register", methods=['POST'])
@cross_origin()
def register():
    data = request.get_json()
    if not data:
        return BaseResponse(success=False, errors=["No data sent."]).to_json()
    try:
        try:
            user_data_init = data['user_data']
        except:
            user_data_init = None
        return User.register(data['email'], data['password'], user_data_init).to_json()
    except:
        return BaseResponse(False, errors=['Improper data']).to_json()


'''
Login endpoint.
Input: {email: email, password: password}
Actions: Attempt to login with credentials
Output: BaseResponse w/ Firebase id_token & uuid if successful
'''


@app.route('/v1/user/login', methods=['POST'])
@cross_origin()
def login():
    data = request.get_json()
    if not data:
        return BaseResponse(success=False, errors=["No data sent."]).to_json()
    try:
        idtoken, uuid, resp = User.login(data['email'], data['password'])
        if resp.success:
            return BaseResponse(True, json={"id_token": idtoken, "uuid": uuid}).to_json()
        return resp.to_json()
    except:
        return BaseResponse(False, errors=['Improper data']).to_json()


'''
Get public user data.
Input: User
Output: BaseResponse w/ public user data
'''
@app.route('/v1/user/<user>', methods=['POST'])
@cross_origin()
def get_user_data(user):
    try:
        cur_user = User.load(user)
        if cur_user:
            return BaseResponse(success=True, json=json.loads(cur_user.to_json())).to_json()
        return BaseResponse(success=False, errors=['Failed to get user data. Perhaps this user is invalid']).to_json()
    except Exception as e:
        return BaseResponse(success=False, errors=[str(e)]).to_json()

@app.route('/v1/user/<user>', methods=['PATCH'])
@cross_origin()
@check_token(request)
def patch_user_data(user):
    try:
        if not check_uid_equivalence(user, request.user):
            return BaseResponse(False, errors=['Bad Authentication']).to_json()
        data = request.get_json()
        cur_user = User.load(user)
        cur_user.update(data)
        cur_user.push()
        return BaseResponse(True).to_json()
    except Exception as e:
        return BaseResponse(success=False, errors=[str(e)]).to_json()

@app.route('/v1/user/<user>/upload-profile', methods=['POST'])
@cross_origin()
@check_token(request)
def upload_profile_pic(user):
    try:
        if not check_uid_equivalence(user, request.user):
            return BaseResponse(False, errors=['Bad Authentication']).to_json()
        file=request.files['profile-pic']
        cur_user = User.load(user)
        return cur_user.change_profile_pic(file).to_json()
    except Exception as e:
        return BaseResponse(False, errors=[str(e)])




'''
-------------------------------------------
CHAT METHODS
-------------------------------------------
'''

'''
Send chat message endpoint
Inputs: {sender: uuid, message: message}, authorization
Actions: Add message to chat (if it exists) if authorized
Outputs: BaseResponse
'''


@app.route("/v1/chat/<chat>/send", methods=['POST'])
@cross_origin()
@check_token(request)
def sendChatMessage(chat):
    data = request.get_json()
    if not data:
        return BaseResponse(success=False, errors=["No data sent."]).to_json()
    try:
        cur_chat = Chat.load(chat)
        if check_chat_allowed(request, cur_chat, data):
            return cur_chat.add_message(Message(data['message'], data['sender'], int(datetime.now().timestamp()))).to_json()
        return BaseResponse(success=False,
                            errors=["Either you are unauthorized for this action or this chat doesn't exist"]).to_json()
    except Exception as e:
        return BaseResponse(success=False, errors=[str(e)]).to_json()


'''
Get all chat messages, TODO: Filter
Inputs: {sender: uuid}, authorization
Actions: Add message to chat (if it exists) if authorized
Outputs: BaseResponse
'''


@app.route("/v1/chat/<chat>/messages", methods=['POST'])
@cross_origin()
@check_token(request)
def getChatMessages(chat):
    data = request.get_json()
    if not data:
        return BaseResponse(success=False, errors=["No data sent."]).to_json()
    try:
        cur_chat = Chat.load(chat)
        if check_chat_allowed(request, cur_chat, data):
            return cur_chat.get_messages().to_json()
        return BaseResponse(success=False,
                            errors=["Either you are unauthorized for this chat or this chat doesn't exist"]).to_json()
    except Exception as e:
        return BaseResponse(success=False, errors=[str(e)]).to_json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
