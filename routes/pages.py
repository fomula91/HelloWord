from flask import Blueprint, request, redirect, url_for, render_template
from models.auth import Auth

# 템플릿 페이지 라우터 객체 등록
pages = Blueprint('pages', __name__, url_prefix='/', template_folder="templates" )


# 홈 화면
@pages.route('/')
def home():
    [ok, _, _] = Auth.check(request)
    return redirect(url_for("pages.my_words")) if ok else render_template("index.html")


# 나만의 단어장 화면
@pages.route('/mywords')
def my_words():
    [ok, _, _] = Auth.check(request)
    return render_template("mywords.html") if ok else redirect(url_for("pages.home"))


# 퀴즈 화면
@pages.route('/quiz')
def quiz():
    [ok, _, _] = Auth.check(request)
    return render_template("quiz.html") if ok else redirect(url_for("pages.home"))
