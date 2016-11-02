from gmusicapi import Mobileclient


class GooglePlay:

    def __init__(self, config):
        self.api = Mobileclient()
        self.settings = config.get('GooglePlay')

        self._login()

    def _login(self):
        logged_in = self.api.login(self.settings['email'],
                                   self.settings['password'],
                                   Mobileclient.FROM_MAC_ADDRESS)

        if not logged_in:
            raise Exception('Failed to log in.')
