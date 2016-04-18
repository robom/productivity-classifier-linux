from logger.dependencies import *


class Config(object):
    CONF_PATH = 'activity_watcher.ini'
    config = ConfigParser.ConfigParser()
    config.read(CONF_PATH)

    @staticmethod
    def load_url():
        return Config.config.get('UXLabClass', 'url') if Config.config.has_option(
            'UXLabClass', 'url') else None

    @staticmethod
    def load_token():
        return Config.config.get('UXLabClass', 'token') if Config.config.has_option(
            'UXLabClass', 'token') else None

    @staticmethod
    def load_logging_level():
        return Config.config.get('Logging', 'level') if Config.config.has_option(
            'Logging', 'level') else None
