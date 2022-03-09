from flask import Blueprint, request, redirect, url_for, jsonify
from models.auth import Auth
from models.words import Words

words_api = Blueprint('words_api', __name__, url_prefix="/api/words")


@words_api.route('/', methods=["GET"])
def word_find():
    [signed, user_id, _] = Auth.check(request)

    if not signed:
        return redirect(url_for("pages.home"))

    query = request.args.to_dict()
    [ok, words, message] = Words.find(user_id, query)

    return jsonify({"ok": ok, "words": words, "message": message})


@words_api.route('/new', methods=["POST"])
def word_insert():
    [signed, user_id, _] = Auth.check(request)

    if not signed:
        return redirect(url_for("pages.home"))

    doc = request.form
    [ok, message] = Words.add(user_id, doc)

    return jsonify({"ok": ok, message: message})


@words_api.route('/<string:word_id>', methods=["PUT"])
def word_modify(word_id):
    [signed, user_id, _] = Auth.check(request)

    if not signed:
        return redirect(url_for("pages.home"))

    doc = request.form
    [ok, message] = Words.update(user_id, word_id, doc)

    return jsonify({"ok": ok, message: message})


@words_api.route('/<string:word_id>', methods=["DELETE"])
def word_delete(word_id):
    [signed, user_id, _] = Auth.check(request)

    if not signed:
        return redirect(url_for("pages.home"))

    [ok, message] = Words.delete(user_id, word_id)
    return jsonify({"ok": ok, message: message})
