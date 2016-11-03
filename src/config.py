import ConfigParser
from os import path


class Config:

    def __init__(self, section):
        """Initialize a Config object with a specific section."""
        self._parser = ConfigParser.ConfigParser()

        filename = path.join(path.dirname(__file__), '../config.cfg')
        self._parser.read(filename)

        self._section = self._get_section(section)

    def _get_section(self, section):
        data = {}
        for option in self._parser.options(section):
            data[option] = self._parser.get(section, option)
        return data

    def get(self, option, default=None):
        """Returns the configuration option's value."""
        return self._section.get(option, default)
