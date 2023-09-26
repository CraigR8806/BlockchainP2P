const express = require('express');
const { Peer } = require('../node/peer');
const Blockchain = require('../../shared/data/blockchain');
const app = express ();
app.use(express.json());


class Server {

    constructor(parentNode) {
        this.parentNode = parentNode;
    }

    updateChain(chain) {
        
    }


    startServer(bootstrapIPs) {

        if (bootstrapIPs.length == 0) {
            this.chain = new Blockchain();
            bootstrapIPs = [this.parentNode.connection];
        }

        app.listen(this.parentNode.connection.port, ()=>{

            app.post('/node/join', (request, response) => {

                console.log(request.body.js_code.peer);

                this.parentNode.addPeer(request.body.js_code.peer);

                response.json({"peers":this.parentNode.getActivePeers()});
            });
            app.post('/node/leave', (request, response) => {
                response.send();
            });

            console.log("listening on port " + this.parentNode.connection.port);
        });

        this.parentNode.joinNetwork(bootstrapIPs);
    }
}

module.exports.Server = Server;