const { Settable } = require("../../shared/data/set");
const sha256Hash = require("../../shared/util");

class Peer extends Settable {

    constructor(name, connection) {
        super();
        this.name = name;
        this.connection = connection;
        this.publicKey;
    }


    toIdString(){
        return sha256Hash(this.name, this.connection, this.publicKey);
    }
}

module.exports.Peer = Peer;