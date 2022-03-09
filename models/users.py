from utils.client import db
from utils.error import Error
from utils.hash import hashing
from utils import types

collection = db.users


# users 컬렉션 모델
class Users:
    # 유저 검색 -> 유저 인가 확인 및 회원가입 시(아이디 중복 방지)
    @staticmethod
    def find(user_id: str) -> [types.BooleanOk, types.DictionaryUser, types.StringMessage]:
        try:
            user = collection.find_one({'user_id': user_id})

            # 아이디가 없는 경우
            if not user:
                return [False, {}, Error.UserNotFoundError()]

            user = dict(user)
            user["_id"] = str(user["_id"])
            return [True, user, '']
        except Exception as e:
            print("Users.find", e)
            return [False, {}, Error.UnexpectedError()]

    # 유저 생성 -> 회원가입 시
    @staticmethod
    def create(user_id: str, user_name: str, user_passwd: str) -> [types.BooleanOk, types.StringMessage]:

        [_, user, _] = Users.find(user_id)

        # 아이디 중복 여부 확인
        if user:
            return [False, Error.AlreadyExistUser()]
        # -----------------

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
