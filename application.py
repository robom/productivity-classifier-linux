from dependencies import *


class Application(object):
    def __init__(self, pid, name):
        self.pid = pid
        self.name = name
        self.stopwatch = Stopwatch()
        self.stopwatch.start()
        self.send_active_thread = None
        self.send_inactive_thread = None
        self.really_active = False

    def switch_into(self):
        self.stopwatch.start()
        if self.send_inactive_thread is not None: self.send_inactive_thread.cancel()
        self.send_active_thread = threading.Timer(4, self.send_active, [self.current_state()])
        self.send_active_thread.start()

    def send_active(self, params):
        if not self.really_active:
            self.really_active = True
            print(params)

    def switch_out(self):
        self.stopwatch.stop()
        if self.send_active_thread is not None: self.send_active_thread.cancel()
        self.send_inactive_thread = threading.Timer(4, self.send_inactive, [self.current_state()])
        self.send_inactive_thread.start()

    def send_inactive(self, params):
        if self.really_active:
            self.really_active = False
            print(params)
            self.stopwatch.reset()


    def current_state(self):
        return {
            'time': self.stopwatch.elapsed,
            'name': self.name,
            'pid': self.pid
        }

    def ping(self):
        self.stopwatch.ping()
