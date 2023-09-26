const http = require('node:http');
const keepAliveAgent = new http.Agent({ keepAlive: true });

class Client {



    constructor(parentNode){
        this.parentNode = parentNode;
    }

    joinNetwork(ips) {
        let selfAsPeer = this.parentNode.asPeer();
        ips.forEach(conn=>{
            
            this.makePostRequest(conn, '/node/join', 
            {
                'peer': selfAsPeer
            },
            data=>{
                console.log("--------------------------");
                console.log(data);
                console.log("--------------------------");
                return;
                this.parentNode.addPeers(data.peers);
            });
        })
    }

    requestTransaction(ips, transaction) {
        ips.forEach(conn=>{
            this.makePostRequest(conn, '/transaction/request',
            {
                
            },
            data=>{
                console.log(data);
            });
        })
    }

    makePostRequest(conn, path, data, callback) {
        var post_data = JSON.stringify({
            'compilation_level' : 'ADVANCED_OPTIMIZATIONS',
            'output_format': 'json',
            'output_info': 'compiled_code',
              'warning_level' : 'QUIET',
              'js_code' : data
        });
      
        var post_options = {
            host: conn.ip,
            port: conn.port,
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



module.exports.Client = Client;