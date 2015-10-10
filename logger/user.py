from logger.dependencies import *


class User(object):
    @staticmethod
    def is_loaded_session():
        return not not User.session()

    @staticmethod
    def session():
        return Config.load_session_key()

    @staticmethod
    def login(email, password):
        r = requests.post(Config.LOGIN_URL,
                          data={'email': email, 'password': password, 'grant_type': 'password'})
        if r.status_code == requests.codes.ok:
            User.write_session(r.json()['access_token'])
            return 'Logged in'
        else:
            return 'Wrong name or password'

    @staticmethod
    def write_session(session):
        Config.save_session_key(session)
