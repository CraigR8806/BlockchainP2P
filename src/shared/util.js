const SHA256 = require("crypto-js/sha256");


const sha256Hash = (...valuesToHash) => {
    return SHA256(valuesToHash.join('')).toString();
}

module.exports = sha256Hash;
    
