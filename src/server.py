from . import Config
from flask import Flask, request, jsonify
from functools import wraps
import sonos

app = Flask(__name__)             # Initializes Flask.
discovery = sonos.Discovery()     # Verifies the existence of speakers.
google_play = sonos.GooglePlay()  # Verifies the existence of a Google Play Music account.


def query_param(key, default=None, required=False):
    """Returns an HTTP query parameter."""
    if required and key not in request.args:
        raise Exception("JSON param missing.")

    return request.args.get(key, default)


def json_param(key, default=None, required=False):
    """Returns a parameter from the JSON body."""
    if request.json is None:
        raise Exception("JSON body expected.")
    if required and key not in request.json:
        raise Exception("JSON param missing.")

    return request.json.get(key, default)


def get_sonos_controller():
    """Returns the sonos.Controller requested."""
    speaker_name = json_param('speaker')

    if speaker_name:
        speaker = discovery.get_speaker_by_name(speaker_name)
    else:
        group = discovery.get_master_group()
        speaker = group.coordinator

    return sonos.Controller(speaker)


def success_response():
    """Returns a Flask response for a successful request."""
    return jsonify(success=True), 200


def failed_response(error="Unknown error occurred", status_code=500):
    """Returns a Flask response for a failed request."""
    return jsonify(success=False, error=error), status_code


def validate_api(f):
    """Validates request via query param and configuration."""
    @wraps(f)
    def decorated(*args, **kwargs):
        config = Config('Flask')
        if query_param('api_key', required=True) != config.get('api_key'):
            return failed_response("Invalid API key.", 403)
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def index():
    """A non-protected test endpoint."""
    return success_response()


@app.route('/play/artist', methods=['POST'])
@validate_api
def play_artist():
    """Shuffle an artist."""
    artist = json_param('artist', required=True)

    result = google_play.find_artist(artist)
    if result is None:
        raise Exception("Artist not found.")

    controller = get_sonos_controller()
    controller.queue_item(result)
    controller.play(play_mode='SHUFFLE_NOREPEAT')

    return success_response()


@app.route('/play/station', methods=['POST'])
@validate_api
def play_station():
    """Start a station."""
    station = json_param('station', required=True)

    result = google_play.find_station(station)
    if result is None:
        raise Exception("Station not found.")

    controller = get_sonos_controller()
    controller.queue_item(result)
    controller.play()

    return success_response()


@app.errorhandler(Exception)
def handle_bad_request(error):
    """Handle exceptions."""
    return failed_response(error.message)


# Start the Flask server.
if __name__ == "__main__":
    app.run()
