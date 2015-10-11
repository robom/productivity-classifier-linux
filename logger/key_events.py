from Xlib import X, XK, display
from Xlib.ext import record
from Xlib.protocol import rq


class KeyEvents(object):
    def __init__(self, key_pressed_callback):
        self.local_dpy = display.Display()
        self.record_dpy = display.Display()
        self.key_pressed_callback = key_pressed_callback
        self.exit_flag = True

    def record_callback(self, reply):
        if reply.category != record.FromServer:
            return
        if reply.client_swapped:
            return
        if not len(reply.data) or (reply.data[0]) < 2:
            # not an event
            return

        data = reply.data
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(data, self.record_dpy.display, None, None)

            if event.type in [X.KeyPress, X.KeyRelease]:
                self.key_pressed_callback()

    def start(self):
        r = self.record_dpy.record_get_version(0, 0)

        # Create a recording context; we only want key and mouse events
        ctx = self.record_dpy.record_create_context(
            0,
            [record.AllClients],
            [{
                'core_requests': (0, 0),
                'core_replies': (0, 0),
                'ext_requests': (0, 0, 0, 0),
                'ext_replies': (0, 0, 0, 0),
                'delivered_events': (0, 0),
                'device_events': (X.KeyPress, X.KeyPress),
                'errors': (0, 0),
                'client_started': False,
                'client_died': False,
            }])

        # Enable the context; this only returns after a call to record_disable_context,
        # while calling the callback function in the meantime
        self.record_dpy.record_enable_context(ctx, self.record_callback)

        # Finally free the context
        self.record_dpy.record_free_context(ctx)
