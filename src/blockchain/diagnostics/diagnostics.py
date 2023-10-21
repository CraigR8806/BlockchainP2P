from p2p.server.server import Server

class Diagnostics:

    def __init__(self, server:Server):
        self.server = server
        self.server.add_get_endpoint("/diag/node/list", "nodeList", self.__list_nodes)
        self.server.add_get_endpoint("/diag/node/name", "nodeName", self.__get_name)
        self.server.add_get_endpoint("/diag/node/connection", "nodeConnection", self.__get_connection)
        self.server.add_get_endpoint("/diag/node/uptime", "nodeUptime", self.__uptime)



    def __list_nodes(self):
        return self.server.build_response(200, self.server.data_service.deep_copy("active_peers"))

    def __get_name(self):
        return self.server.build_response(200, {"name": self.server.parent_peer.name})
    
    def __get_connection(self):
        return self.server.build_response(200, self.server.parent_peer.connection)
    
    def __uptime(self):
        return self.server.build_response(200, {"uptime":self.server.uptime()})
    


