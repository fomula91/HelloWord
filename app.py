import os

from bson import ObjectId
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi
import configparser
import jwt
import hashlib
import datetime

config = configparser.ConfigParser()
config.read(os.getcwd() + os.sep + 'config.ini', encoding='utf-8')
secret_key = config['FLASK_SECRET_KEY']['KEY']
# print('db_host : ' + config['DB_CONFIG']['HOST'])

ca = certifi.where()

client = MongoClient(config['DB_CONFIG']['HOST'],
                     tlsCAFile=ca)
db = client.dbsparta

app = Flask(__name__)
app.secret_key = secret_key


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/my_words')
def my_words():
    return render_template("my_words.html")


@app.route('/quiz')
def quiz():
    return render_template("quiz.html")


######################################################
######################################################


# 사용자 로그아웃
@app.route('/api/logout', methods=['POST'])
def user_logout():
    return render_template('index.html')


# 단어 수정하기
@app.route('/api/words/<string:word_id>', methods=["PUT"])
def word_modify(word_id):
    token = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token, secret_key, algorithms='HS256')
        user_id = payload['id'] # user_id
    except Exception as e:
        # 비회원일 경우 처리
        print(e)

    new_word = {
        "word_word": request.form['word_word'],
        "word_mean": request.form['word_mean'],
        "word_done": request.form['word_done'],
        "word_star": request.form['word_star']
    }

    result = db.words.update_one({'_id': ObjectId(word_id), 'user_id': user_id}, {'$set': new_word}).matched_count

    data = {
        "ok": True if result == 1 else False,
        "message": "수정되었습니다." if result == 1 else "적업에 실패하였습니다."
    }
    return jsonify(data)


# 단어 삭제하기
@app.route('/api/words/<string:word_id>', methods=["DELETE"])
def word_delete(word_id):
    token = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token, secret_key, algorithms='HS256')
        user_id = payload['id']
    except Exception as e:
        print(e)

    result = db.words.delete_one({'_id': ObjectId(word_id), 'user_id': user_id}).deleted_count

    data = {
        "ok": True if result == 1 else False,
        "messasge": "삭제하였습니다." if result == 1 else "작업에 실패하였습니다."
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
