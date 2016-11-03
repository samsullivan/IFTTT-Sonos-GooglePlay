from . import Config

from flask import Flask, request, jsonify
from functools import wraps
app = Flask(__name__)

import sonos
discovery = sonos.Discovery()
google_play = sonos.GooglePlay()


def query_param(key, default=None, required=False):
    if required and key not in request.args:
        raise Exception("JSON param missing.")

    return request.args.get(key, default)


def json_param(key, default=None, required=False):
    if request.json is None:
        raise Exception("JSON body expected.")
    if required and key not in request.json:
        raise Exception("JSON param missing.")

    return request.json.get(key, default)


def get_speaker():
    speaker_name = json_param('speaker')

    if speaker_name:
        speaker = discovery.get_speaker_by_name(speaker_name)
    else:
        group = discovery.get_master_group()
        speaker = group.coordinator

    return sonos.Speaker(speaker)


def success_response():
    return jsonify(success=True), 200


def failed_response(error="Unknown error occurred", status_code=500):
    return jsonify(success=False, error=error), status_code


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        config = Config('Flask')
        if query_param('api_key', required=True) != config.get('api_key'):
            return failed_response("Invalid API key.", 403)
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def index():
    return success_response()


@app.route('/play/artist', methods=['POST'])
@requires_auth
def play_artist():
    speaker = get_speaker()

    artist = json_param('artist', required=True)
    result = google_play.find_artist(artist)

    if result:
        speaker.queue_item(result)
        speaker.play(play_mode='SHUFFLE_NOREPEAT')

    return success_response()


@app.route('/play/station', methods=['POST'])
@requires_auth
def play_station():
    speaker = get_speaker()

    station = json_param('station', required=True)
    result = google_play.find_station(station)

    if result:
        speaker.queue_item(result)
        speaker.play()

    return success_response()


@app.errorhandler(Exception)
def handle_bad_request(error):
    return failed_response(error.message)


if __name__ == "__main__":
    app.run()
