from blockchain.fullchainpeer import FullChainPeer
from p2p.connection import Connection
import signal
import sys
import time
import shared.util as util
from shared.pki.pki import PKI
from shared.pki.nopki import NoPKI

def main():

    properties = util.read_properties_file(sys.argv[1])

    print("------------------------------------------------------------------")
    print("-  Starting Blockchain Node " + properties['server']['name']+"")
    print("------------------------------------------------------------------")

    

    connection = None
    bootstrap_connections = None
    pki = None
    if properties['pki']['enabled']:
        pki = PKI(properties['pki']['certificate_path'], properties['pki']['private_key_path'], properties['pki']['certificate_authority_path'])
        connection = Connection(properties['server']['host'], properties['server']['https_port'])
        bootstrap_connections=[Connection(c['host'], c['https_port']) for c in properties['client']['bootstrap_connections']]
    else:
        pki = NoPKI()
        connection = Connection(properties['server']['host'], properties['server']['http_port'])
        bootstrap_connections=[Connection(c['host'], c['http_port']) for c in properties['client']['bootstrap_connections']]

    database_connection = Connection(properties['database']['host'], properties['database']['port'])

    me = FullChainPeer(properties['server']['name'],
                        connection, 
                        database_connection,
                        properties['database']['name'], 
                        properties['database']['collection']['name'],
                        diagnostics=True, pki=pki)

    me.start_node()
    time.sleep(3)
    me.join_network(bootstrap_connections)


    def kill_it(signal, frame):
        me.stop_node()
        sys.exit(0)

    signal.signal(signal.SIGINT, kill_it)


if __name__ == '__main__':
    main()


