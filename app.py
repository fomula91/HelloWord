from flask import Flask
from routes.pages import pages
from routes.api.users import users_api
from routes.api.words import words_api

app = Flask(__name__)

# Blueprint 등록
app.register_blueprint(pages)
app.register_blueprint(users_api)
app.register_blueprint(words_api)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
