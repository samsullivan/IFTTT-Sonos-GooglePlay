from .. import Config


class Controller:

    def __init__(self, speaker):
        """Initialize a Controller object from a sonos sepaker."""
        self._config = Config('SonosController')
        self._speaker = speaker

    def change_volume(self, parameters):
        """Change speaker's volume."""
        number = int(parameters['number'])
        if parameters['verb'] == "up":
            self._speaker.volume += number
        elif parameters['verb'] == "down":
            self._speaker.volume -= number
        else:
            self._speaker.volume = number
