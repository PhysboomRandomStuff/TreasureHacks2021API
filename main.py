from flask import Flask, request
from flask_cors import CORS, cross_origin
from firebase_interactor import check_token
from data_classes.responses import BaseResponse
from data_classes.user import User
from data_classes.chat import Chat, Message

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
        return User.register(data['email'], data['password']).to_json()
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
            return cur_chat.add_message(Message(data['message'], data['sender'])).to_json()
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
