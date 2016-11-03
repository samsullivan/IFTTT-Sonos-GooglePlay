from .. import Config


class Controller:

    def __init__(self, speaker):
        """Initialize a Controller object from a sonos sepaker."""
        self._config = Config('SonosController')
        self._speaker = speaker

    def _get_all_speakers_from_group(self):
        return self._speaker.group.members if self._speaker.group else [self._speaker]

    def queue_item(self, item):
        """Replace queue with a new item."""
        self._speaker.clear_queue()
        self._speaker.add_to_queue(item)

    def play(self, play_mode='NORMAL'):
        """Adjust the speaker and start playing."""
        for speaker in self._get_all_speakers_from_group():
            speaker.volume = self._config.get('volume')

        self._speaker.play_mode = play_mode
        self._speaker.play()
