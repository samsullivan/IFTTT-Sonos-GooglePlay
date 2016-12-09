from .. import Config
from controller import Controller
import soco


class Discovery:

    def __init__(self):
        """Initialize a Discovery object and look for Sonos speakers."""
        self._config = Config('SonosDiscovery')

        self._speakers = soco.discover()
        if self._speakers is None:
            raise Exception("No speakers found.")

    def get_all(self):
        controllers = []
        for speaker in self._speakers:
            controller = Controller(speaker)
            controllers.append(controller)
        return controllers

    def get_by_name(self, speaker_name):
        for speaker in self._speakers:
            if speaker.player_name == speaker_name:
                controller = Controller(speaker)
                return controller

        raise Exception("Speaker not found.")
