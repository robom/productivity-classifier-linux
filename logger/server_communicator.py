from logger.dependencies import *


class ServerCommunicator(object):
    @staticmethod
    def send(message, params):
        logging.debug(message)
        logging.debug(params)

        timestamp = datetime.now().isoformat(' ')

        try:
            request = requests.post(url=Config.load_url(), data={
                "Token": Config.load_token(),
                "Value": str({'message': message, 'params': params, 'timestamp': timestamp}),
                "ValidFrom": timestamp
            })

            if request.status_code >= 400:
                logging.error("UXS responded with code %d: %s" % (request.status_code, request.reason))
        except Exception as e:
            logging.error(e)

