const sha256Hash = require("../util");

module.exports = class Block {
    constructor(timestamp, data, previousHash = '') {
        this.previousHash = previousHash;
        this.timestamp = timestamp;
        this.data = data;

        this.hash = this.calculateHash();
    }

    calculateHash() {
        return sha256Hash(this.previousHash,this.timestamp,JSON.stringify(this.data));
    }
}
  
  