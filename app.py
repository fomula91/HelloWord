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

# (주석) 최원영 - config 파일 없음
# ------------
secret_key = config['FLASK_SECRET_KEY']['KEY']
# ------------

ca = certifi.where()

# (주석) 최원영 - config 파일 없음
# ------------
client = MongoClient(config['DB_CONFIG']['HOST'], tlsCAFile=ca)
# ------------

# (임시) 추가
# ------------
# client = MongoClient("mongodb://root:password@146.56.187.171:27010")
db = client.dbsparta
# ------------


# (임시) 추가
# ------------
# secret_key = "SpartaCodingClubHanghae99"
# ------------

app = Flask(__name__)
app.secret_key = secret_key


# (추가) 최원영
# 토근 유효성 체크를 위해 따로 함수로 분할
def check_token(req) -> dict:
    token = req.cookies.get('hello-token')
    res = {}
    try:
        payload = jwt.decode(token, secret_key, algorithms='HS256')
        user = db.users.find_one({'user_id': payload["user_id"]})

        if not user:
            res["ok"] = False
            res["message"] = "사용자 정보를 찾을 수 없습니다."

        res["ok"] = True
        res["user_id"] = user["user_id"]

        return res
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


@app.route('/api/words')
def get_words():
    words = [{
        "word_id": "1",
        "word_word": "apple",
        "word_mean": "사과",
        "word_done": True,
        "word_star": False
    }, {
        "word_id": "2",
        "word_word": "banana",
        "word_mean": "바나나",
        "word_done": True,
        "word_star": False
    }, {
        "word_id": "3",
        "word_word": "pear",
        "word_mean": "배",
        "word_done": False,
        "word_star": False
    }, {
        "word_id": "4",
        "word_word": "Oriental Melon",
        "word_mean": "참외",
        "word_done": True,
        "word_star": True
    }, {
        "word_id": "5",
        "word_word": "Grapes",
        "word_mean": "포도",
        "word_done": False,
        "word_star": False
    }, {
        "word_id": "6",
        "word_word": "Fig",
        "word_mean": "무화과",
        "word_done": False,
        "word_star": True
    }, {
        "word_id": "7",
        "word_word": "pomegranate",
        "word_mean": "석류",
        "word_done": False,
        "word_star": False
    }, {
        "word_id": "8",
        "word_word": "jujube",
        "word_mean": "대추",
        "word_done": False,
        "word_star": True
    }]
    return jsonify({
        "ok": True,
        "words": words
    })


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


# 홍승민
@app.route('/api/words/<string:word_id>', methods=["PUT"])
def word_modify(word_id):
    check = check_token(request)

    if not check["ok"]:
        return redirect(url_for("home", message=check["message"]))

    user_id = check["user_id"]

    update_word = request.form
    result = db.words.update_one({'_id': ObjectId(word_id), 'user_id': user_id}, {'$set': update_word}).matched_count

    response = {
        "ok": True if result == 1 else False,
        "message": "수정되었습니다." if result == 1 else "작업에 실패하였습니다."
    }
    return jsonify(response)


# 홍승민
@app.route('/api/words/<string:word_id>', methods=["DELETE"])
def word_delete(word_id):
    check = check_token(request)

    if not check["ok"]:
        return redirect(url_for("home", message=check["message"]))

    user_id = check["user_id"]

    result = db.words.delete_one({'_id': ObjectId(word_id), 'user_id': user_id}).deleted_count

    data = {
        "ok": True if result == 1 else False,
        "messasge": "삭제하였습니다." if result == 1 else "작업에 실패하였습니다."
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
