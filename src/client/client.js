const http = require('node:http');
const keepAliveAgent = new http.Agent({ keepAlive: true });
const crypto = require('crypto');

module.exports = class Client {



    constructor(parentServer, ip, port, name){
        this.generateKeyset();
        this.parentServer = parentServer;
        this.connection = {
            'ip':ip,
            'port':port
        }
        this.name = name;
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

    joinNetwork(ips) {
        ips.forEach(conn=>{
            
            this.makePostRequest(conn.ip, conn.port, '/node/join', 
            {
                'name':this.name,
                'publicKey':this.publicKey,
                'connection':this.connection
            },
            data=>{
                console.log(data);
            });
        })
    }

    makePostRequest(ip, port, path, data, callback) {
        var post_data = JSON.stringify({
            'compilation_level' : 'ADVANCED_OPTIMIZATIONS',
            'output_format': 'json',
            'output_info': 'compiled_code',
              'warning_level' : 'QUIET',
              'js_code' : data
        });
      
        var post_options = {
            host: ip,
            port: port,
            path: path,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(post_data)
            }
        };
      
        var post_req = http.request(post_options, function(res) {
            res.setEncoding('utf8');
            res.on('data', function (data) {
                callback(data);
            });
        });
      
        post_req.write(post_data);
        post_req.end();
    }
    
}



