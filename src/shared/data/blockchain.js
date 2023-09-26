const Block = require('./block');
const sha256Hash = require('../util');

module.exports = class Blockchain {
    constructor() {
        this.chain = [this.createGenesisBlock()];
        this.changePool = [];
        this.candidate = null;
    }


    createGenesisBlock() {
        return new Block("01/01/2017", "Genesis block", "0");
    }

    getLatestBlock() {
        return this.chain[this.chain.length - 1];
    }

    addNewBlock(block) {
        prepareBlockForChain(block);
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

    addToChangePool(block) {
        if(this.changePool.findIndex((b) => sha256Hash(JSON.stringify(b.block.data)) === sha256Hash(JSON.stringify(block.data))) != -1)
            this.changePool.push({'processed':false,'block':block});
    }

    processPool() {
        let unprocessed = this.changePool.filter(b=>b.processed == false);
        let block = undefined;
        if (unprocessed.length > 0) {
            let index = Math.round(Math.random()*unprocessed.length-1);
            block = unprocessed[index].block;
            prepareBlockForChain(block);
            unprocessed[index].processed = true;
        }
        return block;
    }

    prepareBlockForChain(block) {
        block.previousHash = this.getLatestBlock().hash;
        block.hash = block.calculateHash();
    }
}
