const express = require('express');
const Client = require('../client/client');
const Blockchain = require('../shared/data/blockchain');
const app = express ();
app.use(express.json());


module.exports = class Server {

    constructor(ip, port, name) {
        this.client = new Client(this, ip, port, name);
    }

    updateChain(chain) {
        
    }

    startServer(bootstrapIPs) {

        if (bootstrapIPs.length > 0) 
            this.client.joinNetwork(bootstrapIPs);
        else 
            this.chain = new Blockchain();
        

        app.listen(this.client.connection.port, ()=>{

            app.post('/node/join', (request, response) => {
                console.log(request.body.js_code);
                response.json({"blockchain":this.chain});
            });
            app.post('/node/leave', (request, response) => {
                response.send();
            });

            console.log("listening on port " + this.client.connection.port);
        });
    }



}