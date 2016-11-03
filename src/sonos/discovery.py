from . import get_config
import soco


class Discovery:

    def __init__(self):
        self._settings = get_config('Discovery')
        self._speakers = soco.discover()

    def get_speaker_by_name(self, name):
        for speaker in self._speakers:
            if speaker.player_name == name:
                return speaker

        raise Exception("Speaker doesn't exist.")

    def get_master_group(self):
        master = self.get_speaker_by_name(self._settings['master'])

        for speaker in self._speakers:
            if speaker.uid != master.uid:
                speaker.join(master)

        return master.group
