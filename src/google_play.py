from gmusicapi import Mobileclient


class GooglePlay:

    def __init__(self, config):
        self.api = Mobileclient()
        self.settings = config.get('GooglePlay')

        self._login()
        self.stations = self.api.get_all_stations()

    def _login(self):
        logged_in = self.api.login(self.settings['email'],
                                   self.settings['password'],
                                   Mobileclient.FROM_MAC_ADDRESS)

        if not logged_in:
            raise Exception("Failed to log in.")

    def get_station_tracks(self, name, count=100):
        station_id = self._get_station_id(name)
        return self.api.get_station_tracks(station_id, count)

    def _get_station_id(self, name):
        for station in self.stations:
            if station['name'] == name:
                return station['id']

        raise Exception("Radio station not found.")

    def get_mp3(self, song_id):
        return self.api.get_stream_url(song_id)
