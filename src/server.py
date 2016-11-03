from flask import Flask, request, make_response
app = Flask(__name__)

import sonos
discovery = sonos.Discovery()
google_play = sonos.GooglePlay()


def json_param(key, default=None, required=False):
    if request.json is None:
        raise Exception("JSON body expected.")
    if required and key not in request.json:
        raise Exception("JSON param missing.")

    return request.json[key] if key in request.json else default


def get_speaker():
    speaker_name = json_param('speaker')

    if speaker_name is not None:
        speaker = discovery.get_speaker_by_name(speaker_name)
    else:
        group = discovery.get_master_group()
        speaker = group.coordinator

    if speaker is None:
        raise Exception("Unable to find speaker.")

    return sonos.Speaker(speaker)


@app.route('/play/artist', methods=['POST'])
def play_artist():
    speaker = get_speaker()

    artist = json_param('artist', required=True)
    result = google_play.find_artist(artist)

    if result is not None:
        speaker.queue_item(result)
        speaker.play(play_mode='SHUFFLE_NOREPEAT')

    return make_response()


@app.route('/play/station', methods=['POST'])
def play_station():
    speaker = get_speaker()

    station = json_param('station', required=True)
    result = google_play.find_station(station)

    if result is not None:
        speaker.queue_item(result)
        speaker.play()

    return make_response()


if __name__ == "__main__":
    app.run()
