import os

from flask import Flask, render_template, request, jsonify, session
from pymongo import MongoClient
import certifi
import configparser

config = configparser.ConfigParser()
config.read(os.getcwd() + os.sep + 'config.ini', encoding='utf-8')
# print('db_host : ' + config['DB_CONFIG']['HOST'])

ca = certifi.where()

client = MongoClient(config['DB_CONFIG']['HOST'],
                     tlsCAFile=ca)
db = client.dbsparta

app = Flask(__name__)
app.secret_key = config['FLASK_SECRET_KEY']['KEY']


@app.route('/')
def home():
    if 'id' in session:
        return return_all_words()
    return render_template('index.html')


@app.route("/api/login", methods=["POST"])
def api_login():
    print('login')
    id = request.form['id']
    pw = request.form['pw']

    users = list(db.user.find({'id': id}, {'_id': False}))
    if len(users) == 0:
        return jsonify({'msg': 'ID가 존재하지 않습니다.'})

    if users[0]['pw'] != pw:
        return jsonify({'msg': '비밀번호가 다릅니다.'})

    session['id'] = id
    return return_all_words()


@app.route("/api/signup", methods=["POST"])
def api_signup():
    id = request.form['id']
    pw = request.form['pw']
    pw2 = request.form['confirm']

    if pw != pw2:
        return jsonify({'msg': '입력된 비밀번호가 다릅니다.'})

    users = list(db.user.find({'id': id}, {'_id': False}))
    print(users)
    if len(users) > 0:
        return jsonify({'msg': '이미 사용중인 ID 입니다.'})

    data = {
        'id': id,
        'pw': pw,
    }
    db.user.insert_one(data)
    session['id'] = id
    return return_all_words()


@app.route("/api/logout", methods=["GET"])
def api_logout():
    session.pop('id', None)
    return home()


# 모든 단어 조회
@app.route("/api/words", methods=["GET"])
def return_all_words():
    id = session['id']

    all_words = list(db.words.find({'id': id}, {'_id': False}))
    return render_template('word.html', words=all_words)


# 새 단어 추가
@app.route("/api/words", methods=["POST"])
def add_word():
    id = session['id']
    word = request.form['word']
    mean = request.form['mean']

    data = {
        'word': word,
        'mean': mean,
        'status': '0',
        'id': id
    }
    db.words.insert_one(data)
    return return_all_words()


#
#
# # 단어 수정
# @app.route("/api/words", methods=["PUT"])
# def update_word():
#     return 0


# 단어 지우기
@app.route("/api/words", methods=["DELETE"])
def delete_word():
    return 0


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
