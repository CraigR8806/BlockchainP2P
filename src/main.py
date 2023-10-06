from peers.blockchain.fullchainpeer import FullChainPeer
from p2p.peer.peer import Peer
from p2p.connection import Connection
import signal
import sys
import time
import shared.util as util
import jsonpickle



def main():

    properties = util.read_properties_file(sys.argv[1])

    connection = Connection(properties['server.ip'], properties['server.port'])

    me = FullChainPeer(properties['server.name'], connection, True)

    me.start_node()
    time.sleep(3)
    me.join_network([Connection(c['ip_address'], c['port']) for c in jsonpickle.decode(properties['client.bootstrap_connections'])])


    def kill_it(signal, frame):
        me.stop_node()
        sys.exit(0)

    signal.signal(signal.SIGINT, kill_it)


if __name__ == '__main__':
    main()


