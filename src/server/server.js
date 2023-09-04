const express = require('express');
const Client = require('../client/client');
const app = express ();
app.use(express.json());


module.exports = class Server {

    constructor(ip, port, name) {
        this.client = new Client(this, ip, port, name);
    }


    startServer(...bootstapIPs) {
        this.client.joinNetwork(bootstapIPs);

        
    }



}