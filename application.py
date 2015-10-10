from dependencies import *


class Application(object):
    def __init__(self, pid, name, url):
        self.pid = pid
        self.name = name
        self.stopwatch = Stopwatch()
        self.stopwatch.start()
        self.send_active_thread = None
        self.send_inactive_thread = None
        self.really_active = True
        self.key_pressed = 0
        self.previous_active_pid = None
        self.url = url
        threading.Timer(4, self.send_app_start, [self.start_state()]).start()

    def switch_into(self, previous_active_pid):
        self.stopwatch.start()
        self.previous_active_pid = previous_active_pid
        if self.send_inactive_thread is not None: self.send_inactive_thread.cancel()
        self.send_active_thread = threading.Timer(4, self.send_active, [self.switch_out_state()])
        self.send_active_thread.start()

    def send_active(self, params):
        if not self.really_active:
            self.really_active = True
            ServerCommunicator.send(Config.API_URL + '/active_pages/tab_change.json', params)

    def switch_out(self):
        self.stopwatch.stop()
        if self.send_active_thread is not None: self.send_active_thread.cancel()
        self.send_inactive_thread = threading.Timer(4, self.send_inactive, [self.current_state()])
        self.send_inactive_thread.start()

    def send_inactive(self, params):
        if self.really_active:
            self.really_active = False
            ServerCommunicator.send(Config.API_URL + '/active_pages/page_lost_focus.json', params)
            self.reset_attrs()

    def current_state(self):
        return {
            'active_length': self.stopwatch.elapsed,
            'url': self.name,
            'key_pressed': self.key_pressed,
            'tab_id': self.pid
        }

    def switch_out_state(self):
        return {
            'tab_id': self.pid,
            'previous_tab_id': self.previous_active_pid
        }

    def reset_attrs(self):
        self.key_pressed = 0
        self.stopwatch.reset()

    def ping(self):
        self.key_pressed += 1
        self.stopwatch.ping()

    def send_app_start(self, params):
        ServerCommunicator.send(Config.API_URL + '/active_pages/new_page.json', params)

    def start_state(self):
        return ({
            "url": self.url,
            "tab_id": self.pid,
            "title": self.name,
            "app_type": "unix"
        })


from dependencies import *
