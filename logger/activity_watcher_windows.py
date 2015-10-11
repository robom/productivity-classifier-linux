from logger.dependencies import *

WinEventProcType = ctypes.WINFUNCTYPE(
    None,
    ctypes.wintypes.HANDLE,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.HWND,
    ctypes.wintypes.LONG,
    ctypes.wintypes.LONG,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.DWORD
)


class ActivityWatcher(object):
    EVENT_FOCUS_OUT = 0x0003
    WINEVENT_OUTOFCONTEXT = 0x0000

    def __init__(self):
        self.active_pid = -1
        self.active_app = None
        self.keylog = KeyEvents(self.key_changed_event)
        self.keylog_thread = threading.Thread(target=self.keylog.start)
        self.apps = {}
        self.hook_id = None
        self.exit_flag = True
        self.user32 = ctypes.windll.user32
        self.ole32 = ctypes.windll.ole32
        self.ole32.CoInitialize(0)

    def end_keylog(self):
        self.keylog.exit_flag = False

    def watch(self):
        self.keylog_thread.start()

        WinEventProc = WinEventProcType(self.app_change_event)

        self.user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE
        hook = self.user32.SetWinEventHook(
            self.EVENT_FOCUS_OUT,
            self.EVENT_FOCUS_OUT,
            0,
            WinEventProc,
            0,
            0,
            self.WINEVENT_OUTOFCONTEXT
        )
        if hook == 0:
            print
            'SetWinEventHook failed'

        msg = ctypes.wintypes.MSG()
        while self.user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0:
            self.user32.TranslateMessage(msg)
            self.user32.DispatchMessageW(msg)

        self.user32.UnhookWinEvent(hook)
        self.ole32.CoUninitialize()

    def callback(self, hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
        length = self.user32.GetWindowTextLengthA(hwnd)
        buff = ctypes.create_string_buffer(length + 1)
        self.user32.GetWindowTextA(hwnd, buff, length + 1)
        print(buff.value)

    def app_change_event(self, hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        if self.active_pid != pid:
            length = self.user32.GetWindowTextLengthA(hwnd)
            buff = ctypes.create_string_buffer(length + 1)
            self.user32.GetWindowTextA(hwnd, buff, length + 1)

            if length <=1: return

            if self.active_app:
                self.active_app.switch_out()

            name = buff.value

            handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
            url = win32process.GetModuleFileNameEx(handle, 0)

            if self.apps.get(pid):
                self.apps[pid].switch_into(self.active_pid)
            else:
                self.apps[pid] = Application(pid, name, url)

            self.active_app = self.apps[pid]
            self.active_pid = pid

    def key_changed_event(self, event):
        print('aaa')
        self.active_app.ping()
