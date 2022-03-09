from flask import Blueprint, request, redirect, url_for, render_template
from models.auth import Auth

pages = Blueprint('pages', __name__, url_prefix='/', template_folder="templates" )


@pages.route('/')
def home():
    [signed, _, _] = Auth.check(request)

    if signed:
        return redirect(url_for("pages.my_words"))

    return render_template("index.html")


@pages.route('/mywords')
def my_words():
    [signed, _, _] = Auth.check(request)

    if not signed:
        return redirect(url_for("pages.home"))

    return render_template("mywords.html")


@pages.route('/quiz')
def quiz():
    [signed, _, _] = Auth.check(request)

    if not signed:
        return redirect(url_for("pages.home"))

    return render_template("quiz.html")
