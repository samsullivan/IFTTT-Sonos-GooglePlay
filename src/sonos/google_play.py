from .. import Config
from soco.music_services.music_service import MusicService
from soco.music_services.accounts import Account


class GooglePlay:

    _service = None

    def __init__(self):
        """Initialize a GooglePlay object and look for linked account."""
        self._config = Config('SonosGooglePlay')

        for account in Account.get_accounts_for_service('12345'):  # todo: right service_type
            if account.username == self._config.get('email'):
                self._service = MusicService('Google Play Music', account)
                break

        if self._service is None:
            raise Exception("Could not find Google Play Music account.")

    def _fetch_result(self, category, term):
        results = self._service.search(category=category, term=term, count=1)
        return results.popitem(False) if len(results) else None

    def find_artist(self, artist):
        """Returns an artist from a search term."""
        return self._fetch_result('artist', artist)

    def find_station(self, station):
        """Returns a station from a search term."""
        return self._fetch_result('station', station)
