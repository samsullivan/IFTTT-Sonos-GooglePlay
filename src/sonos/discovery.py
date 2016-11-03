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

    def create_controller(self, speaker_name=None):
        """Creates a sonos.Controller from a given speaker/group."""
        if speaker_name:
            speaker = self._get_speaker_by_name(speaker_name)
        else:
            group = self._get_master_group()
            speaker = group.coordinator

        return Controller(speaker)

    def _get_speaker_by_name(self, name):
        for speaker in self._speakers:
            if speaker.player_name == name:
                return speaker

        raise Exception("Speaker doesn't exist.")

    def _get_master_group(self):
        master = self._get_speaker_by_name(self._config.get('master'))

        for speaker in self._speakers:
            if speaker.uid != master.uid:
                speaker.join(master)

        return master.group
