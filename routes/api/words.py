from flask import Blueprint, request, redirect, url_for, jsonify
from models.auth import Auth
from models.words import Words

# 단어 API 요청 블루프린트 객체 등록
words_api = Blueprint('words_api', __name__, url_prefix="/api/words")


# 단어 조회 요청
@words_api.route('/', methods=["GET"])
def word_find():
    [ok, payload, _] = Auth.check(request)

    if not ok:
        return redirect(url_for("pages.home"))

    user_id = payload["user_id"]

    query = request.args.to_dict()
    [ok, words, message] = Words.find(user_id, query)

    return jsonify({"ok": ok, "words": words, "message": message})


# 단어 등록 요청
@words_api.route('/new', methods=["POST"])
def word_insert():
    [ok, payload, _] = Auth.check(request)

    if not ok:
        return redirect(url_for("pages.home"))

    user_id = payload["user_id"]

    doc = request.form
    [ok, message] = Words.add(user_id, doc)

    return jsonify({"ok": ok, message: message})


# 단어 수정 요청
@words_api.route('/<string:word_id>', methods=["PUT"])
def word_modify(word_id):
    [ok, payload, _] = Auth.check(request)

    if not ok:
        return redirect(url_for("pages.home"))

    user_id = payload["user_id"]

    doc = request.form
    [ok, message] = Words.update(user_id, word_id, doc)

    return jsonify({"ok": ok, message: message})


# 단어 삭제 요청
@words_api.route('/<string:word_id>', methods=["DELETE"])
def word_delete(word_id):
    [ok, payload, _] = Auth.check(request)

    if not ok:
        return redirect(url_for("pages.home"))

    user_id = payload["user_id"]

    [ok, message] = Words.delete(user_id, word_id)
    return jsonify({"ok": ok, message: message})
