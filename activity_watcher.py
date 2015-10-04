from dependencies import *


class ActivityWatcher(object):
    display = Xlib.display.Display()
    NET_WM_NAME = display.intern_atom('_NET_WM_NAME')
    NET_WM_PID = display.intern_atom('_NET_WM_PID')
    NET_ACTIVE_WINDOW = display.intern_atom('_NET_ACTIVE_WINDOW')

    def __init__(self):
        self.root = self.display.screen().root
        self.root.change_attributes(event_mask=Xlib.X.FocusChangeMask)
        self.active_pid = -1

    def watch(self):
        while True:
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
        pid = window.get_full_property(self.NET_WM_NAME, 0).value
        if self.active_pid != pid:
            self.active_pid = pid

            name = window.get_full_property(self.NET_WM_NAME, 0).value
            print(name)
