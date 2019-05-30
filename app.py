#!/usr/bin/python3
##### Imports
from flask import Flask, request
from youtube_dl import YoutubeDL
from threading import Thread

##### Variables
port = 2019
creds = {
    
}

##### Flask setup
app = Flask(__name__)

##### Helper functions
# YTDL helper
def ytdl(url, filename):
    ytdl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav'
        }],
        'outtmpl': 'audio/' + filename + '.wav'
    }
    with YoutubeDL(ytdl_opts) as ytdl:
        ytdl.download([url])

##### Routes
# The only route we will ever need
@app.route('/', methods=["POST"])
def download_uri():
    try:
        # Check if the request has valid credentials
        if request.json['source'] in creds and request.json['secret'] == creds[request.json['source']]:
            # Download the URI through YTDL on a different thread
            dlthread = Thread(target=ytdl, args=(request.json['uri'], request.json['name']))
            dlthread.start()

            # Return successfully with no further content
            return '', 204
        else:
            # Return unauthorised
            return '', 401

    except Exception as e:
        # Return an unknown failure
        return '', 500

##### Main runny bit
if __name__ == '__main__':
    app.run(port=port)
