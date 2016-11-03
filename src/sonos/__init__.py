from ..config import Config


def get_config(name):
    config = Config()
    return config.get('Sonos' + name)


__all__ = ['Discovery', 'Speaker', 'GooglePlay']
