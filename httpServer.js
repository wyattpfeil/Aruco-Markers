let fs = require('fs');
let express = require('express');
let app = express();

// Let's create the regular HTTP request and response
app.get('/', function(req, res) {

  console.log('Get index');
  fs.createReadStream('./views/index.html')
  .pipe(res);
});


module.exports = app;