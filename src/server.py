from flask import Flask, request
from . import google_play

app = Flask(__name__)


@app.route('/play', methods=['POST'])
def get_station():
    urls = []

    if request.json is None:
        raise Exception("POST body must be formatted in JSON.")
    if 'station' not in request.json:
        raise Exception("Station is a required field.")

    for track in google_play.get_station_tracks(request.json['station'], 10):
        urls.append(google_play.get_mp3(track['nid']))

    return str(urls)


if __name__ == "__main__":
    app.run()
