const Block = require('./src/shared/data/block');
const Blockchain = require('./src/shared/data/blockchain');



var testchain = new Blockchain();

testchain.addNewBlock(new Block(Date.now(), "a"))
testchain.addNewBlock(new Block(Date.now(), "ab"))
testchain.addNewBlock(new Block(Date.now(), "abc"))
testchain.addNewBlock(new Block(Date.now(), "abcd"))
testchain.addNewBlock(new Block(Date.now(), "abcde"))

console.log(testchain.isChainValid());
testchain.chain[2].data = "123";

console.log(testchain.isChainValid());
