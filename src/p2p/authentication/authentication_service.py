from p2p.authentication.user import User
from p2p.authentication.role import Role
from p2p.authentication.api_key import ApiKey
from abc import ABC, abstractmethod

import typing as t
from typing import Generic, TypeVar
from uuid import UUID

T = TypeVar("T")


class AuthenticationService(ABC):
    class Response(Generic[T]):
        def __init__(self, status: int, message: str, returnedObj: T = None):
            self.status = status
            self.message = message

    def __init__(self):
        pass

    @abstractmethod
    def load_user(self, api_key: ApiKey) -> "AuthenticationService.Response[User]":
        pass

    @abstractmethod
    def new_user(self, user: User) -> "AuthenticationService.Response[ApiKey]":
        pass

    @abstractmethod
    def modify_user(
        self, uuid: UUID, user: User
    ) -> "AuthenticationService.Response[None]":
        pass

    @abstractmethod
    def delete_user(self, uuid: UUID) -> "AuthenticationService.Response[None]":
        pass
