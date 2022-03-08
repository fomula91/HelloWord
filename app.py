from flask import Flask, render_template, request, jsonify, redirect, url_for
from utils.mongo import MongoDB
from datetime import datetime, timedelta
from distutils.util import strtobool
import jwt

JWT_SECRET = "HangHae99Chapter1MiniProject"

app = Flask(__name__)
mongo = MongoDB()


@app.route('/')
def home():
    token = request.cookies.get("hello-token")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        result = mongo.auth_user(payload)
        if not result["ok"]:
            return render_template("index.j2")
        return redirect(url_for("my_words"))
    except jwt.ExpiredSignatureError:
        return render_template("index.j2", message="로그인 시간이 만료되었습니다.")
    except jwt.exceptions.DecodeError:
        return render_template("index.j2")


@app.route('/mywords')
def my_words():
    token = request.cookies.get("hello-token")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        result = mongo.auth_user(payload)
        if not result["ok"]:
            return redirect(url_for("home"))
        return render_template("my_words.j2")
    except jwt.ExpiredSignatureError:
        return redirect(url_for("home", message="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("home", message="로그인 시간이 만료되었습니다."))


def check_auth(req) -> jsonify:
    token = req.cookies.get('hello-token')
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = mongo.auth_user(payload)

        if not user:
            return {
                "ok": False,
                "message": "사용자 정보를 찾을 수 없습니다."
            }
        return {
            "ok": True
        }
    except jwt.ExpiredSignatureError:
        return {
            "ok": False,
            "message": "로그인 기간이 만료되었습니다."
        }
    except jwt.exceptions.DecodeError:
        return {
            "ok": False,
            "message": "로그인 정보가 존재하지 않습니다."
        }


@app.route('/api/signup', methods=["POST"])
def signup() -> jsonify:
    data = request.form
    result = mongo.insert_user(data)

    if not result["ok"]:
        return jsonify({
            "ok": False,
            "message": result["message"]
        })

    return jsonify({
        "ok": True
    })


@app.route('/api/login', methods=["POST"])
def login() -> jsonify:
    data = request.form
    result = mongo.sign_user(data)

    if not result["ok"]:
        return jsonify({
            "ok": False,
            "message": result["message"]
        })

    user = result["user"]
    payload = {
        "id": user["id"],
        "exp": datetime.utcnow() + timedelta(days=1)
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    return jsonify({
        "ok": True,
        "token": token
    })


# query-string으로 필터
# ex) /api/words                            모든 단어 조회
# ex) /api/words?done=True                  암기 완료한 단어만 조회
# ex) /api/words?star=True                  즐겨찾기 추가된 단어만 조회
# ex) /api/words?done=True&start=True       암기 완료 및 즐찾 추가된 단어만 조회
@app.route('/api/words', methods=["GET"])
def get_words() -> jsonify:
    auth = check_auth(request)

    if not auth['ok']:
        return jsonify(auth)

    query = request.args.to_dict()
    query["id"] = auth["id"]

    # 'done'이 query에 있는 경우 Boolean으로 형변환
    if 'done' in query.keys():
        query["done"] = bool(strtobool(query["done"]))

    # 'star'가 query에 있는 경우 Boolean으로 형변환
    if 'star' in query.keys():
        query['star'] = bool(strtobool(query["star"]))

    result = mongo.find_words(query)

    return jsonify({
        "ok": True,
        "words": result
    })


@app.route('/api/words/new', method=["POST"])
def insert_words() -> jsonify:

    # 토큰 유효성 체크
    auth = check_auth(request)

    if not auth['ok']:
        return jsonify(auth)

    # ajax로 받는 데이터 : { word: String, mean: String }
    data = request.form
    result = mongo.insert_word(data)

    if not result["ok"]:
        return {"ok": False, "message": result["message"]}

    return jsonify({"ok": True})


# 단어의 _id를 params로 받음
@app.route('/api/words/<str:_id>', methods=["PUT"])
def update_word(_id) -> jsonify:

    # 토큰 유효성 체크
    auth = check_auth(request)

    if not auth['ok']:
        return jsonify(auth)

    # ajax로 받는 데이터 : { word?: String, mean?: String, done?: Boolean, star?: Boolean }
    # 물음표는 있어도 되고, 없어도 된다는 뜻
    data = request.form
    result = mongo.update_word(_id, data)

    if not result["ok"]:
        return {"ok": False, "message": result["message"]}

    return {"ok": True}


# 단어의 _id를 params로 받음 ex)/api/words/Xkaeo31axAsleklsj35Gsz
@app.route('/api/words/<str:_id>', method=["DELETE"])
def delete_words(_id) -> jsonify:

    # 토큰 유효성 체크
    auth = check_auth(request)

    if not auth['ok']:
        return jsonify(auth)

    result = mongo.delete_word(_id)

    if not result["ok"]:
        return {"ok": False, "message": result["message"]}

    return jsonify({"ok": True})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
