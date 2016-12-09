from flask import Flask, request, jsonify
from functools import wraps
import sonos

app = Flask(__name__)             # Initializes Flask.
discovery = sonos.Discovery()     # Verifies the existence of speakers.


def success_response():
    """Returns a Flask response for a successful request."""
    return jsonify(success=True), 200


def failed_response(error="Unknown error occurred", status_code=500):
    """Returns a Flask response for a failed request."""
    print error
    return jsonify(success=False, error=error), status_code


@app.route('/')
def index():
    """A test endpoint."""
    return success_response()


@app.route('/action', methods=['POST'])
def action():
    result = request.json['result']
    parameters = result['parameters']

    room = parameters.pop('room', None)
    controllers = discovery.get_all() if not room else [discovery.get_by_name(room)]

    for controller in controllers:
        getattr(controller, result['action'])(parameters)

    return success_response()


@app.errorhandler(Exception)
def handle_bad_request(error):
    """Handle exceptions."""
    return failed_response(error.message)


# Start the Flask server.
if __name__ == "__main__":
    app.run()
