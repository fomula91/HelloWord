# Annotaion(함수나 클래스의 인자값 또는 반환값의 형태를 알려주기 위해 타입을 지정하는 방법)을 위한 클래스

# bool 타입의 ok
class BooleanOk:
    @staticmethod
    def __type__():
        return bool


# dict 타입의 uses
class DictionaryUser:
    @staticmethod
    def __type__():
        fields = {
            "_id": str,
            "user_id": str,
            "user_name": str,
            "user_passwd": str
        }
        return fields


# dict 타입의 payload
class DictionaryPayload:
    @staticmethod
    def __type__():
        fields = {
            "user_id": str,
            "user_name": str,
        }
        return fields


# string 타입의 token
class StringToken:
    @staticmethod
    def __type__():
        return str


# string 타입의 user_id
class StringUserId:
    @staticmethod
    def __type__():
        return str


# string 타입의 message
class StringMessage:
    @staticmethod
    def __type__():
        return str


# string 타입의 objectId
class StringObjectId:
    @staticmethod
    def __type__():
        return str


# list 타입의 words
class ArrayWords:
    @staticmethod
    def __type__():
        return str
