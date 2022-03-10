import jwt
from flask import request
from datetime import datetime, timedelta
from utils.env import SECRET_KEY
from utils.hash import hashing
from models.users import Users
from utils.error import Error
from utils import types


# 유저 인증 모델
class Auth:
    # 유저 인증 확인(로그인 정보 일치하는 경우 토큰 발급)
    @staticmethod
    def sign(user_id: str, user_passwd: str) -> [types.BooleanOk, types.StringToken, types.StringMessage]:
        [ok, user, message] = Users.find(user_id)

        if not ok:
            return [ok, '', message]

        hashed_passwd = hashing(user_passwd)

        if hashed_passwd != user["user_passwd"]:
            return [False, '', Error.PasswdIncorrectError()]
        user_name = user["user_name"]
        expired = datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        payload = {"user_id": user_id, "user_name": user_name, "exp": expired}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return [True, token, '']

    # 유저 인가 확인(모든 API 요청 시 토큰 검증)
    @staticmethod
    def check(req: request) -> [types.BooleanOk, types.DictionaryPayload, types.StringMessage]:
        token = req.cookies.get('hello-token')
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            [ok, user, message] = Users.find(payload["user_id"])

            if not ok:
                return [ok, {}, message]

            user_id = user["user_id"]
            user_name = user["user_name"]
            return [ok, {"user_id": user_id, "user_name": user_name}, ''] if ok else [ok, '', message]

        except jwt.ExpiredSignatureError:
            return [False, {}, Error.ExpiredTokenError()]

        except jwt.exceptions.DecodeError:
            return [False, {}, Error.UndefinedTokenError()]
