from .. import Config


class Controller:

    def __init__(self, speaker):
        """Initialize a Controller object from a sonos sepaker."""
        self._config = Config('SonosController')
        self._speaker = speaker

    def queue_item(self, item):
        """Replace queue with a new item."""
        self._speaker.clear_queue()
        self._speaker.add_to_queue(item)

    def play(self, play_mode='NORMAL'):
        """Adjust the speaker and start playing."""
        self._speaker.play_mode = play_mode
        self._speaker.volume = self._config.get('volume')

        self._speaker.play()
