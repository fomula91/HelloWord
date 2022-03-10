from bson import ObjectId
from utils.client import db
from utils.error import Error
from utils import types

collection = db.words


# words 컬렉션 모델
class Words:
    # words 검색
    @staticmethod
    def find(user_id: str, query: dict = None) -> [types.BooleanOk, types.ArrayWords]:

        if query:
            query = dict(query)
            query["user_id"] = user_id
        else:
            query = {"user_id": user_id}

        if "word_done" in query.keys():
            value = query["word_done"]
            query["word_done"] = True if value in ['true'] else False

        if "word_star" in query.keys():
            value = query["word_star"]
            query["word_star"] = True if value in ['true'] else False

        if "public" in query.keys():
            value = query["public"]
            query["public"] = True if value in ['true'] else False
            del query["user_id"]

        try:
            words = list(collection.find(query))
            for (i, word) in enumerate(words):
                words[i]["_id"] = str(word["_id"])
            return [True, words, '']
        except Exception as e:
            print("Words.find :", e)
            return [False, [], Error.UnexpectedError()]

    # word 추가
    @staticmethod
    def add(user_id: str, doc: dict) -> [types.BooleanOk, types.StringMessage]:
        doc = dict(doc)
        doc["user_id"] = user_id
        doc["word_done"] = False
        doc["word_star"] = False

        try:
            collection.insert_one(doc)
            return [True, "등록되었습니다."]
        except Exception as e:
            print("Words.add :", e)
            return [False, Error.UnexpectedError()]

    # word 수정
    @staticmethod
    def update(user_id: str, word_id: types.StringObjectId, doc: dict) -> [types.BooleanOk, types.StringMessage]:
        doc = dict(doc)

        if "word_done" in doc:
            value = doc["word_done"]
            doc["word_done"] = True if value in ["true"] else False

        if "word_star" in doc:
            value = doc["word_star"]
            doc["word_star"] = True if value in ["true"] else False

        try:
            collection.update_one(
                {"user_id": user_id, "_id": ObjectId(word_id)}, {"$set": dict(doc)})
            return [True, '수정되었습니다.']
        except Exception as e:
            print("Words.update :", e)
            return [False, Error.UnexpectedError()]

    # word 삭제
    @staticmethod
    def delete(user_id: str, word_id: types.StringObjectId) -> [types.BooleanOk, types.StringMessage]:
        try:
            collection.delete_one(
                {"user_id": user_id, "_id": ObjectId(word_id)})
            return [True, '수정되었습니다.']
        except Exception as e:
            print("Words.delete :", e)
            return [False, Error.UnexpectedError()]

    # 회원가입 시 임시 데이터 생성
    @staticmethod
    def dummy(user_id: str) -> [types.BooleanOk, types.StringMessage]:
        default_words = [
            {"word_word": "ex) create", "word_mean": "ex) 생성하다, 창조하다",
                "word_star": True, "word_done": True},
        ]

        for (i, _) in enumerate(default_words):
            default_words[i]["user_id"] = user_id
        try:
            collection.insert_many(default_words)
            return [True, '']
        except Exception as e:
            print("Words.dummy :", e)
            return [False, Error.UnexpectedError()]
