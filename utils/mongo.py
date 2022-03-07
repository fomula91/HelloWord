from bson import ObjectId
from pymongo import MongoClient
import hashlib


class MongoDB:
    def __init__(self) -> None:
        self.client = MongoClient('mongodb://root:password@146.56.187.171:27010')
        self.db = self.client["hello-word"]
        self.users_collection = self.db["users"]
        self.words_collection = self.db["words"]

    def auth_user(self, data: dict) -> dict:
        # dict = { id : String }
        try:
            user = self.users_collection.find_one({"id": data["id"]})

            if not user:
                return { "ok": False, "message": "존재하지 않는 아이디입니다."}

            return {"ok": True,  "user": user}
        except Exception as e:
            return {"ok": False, "message": str(e)}

    def sign_user(self, data: dict) -> dict:
        # dict = { id: String, passwd: String }
        try:
            user = self.users_collection.find_one({"id": data["id"]})

            if not user:
                return {"ok": False,"message": "존재하지 않는 아이디입니다."}

            passwd = data["passwd"]
            hashed = hashlib.sha256(passwd.encode('utf-8')).hexdigest()

            if user["passwd"] != hashed:
                return {"ok": False, "message": "비밀번호가 일치하지 않습니다."}

            return {"ok": True, "user": user}
        except Exception as e:
            return {"ok": False, "message": str(e)}

    def insert_user(self, data: dict) -> dict:
        # dict = { id: String, name: String, passwd: String }
        try:
            exist = self.users_collection.find_one({"id": data["id"]})

            if exist:
                return {"ok": False,"message": "이미 존재하는 아이디입니다."}

            passwd = data["passwd"]
            hashed = hashlib.sha256(passwd.encode('utf-8')).hexdigest()

            doc = {
                "id": data["id"],
                "name": data["name"],
                "passwd": hashed
            }
            self.users_collection.insert_one(doc)
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "message": str(e)}

    def insert_word(self, data: dict) -> dict:
        # data = { "user_id": String, "word": String, "mean": String, "done": False, "star": False }
        try :
            self.words_collection.insert_one(data)
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "message": str(e)}

    def find_words(self, query: dict) -> dict:
        # query = { key: value }
        try:
            words = list(self.words_collection.find(query))
            for (i, word) in words:
                word["_id"] = str(word["_id"])
            return {"ok": True, "words": words}
        except Exception as e:
            return {"ok": False, "message": e}

    def update_word(self, _id: str, data: dict) -> dict:
        # data = { "word": String, "mean": String, "done": False, "star": False }
        try:
            _id = ObjectId(_id)
            self.words_collection.update_one({"_id": _id}, data)
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "message": str(e)}

    def delete_word(self, _id: str) -> dict:
        try:
            _id = ObjectId(_id)
            self.words_collection.delete_one({"_id": _id})
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "message": str(e)}
