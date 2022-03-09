from utils.client import db
from utils.error import Error
from utils.hash import hashing

collection = db.users


class Users:
    @staticmethod
    def find(user_id: str) -> [bool, dict, '']:
        try:
            user = collection.find_one({'user_id': user_id})

            if not user:
                return [False, {}, Error.UserNotFoundError()]

            user = dict(user)
            user["_id"] = str(user["_id"])
            return [True, user, '']
        except Exception as e:
            print("Users.find", e)
            return [False, {}, Error.UnexpectedError()]

    @staticmethod
    def create(user_id, user_name, user_passwd) -> [bool, str]:
        [_, user, _] = Users.find(user_id)

        if user:
            return [False, Error.AlreadyExistUser()]

        doc = {
            "user_id": user_id,
            "user_name": user_name,
            "user_passwd": hashing(user_passwd)
        }

        try:
            collection.insert_one(doc)
            return [True, '']
        except Exception as e:
            print("Users.create", e)
            return [False, Error.UnexpectedError()]
