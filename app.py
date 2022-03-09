import os
from bson import ObjectId
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import certifi
import configparser
import jwt
import hashlib
from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta

config = configparser.ConfigParser()
config.read(os.getcwd() + os.sep + 'config.ini', encoding='utf-8')
secret_key = config['FLASK_SECRET_KEY']['KEY']
ca = certifi.where()

app = Flask(__name__)
app.secret_key = secret_key
client = MongoClient(config['DB_CONFIG']['HOST'], tlsCAFile=ca)
db = client.dbsparta


# (추가) 최원영
# 토근 유효성 체크를 위해 따로 함수로 분할
def check_token(req) -> dict:
    token = req.cookies.get('hello-token')

    try:
        payload = jwt.decode(token, secret_key, algorithms='HS256')
        user = db.users.find_one({'user_id': payload["user_id"]})

        if not user:
            message = "사용자 정보를 찾을 수 없습니다."
            return {"ok": False, "message": message}

        user_id = user["user_id"]
        return {"ok": True, "user_id": user_id}
    except jwt.ExpiredSignatureError:
        return {"ok": False, "message": "토큰이 만료되었습니다."}
    except jwt.exceptions.DecodeError:
        return {"ok": False, "message": "로그인 정보가 존재하지 않습니다."}


@app.route('/')
def home():

    # (추가) 최원영
    # ------------
    check = check_token(request)

    if check["ok"]:
        return redirect(url_for("my_words"))
    # ------------

    return render_template("index.html")


@app.route('/mywords')
def my_words():

    # (추가) 최원영
    # ------------
    check = check_token(request)

    if not check["ok"]:
        return redirect(url_for("home"))
    # ------------

    return render_template("mywords.html")


@app.route('/quiz')
def quiz():

    # (추가) 최원영
    # ------------
    check = check_token(request)

    if not check["ok"]:
        return redirect(url_for("home"))
    # ------------

    return render_template("quiz.html")


# 하상우
@app.route('/api/login', methods=['POST'])
def login():
    user_id = request.form['user_id']
    user_passwd = request.form['user_passwd']

    user = db.users.find_one({'user_id': user_id})

    # (추가) 최원영
    # ------------
    if not user:
        return jsonify({"ok": False, "message": "존재하지 않는 아이디입니다."})
    # ------------

    hashed = hashlib.sha256(user_passwd.encode('utf-8')).hexdigest()

    # (추가) 최원영
    # ------------
    if hashed != user["user_passwd"]:
        return jsonify({"ok": False, "message": "비밀번호가 일치하지 않습니다."})
    # ------------

    payload = {'user_id': user_id,
               'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)}
    token = jwt.encode(payload, secret_key, algorithm='HS256')

    return jsonify({"ok": True, "token": token})


# 하상우
@app.route('/api/signup', methods=['POST'])
def sign_up():
    user_id = request.form['user_id']
    user_name = request.form['user_name']
    user_passwd = request.form['user_passwd']

    # (추가) 최원영
    # ------------
    exist = db.users.find_one({'user_id': user_id})

    if exist:
        return {"ok": False, "message": "이미 존재하는 아이디입니다."}
    # ------------

    hashed = hashlib.sha256(user_passwd.encode('utf-8')).hexdigest()
    doc = {
        "user_id": user_id,
        "user_name": user_name,
        "user_passwd": hashed
    }
    db.users.insert_one(doc)
    return jsonify({"ok": True})


# 김형중
@app.route('/api/words', methods=["GET"])
def word_find():

    # (수정) 최원영
    # ------------
    check = check_token(request)

    if not check["ok"]:
        # 기존 : response -> { ok, message }
        # 변경 : redirect -> /
        return redirect(url_for("home", message=check["message"]))
    # ------------

    query = dict(request.args.to_dict())
    query["user_id"] = check["user_id"]

    # (추가) 최원영
    # ------------
    if "word_done" in query.keys():
        current = query["word_done"]
        query["word_done"] = True if current in ['true'] else False

    if "word_star" in query.keys():
        current = query["word_star"]
        query["word_star"] = True if current in ['true'] else False
    # ------------

    words = list(db.words.find(query))

    # (추가) 최원영
    # ------------
    for (i, word) in enumerate(words):
        words[i]["_id"] = str(word["_id"])
    # ------------

    return jsonify({"ok": True, "words": words})


# 김형중
@app.route('/api/words/new', methods=["POST"])
def word_insert():
    # (수정) 최원영
    # ------------
    check = check_token(request)

    if not check["ok"]:
        # 기존 : response -> { ok, message }
        # 변경 : redirect -> /
        return redirect(url_for("home", message=check["message"]))
    # ------------

    doc = dict(request.form)
    doc["user_id"] = check["user_id"]
    doc["word_done"] = False
    doc["word_star"] = False

    try:
        db.words.insert_one(doc)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, message: "작업에 실패하였습니다."})


# 홍승민
@app.route('/api/words/<string:word_id>', methods=["PUT"])
def word_modify(word_id):

    # (수정) 최원영
    # ------------
    check = check_token(request)

    if not check["ok"]:
        # 기존 : response -> { ok, message }
        # 변경 : redirect -> /
        return redirect(url_for("home", message=check["message"]))

    user_id = check["user_id"]
    # ------------

    doc = dict(request.form)

    if "word_done" in doc:
        current = doc["word_done"]
        doc["word_done"] = True if current in ["true"] else False

    if "word_star" in doc:
        current = doc["word_star"]
        doc["word_star"] = True if current in ["true"] else False

    result = db.words.update_one({'_id': ObjectId(word_id), 'user_id': user_id}, {'$set': doc}).matched_count

    response = {
        "ok": True if result == 1 else False,
        "message": "수정되었습니다." if result == 1 else "작업에 실패하였습니다."
    }
    return jsonify(response)


# 홍승민
@app.route('/api/words/<string:word_id>', methods=["DELETE"])
def word_delete(word_id):

    # (수정) 최원영
    # ------------
    check = check_token(request)

    if not check["ok"]:
        # 기존 : response -> { ok, message }
        # 변경 : redirect -> /
        return redirect(url_for("home", message=check["message"]))

    user_id = check["user_id"]
    # ------------

    result = db.words.delete_one({'_id': ObjectId(word_id), 'user_id': user_id}).deleted_count

    response = {
        "ok": True if result == 1 else False,
        "messasge": "삭제하였습니다." if result == 1 else "작업에 실패하였습니다."
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
