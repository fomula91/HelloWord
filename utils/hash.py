import hashlib


# 문자열 암호화 -> 회원가입 및 로그인 시 비밀번호 암호화
def hashing(any_string: str) -> str:
    return hashlib.sha256(any_string.encode('utf-8')).hexdigest()
