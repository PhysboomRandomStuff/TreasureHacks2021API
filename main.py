from flask import Flask, request
from flask_cors import CORS, cross_origin

from data_classes.responses import BaseResponse
from data_classes.user import User

app = Flask(__name__)
app.secret_key = "fdsjfuiyujew98tcewu,x9freucterycewyrct8eu"

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def check_uid_equivalence(uid, user, request):
    if uid == user['user_id']:
        return True
    return False


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
