const { SelfNode } = require('./src/p2p/node/selfnode');
const { Connection } = require('./src/p2p/node/connection');
var propertiesReader = require('properties-reader');


var propertyFile = process.argv[2];


var properties = propertiesReader(propertyFile);
var ip = properties.get("ip");
var port = properties.get("port");
var name = properties.get("name");
var bootstrapIPs = JSON.parse(properties.getRaw("bootstrap.ip"));


var selfNode = new SelfNode(name, new Connection(ip, port));
selfNode.startNode(bootstrapIPs);
