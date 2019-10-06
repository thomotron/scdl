#!/usr/bin/python3
##### Imports
import os
import stat
from flask import Flask, request
from youtube_dl import YoutubeDL
from threading import Thread

##### Variables
port = 2019
creds = {
    
}
base_path = '/media/downloads/scdl/'
type_paths = {
    'like': base_path + 'likes/',
    'post': base_path + 'posts/'
}

##### Flask setup
app = Flask(__name__)

##### Helper functions
# YTDL helper
def ytdl(url, path):
    ytdl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav'
        }],
        'outtmpl': path
    }
    with YoutubeDL(ytdl_opts) as ytdl:
        ytdl.download([url])

    # Set the file permissions to user: rw, group: r
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP)

##### Routes
# The only route we will ever need
@app.route('/', methods=["POST"])
def download_uri():
    try:
        # Make sure the request has the type set and we accept it
        if not request.json['type'] or request.json['type'] not in type_paths.keys():
            # Return bad request
            return '', 400

        # Check if the request has valid credentials
        if request.json['source'] in creds and request.json['secret'] == creds[request.json['source']]:
            # Format the filepath according to the request type
            filename = request.json['name'].replace('/', '(slash)') + '.wav'
            filepath = type_paths[request.json['type']] + filename

            # Download the URI through YTDL on a different thread        
            dlthread = Thread(target=ytdl, args=(request.json['uri'], filepath))
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
