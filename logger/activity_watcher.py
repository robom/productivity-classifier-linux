from logger.dependencies import *


class ActivityWatcher(object):
    display = Xlib.display.Display()
    NET_WM_NAME = display.intern_atom('_NET_WM_NAME')
    NET_WM_PID = display.intern_atom('_NET_WM_PID')
    NET_ACTIVE_WINDOW = display.intern_atom('_NET_ACTIVE_WINDOW')

    def __init__(self):
        self.root = self.display.screen().root
        self.root.change_attributes(event_mask=Xlib.X.FocusChangeMask)
        self.active_pid = -1
        self.active_app = None
        self.keylog_thread = threading.Thread(target=KeyEvents(self.key_changed_event).start)
        self.apps = {}

    def watch(self):
        if not self.keylog_thread.is_alive(): self.keylog_thread.start()
        while User.is_loaded_session():
            try:
                window_id = self.root.get_full_property(self.NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
                window = self.display.create_resource_object('window', window_id)
                window.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
                self.app_change_event(window)
            except Xlib.error.XError:
                pass
            self.display.next_event()

    def start(self):
        t = threading.Thread(target=self.watch)
        t.start()

    def app_change_event(self, window):
        pid = window.get_full_property(self.NET_WM_PID, 0).value[0]
        if self.active_pid != pid:
            name = window.get_full_property(self.NET_WM_NAME, 0)
            if name is None: return

            if self.active_app:
                self.active_app.switch_out()

            name = name.value
            url = psutil.Process(pid).exe()

            if self.apps.get(pid):
                self.apps[pid].switch_into(self.active_pid)
            else:
                self.apps[pid] = Application(pid, name, url)

            self.active_app = self.apps[pid]
            self.active_pid = pid

    def key_changed_event(self):
        self.active_app.ping()
