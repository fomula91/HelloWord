import pymongo
from flask import Flask, render_template, jsonify

# 기존 코드는 아래 링크를 참고하세요.
# https://github.com/fomula91/HelloWord/tree/v1.0.0-test

JWT_SECRET_KEY = "Hanghae99Chater1MiniTeamProjectHelloWord"

app = Flask(__name__)

# MongoDB 연결
# db = pymongo.MongoClient()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/mywords')
def my_words():
    result = {
        "ok": True,
        "message": ""
    }
    if not result["ok"]:
        return render_template("mywords.html", message={result["message"]})
    return render_template("mywords.html")


@app.route('/quiz')
def quiz():
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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

