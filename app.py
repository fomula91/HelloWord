from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
import certifi
certifi = certifi.where()
client = MongoClient('url입력')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/api/login", methods=["POST"])
def login():
    #로그인
    return jsonify({'msg':''})



@app.route("/api/signup", methods=["POST"])
def signup():
    #회원가입
    return jsonify({'msg': ''})

@app.route("/api/words/:para", methods=["GET"])
def word_list():
    #단어목록
    return jsonify({'msg': ''})

@app.route("/api/words/", methods=["POST"])
def init_word():
    #단어추가
    return
@app.route("/api/words/:para", methods=["POST"])
def edit_word():
    #단어수정
    return

@app.route("/api/words/:para", methods=["POST"])
def delete_word():
    #단어삭제
    return
if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
