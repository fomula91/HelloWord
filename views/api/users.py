from flask import Blueprint, request, jsonify
from models.auth import Auth
from models.users import Users
from models.words import Words

# 유저 API 요청 블루프린트 객체 등록
users_api = Blueprint('users_api', __name__, url_prefix='/api')


# 로그인 요청
@users_api.route('/login', methods=['POST'])
def login():
    user_id = request.form['user_id']
    user_passwd = request.form['user_passwd']

    # 인증 확인 및 토큰 발급
    [ok, token, message] = Auth.sign(user_id, user_passwd)
    return jsonify({"ok": ok, "token": token, "message": message})


# 회원가입 요청
@users_api.route('/signup', methods=['POST'])
def sign_up():
    user_id = request.form['user_id']
    user_name = request.form['user_name']
    user_passwd = request.form['user_passwd']

    # 유저 등록
    [ok, message] = Users.create(user_id, user_name, user_passwd)

    if not ok:
        return jsonify({"ok": False, "message": message})

    # 임시 데이터 추가
    [ok, message] = Words.dummy(user_id)
    return jsonify({"ok": ok, "message": message})
