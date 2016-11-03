from flask import Flask, request
from . import google_play, sonos

app = Flask(__name__)


@app.route('/play', methods=['POST'])
def play():
    if request.json is None:
        raise Exception("POST body must be formatted in JSON.")
    if 'speaker' not in request.json:
        raise Exception("Speaker is required.")
    if 'station' not in request.json:
        raise Exception("Station is required.")

    speaker = sonos.get_speaker_by_name(request.json['speaker'])
    ip = speaker.ip_address

    track = google_play.get_station_tracks(request.json['station'], 1).pop()
    url = google_play.get_mp3(track['nid'])

    sonos.play_song(ip, url)

    return "Playing."


if __name__ == "__main__":
    app.run()
