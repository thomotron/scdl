// Some helpful variables
var port = 8080;
var credentials = {
    
};

// Imports
var fs = require('fs'); // Filesystem
var express = require('express'); // Express
var youtubedl = require('@microlink/youtube-dl'); // Youtube-DL
var bodyParser = require('body-parser'); // Data conversion, JSON parsing

// Set up Express
var app = express();

app.use(express.json()) // Parse JSON

// Default route (only one we need, really)
app.post("/", function(req, res) {
    console.log(req.body);
    var json = req.body;
    try
    {
        if (json.secret != credentials[json.source])
        {
            res.sendStatus(401);
        }
    }
    catch (e)
    {
        //console.log(e);
        res.sendStatus(401);
    }

    // Set up ytdl
    var ytdl = youtubedl(json.uri);

    // Log ytdl downloads
    ytdl.on('info', function(info) {
        console.log('Download started');
        console.log('filename: ' + info._filename);
        console.log('size: ' + info.size);
    });

    // Start a download
    ytdl.pipe(fs.createWriteStream(json.name));

    // Reply successfully
    res.sendStatus(204);
});

// Start listening
app.listen(port, function (){
    console.log("Listening on port " + port);
});
