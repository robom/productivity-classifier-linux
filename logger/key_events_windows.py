from logger.dependencies import *


# KeyboardEvent = namedtuple('KeyboardEvent', ['event_type', 'key_code',
#                                              'scan_code', 'alt_pressed',
#                                              'time'])


class KeyEvents(object):
    def __init__(self, key_pressed_callback):
        self.key_pressed_callback = key_pressed_callback
        # self.event_types = {
        #     win32con.WM_KEYDOWN: 'key down',
        #     win32con.WM_KEYUP: 'key up',
        #     0x104: 'key down',  # WM_SYSKEYDOWN, used for Alt key.
        #     0x105: 'key up',  # WM_SYSKEYUP, used for Alt key.
        # }
        # self.hook_id = None
        self.exit_flag = True
        self.hm = pyHook.HookManager()
        self.hm.SubscribeKeyDown(self.key_pressed_callback)

    def start(self):
        self.hm.HookKeyboard()
        while self.exit_flag:
            pythoncom.PumpWaitingMessages()
