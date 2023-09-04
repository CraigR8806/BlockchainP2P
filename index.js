const Server = require('./src/server/server');
var propertiesReader = require('properties-reader');


var propertyFile = process.argv[2];


var properties = propertiesReader(propertyFile);
var ip = properties.get("ip");
var port = properties.get("port");
var name = properties.get("name");
var bootstrapIPs = JSON.parse(properties.getRaw("bootstrap.ip"));



var server = new Server(ip, port, name);

server.startServer(bootstrapIPs);