const { Peer } = require('./peer');
const { Client } = require('../client/client');
const { Server } = require('../server/server');
const { GeneralSet } = require("../../shared/data/set");
const crypto = require('crypto');


class SelfNode extends Peer {

    constructor(name, connection) {
        super(name, connection);
        this.generateKeyset();
        this.client = new Client(this);
        this.server = new Server(this);

        this.activePeers = new GeneralSet();
        this.activePeers.add(this.asPeer());
    }

    startNode(bootstrapIPs) {
        this.server.startServer(bootstrapIPs);
    }

    joinNetwork(bootstrapIPs) {
        this.client.joinNetwork(bootstrapIPs);
    }

    addPeer(peer) {
        this.activePeers.add(peer);
    }
    addPeers(peers) {
        peers.forEach(peer=>{
            this.activePeers.add(peer);
        })
    }
    getActivePeers() {
        return this.activePeers.values();
    }

    generateKeyset() {
        var { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', {
            modulusLength: 2048,
            publicKeyEncoding: {
              type: 'spki',
              format: 'pem'
            },
            privateKeyEncoding: {
              type: 'pkcs8',
              format: 'pem'
            }
          }); 
        this.privateKey = privateKey;
        this.publicKey = publicKey;
    }

    asPeer(){
        let out = new Peer(this.name, this.connection);
        out.publicKey = this.publicKey;
        return out;
    }

}



module.exports.SelfNode = SelfNode;