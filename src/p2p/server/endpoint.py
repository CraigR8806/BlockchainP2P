from p2p.authentication.role import Role

from enum import Enum
import typing as t


class Endpoint:

    class MethodEnum(Enum):
        POST = "POST"
        GET = "GET"
        OPTIONS = "OPTIONS"

    def __init__(
        self,
        uri: str,
        name: str,
        method: MethodEnum,
        response: t.Dict[str, str],
        params: t.Dict[str, str] = None,
        accessible_to: Role = Role.OPEN
    ):
        self.__uri = uri
        self.__name = name
        self.__method = method
        self.__response = response
        self.__params = params
        self.__accessible_to = accessible_to

    def get_uri(self) -> str:
        return self.__uri

    def get_method(self) -> t.Iterable[str]:
        out = [self.__method.value]
        if self.__method == Endpoint.MethodEnum.POST:
            out.append("OPTIONS")
        return out

    def get_response(self) -> t.Dict[str, str]:
        return self.__response

    def get_params(self) -> t.Dict[str, str]:
        return self.__params

    def get_name(self) -> str:
        return self.__name
    
    def accessible_to(self) -> Role:
        return self.__accessible_to
