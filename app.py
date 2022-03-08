import pymongo
from flask import Flask, render_template
JWT_SECRET_KEY = "Hanghae99Chater1MiniTeamProjectHelloWord"

app = Flask(__name__)

# MongoDB 연결
db = pymongo.MongoClient()


@app.route('/')
def home():
    return render_template("index.j2")


@app.route('/my_words')
def my_words():
    return render_template("my_words.j2")


@app.route('/quiz')
def quiz():
    return render_template("quiz.j2")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

