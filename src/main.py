from blockchain.fullchainpeer import FullChainPeer
from p2p.connection import Connection
import signal
import sys
import time
import shared.util as util
from shared.pki.pki import PKI
from shared.pki.nopki import NoPKI
import random

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
    wait_time=2
    if properties['client']['is_bootstrap_node']:
        bootstrap_connections = []
        wait_time=0

    is_bootstrap_node = properties['client']['is_bootstrap_node']

    me = FullChainPeer(properties['server']['name'],
                        connection, 
                        database_connection,
                        properties['database']['name'], 
                        properties['database']['collection']['name'],
                        diagnostics=True, pki=pki,
                        is_bootstrap_node=is_bootstrap_node)

    print("STARTING SERVER")
    me.start_node()
    print("SERVER START INITTED")
    print("SLEEPING " + str(wait_time) + " SECONDS WAITING FOR SERVER TO START")
    time.sleep(wait_time)
    print("SLEEP DONE ATTEMPTING TO START CLIENT")
    me.bootstrap_to_network(bootstrap_connections)
    print("CLIENT STARTED")


    if not is_bootstrap_node:
        me.synchronize_chain(bootstrap_connections[0])
        chain_length = me.chain.chain_length()
        print("HERES MY CHAIN LENGTH: " + str(chain_length))
        blocks = me.chain.get_blocks(0, chain_length)
        print("HERES MY BLOCKS:")
        [print(b.data) for b in blocks]



    def kill_it(signal, frame):
        me.stop_node()
        sys.exit(0)

    signal.signal(signal.SIGINT, kill_it)


if __name__ == '__main__':
    main()
