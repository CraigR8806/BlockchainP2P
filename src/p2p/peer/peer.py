from p2p.connection import Connection


class Peer:

    """
    Class representing a P2P Peer

    ---
    FIELDS
    ---

    This class has no accessible fields
    """

    def __init__(self, name: str, connection: Connection):
        """
        Constructor for Peer

        Args:
            name (str): The `Peer` name
            connection (Connection): The `Connection` object that describes how to connect with the `Peer`
        """
        self.__name = name
        self.__connection = connection

    def get_connection(self) -> Connection:
        """
        Accessor for the `Connection` object

        Returns:
            Connection: The `Connection` object
        """
        return self.__connection

    def get_name(self) -> str:
        """
        Accessor for the `Peer` name

        Returns:
            str: The `Peer` name
        """
        return self.__name

    def __eq__(self, other: "Peer"):
        return (
            self.__name == other.__name
            and self.__connection.get_host() == other.__connection.get_host()
            and self.__connection.get_port() == other.__connection.get_port()
        )

    def __ne__(self, other: "Peer"):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__name)

    def __str__(self):
        return self.get_name()
