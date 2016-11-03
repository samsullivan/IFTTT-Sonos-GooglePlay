from config import Config
from google_play import GooglePlay
from sonos import Sonos

config = Config()

google_play = GooglePlay(config)
sonos = Sonos(config)
