class Role:
    def __init__(self, role_name: str):
        self.__role_name = role_name

    def get_name(self) -> str:
        return self.__role_name
