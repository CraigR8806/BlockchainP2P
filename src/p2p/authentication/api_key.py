import secrets
from time import time


class ApiKey:
    def __init__(self, expiration_length=15778476):
        self.__key = secrets.token_urlsafe(16)
        self.__issued = time()
        self.__expiration = self.__issued + expiration_length

    def get_key(self) -> str:
        return self.__key

    def is_expired(self) -> bool:
        return time() >= self.__expiration

    def was_issued_at(self) -> float:
        return self.__issued
