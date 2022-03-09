import hashlib


def hashing(any_string: str) -> str:
    return hashlib.sha256(any_string.encode('utf-8')).hexdigest()
