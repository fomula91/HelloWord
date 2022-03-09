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
            return [ok, user, message]

        hashed_passwd = hashing(user_passwd)

        if hashed_passwd != user["user_passwd"]:
            return [False, '', Error.PasswdIncorrectError()]

        expired = datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        payload = {"user_id": user_id, "exp": expired}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return [True, token, '']

    # 유저 인가 확인(모든 API 요청 시 토큰 검증)
    @staticmethod
    def check(req: request) -> [types.BooleanOk, types.StringUserId, types.StringMessage]:
        token = req.cookies.get('hello-token')
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            [ok, user, message] = Users.find(payload["user_id"])

            if not ok:
                return [ok, '', message]

            return [True, user["user_id"], '']

        except jwt.ExpiredSignatureError:
            return [False, '', Error.ExpiredTokenError()]

        except jwt.exceptions.DecodeError:
            return [False, '', Error.UndefinedTokenError()]
