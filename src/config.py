import ConfigParser
from os import path


class Config:

    def __init__(self):
        self.parser = ConfigParser.ConfigParser()

        filename = path.join(path.dirname(__file__), '../config.cfg')
        self.parser.read(filename)

    def get(self, section, key=None):
        if key is None:
            data = {}
            for option in self.parser.options(section):
                data[option] = self.get(section, option)
            return data
        else:
            return self.parser.get(section, key)
