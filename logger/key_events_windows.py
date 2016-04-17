from logger.dependencies import *


# KeyboardEvent = namedtuple('KeyboardEvent', ['event_type', 'key_code',
#                                              'scan_code', 'alt_pressed',
#                                              'time'])


class KeyEvents(object):
    def __init__(self, key_pressed_callback):
        self.key_pressed_callback = key_pressed_callback
        self.exit_flag = True
        self.hm = pyHook.HookManager()
        self.hm.SubscribeKeyDown(self.key_pressed_callback)

    def start(self):
        self.hm.HookKeyboard()
        self.run()

    def run(self):
        while self.exit_flag:
            pythoncom.PumpWaitingMessages()

    def stop(self):
        self.exit_flag = False
        self.hm.UnhookKeyboard()
