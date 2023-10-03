from p2p.connection import Connection


class Peer:

    def __init__(self, name:str, connection:Connection, public_key:str=None):
        self.name = name
        self.connection = connection   
        self.public_key = public_key


    def __eq__(self, other):
        return self.name == other.name \
            and self.connection.ip_address == other.connection.ip_address \
            and self.connection.port == other.connection.port \
            and self.public_key == other.public_key
    

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)