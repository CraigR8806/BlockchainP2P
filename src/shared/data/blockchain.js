const Block = require('./block');

module.exports = class Blockchain {
    constructor() {
        this.chain = [this.createGenesisBlock()];
    }


    createGenesisBlock() {
        return new Block("01/01/2017", "Genesis block", "0");
    }

    getLatestBlock() {
        return this.chain[this.chain.length - 1];
    }

    addNewBlock(block) {
        block.previousHash = this.getLatestBlock().hash;
        block.hash = block.calculateHash();
        this.chain.push(block);
    }

    isChainValid(index=this.chain.length - 1) {
        const currentBlock = this.chain[index];
        let result = false;

        if (index > 0) {
            
            const previousBlock = this.chain[index - 1];
            result = (currentBlock.hash === currentBlock.calculateHash() && 
                      currentBlock.previousHash === previousBlock.hash &&
                      this.isChainValid(index - 1));
        } else {
            result = currentBlock.hash === this.createGenesisBlock().hash;
        }
        return result;
      }
}
