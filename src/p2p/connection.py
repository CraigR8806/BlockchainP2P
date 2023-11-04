


class Connection:

    def __init__(self, host:str, port:str):
        self.__host = host
        self.__port = str(port)

    def get_host(self) -> str:
        return self.__host
    
    def get_port(self) -> str:
        return self.__port

