from p2p.authentication.role import Role
from p2p.authentication.api_key import ApiKey
import typing as t
from uuid import uuid4, UUID


class User:
    def __init__(self, username: str, roles: t.Set[Role]):
        self.__username = username
        self.__roles = roles
        self.__roles.add(Role.OPEN)
        self.__apikey = ApiKey()
        self.__uuid = uuid4()

    def get_username(self) -> str:
        return self.__username

    def has_role(self, role: Role) -> bool:
        return role in self.__roles

    def get_apikey(self) -> ApiKey:
        return self.__apikey

    def get_uuid(self) -> UUID:
        return self.__uuid
