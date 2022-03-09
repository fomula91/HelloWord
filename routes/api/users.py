from flask import Blueprint, request, jsonify
from models.auth import Auth
from models.users import Users
from models.words import Words

users_api = Blueprint('users_api', __name__, url_prefix='/api')


@users_api.route('/login', methods=['POST'])
def login():
    user_id = request.form['user_id']
    user_passwd = request.form['user_passwd']

    [signed, token, message] = Auth.sign(user_id, user_passwd)
    return jsonify({"ok": signed, "token": token, "message": message})


@users_api.route('/signup', methods=['POST'])
def sign_up():
    user_id = request.form['user_id']
    user_name = request.form['user_name']
    user_passwd = request.form['user_passwd']

    [success, message] = Users.create(user_id, user_name, user_passwd)

    if not success:
        return jsonify({"ok": False, "message": message})

    [ok, message] = Words.dummy(user_id)
    return jsonify({"ok": ok, "message": message})