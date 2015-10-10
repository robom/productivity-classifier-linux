from dependencies import *


class ServerCommunicator(object):
    @staticmethod
    def send(url, params):
        headers = {"Authorization": Config.session_key_header()}
        request = requests.post(url, params, headers=headers)
        if request.status_code == 401:
            Config.delete_session_key()

