from logger.dependencies import *


class Config(object):
    RAILS_ROOT = 'http://localhost:3009'
    API_URL = RAILS_ROOT + '/extension_api'
    LOGIN_URL = RAILS_ROOT + "/oauth/token.json"
    SIGN_UP_URL = RAILS_ROOT + '/users/sign_up'

    CONF_PATH = expanduser("~") + '/.productivity'
    config = configparser.ConfigParser()
    # config._interpolation = ConfigParser.ExtendedInterpolation()
    config.read(CONF_PATH)

    @staticmethod
    def load_session_key():
        return Config.config.get('session', 'key') if Config.config.has_option(
            'session', 'key') else None

    @staticmethod
    def session_key_header():
        return 'Bearer ' + Config.config.get('session', 'key') if Config.config.has_option(
            'session', 'key') else None

    @staticmethod
    def save_session_key(key):
        if not Config.config.has_section('session'): Config.config.add_section('session')
        Config.config.set('session', 'key', key)
        Config.save_options()

    @staticmethod
    def save_options():
        Config.config.write(open(Config.CONF_PATH, 'w+'))

    @staticmethod
    def delete_session_key():
        Config.config.remove_option('session', 'key')
        Config.save_options()
