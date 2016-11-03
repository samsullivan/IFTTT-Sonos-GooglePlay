import soco
import re


class Sonos:

    def __init__(self, config):
        self.settings = config.get('Sonos')

        self.speakers = soco.discover()

    def get_speaker_by_name(self, name):
        for speaker in self.speakers:
            if speaker.player_name == name:
                return speaker

        raise Exception("Speaker doesn't exist.")

    def play_song(self, ip, url):
        speaker = soco.core.SoCo(ip)

        url = re.sub(r'^https?', 'x-rincon-mp3radio', url)
        speaker.play_uri(url, title="Test")

        speaker.volume = 25
        speaker.play()
