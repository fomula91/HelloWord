import jwt
from flask import request
from datetime import datetime, timedelta
from utils.env import SECRET_KEY
from utils.hash import hashing
from models.users import Users
from utils.error import Error


class Auth:

    @staticmethod
    def sign(user_id: str, user_passwd: str) -> [bool, str, str]:
        [success, user, message] = Users.find(user_id)

        if not success:
            return [success, user, message]

        hashed_passwd = hashing(user_passwd)

        if hashed_passwd != user["user_passwd"]:
            return [False, '', Error.PasswdIncorrectError()]

        expired = datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        payload = {"user_id": user_id, "exp": expired}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return [True, token, '']

    @staticmethod
    def check(req: request) -> [bool, str, str]:
        token = req.cookies.get('hello-token')
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            [success, user, message] = Users.find(payload["user_id"])

            if not success:
                return [success, '', message]

            return [True, user["user_id"], '']

        except jwt.ExpiredSignatureError:
            return [False, '', Error.ExpiredTokenError()]

        except jwt.exceptions.DecodeError:
            return [False, '', Error.UndefinedTokenError()]


