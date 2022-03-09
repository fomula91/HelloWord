class Error:
    @staticmethod
    def UserNotFoundError():
        return "존재하지 않는 아이디입니다."

    @staticmethod
    def AlreadyExistUser():
        return "이미 존재하는 아이디입니다."

    @staticmethod
    def PasswdIncorrectError():
        return "비밀번호가 일치하지 않습니다."

    @staticmethod
    def ExpiredTokenError():
        return "토큰이 만료되었습니다."

    @staticmethod
    def UndefinedTokenError():
        return "유효하지 않은 토큰입니다."

    @staticmethod
    def UnexpectedError():
        return "예기치 못한 오류가 발생하였습니다."
