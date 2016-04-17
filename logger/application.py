from logger.dependencies import *


class Application(object):
    def __init__(self, pid, name, path):
        self.pid = pid
        self.name = name
        self.stopwatch = Stopwatch()
        self.stopwatch.start()
        self.really_active = True
        self.key_pressed = 0
        self.previous_active_pid = None
        self.path = path

        self.send_app_start()

    def switch_into(self, previous_active_pid):
        self.stopwatch.start()
        self.previous_active_pid = previous_active_pid
        self.send_active(self.switch_out_state())

    def send_active(self, params):
        if not self.really_active:
            self.really_active = True
            ServerCommunicator.send('app_got_focus', params)

    def switch_out(self):
        self.stopwatch.stop()
        self.send_inactive(self.current_state())

    def send_inactive(self, params):
        if self.really_active:
            self.really_active = False
            ServerCommunicator.send('app_lost_focus', params)
            self.reset_attributes()

    def current_state(self):
        return {
            'path': self.name,
            'pid': self.pid,
            'active_length': self.stopwatch.elapsed,
            'key_pressed': self.key_pressed
        }

    def switch_out_state(self):
        return {
            'path': self.path,
            'pid': self.pid,
            'previous_pid': self.previous_active_pid
        }

    def reset_attributes(self):
        self.key_pressed = 0
        self.stopwatch.reset()

    def ping(self):
        self.key_pressed += 1
        self.stopwatch.ping()

    def send_app_start(self):
        ServerCommunicator.send('new_app_logged', {
            'path': self.path,
            'title': self.name,
            'pid': self.pid,
            'app_type': 'windows'
        })
