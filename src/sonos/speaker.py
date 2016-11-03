from .. import Config


class Speaker:

    def __init__(self, speaker):
        self._config = Config('SonosSpeaker')

        self._speaker = speaker

    def queue_item(self, item):
        self._speaker.clear_queue()
        self._speaker.add_to_queue(item)

    def play(self, play_mode='NORMAL'):
        self._speaker.play_mode = play_mode
        self._speaker.volume = self._config.get('volume')

        self._speaker.play()
