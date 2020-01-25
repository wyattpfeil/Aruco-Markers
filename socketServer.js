let WSServer = require('ws').Server;
let server = require('http').createServer();
let app = require('./http-server');
const fs = require('fs')
// Create web socket server on top of a regular http server
let wss = new WSServer({

  server: server
});

server.on('request', app);
var connections = []
wss.on('connection', function connection(ws) {
  connections.push(ws)
  console.log("Connected!")
  ws.on('message', function incoming(message) {
    connections.forEach(function(socket, index){
      socket.send(message)
    })
  });
});




server.listen(process.env.PORT, function() {

  console.log(`http/ws server listening on ${process.env.PORT}`);
});