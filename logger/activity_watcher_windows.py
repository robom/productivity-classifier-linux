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
        self.apps = {}

        self.runner = threading.Thread(target=self.watch, name="activity_watcher")

        self.keylog = KeyEvents(self.key_changed_event)
        self.keylog_thread = threading.Thread(target=self.keylog.start, name="key_logger")
        self.keylog_thread.setDaemon(True)

        self.hook = None
        self.user32 = ctypes.windll.user32
        self.ole32 = ctypes.windll.ole32
        self.ole32.CoInitialize(0)

    def watch(self):
        self.keylog_thread.start()

        win_event_proc = WinEventProcType(self.app_change_event)
        # win_event_proc = WinEventProcType(self.callback)

        self.user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE
        self.hook = self.user32.SetWinEventHook(
            self.EVENT_FOCUS_OUT,
            self.EVENT_FOCUS_OUT,
            0,
            win_event_proc,
            0,
            0,
            self.WINEVENT_OUTOFCONTEXT
        )

        if self.hook == 0:
            logging.error('SetWinEventHook failed')

        msg = ctypes.wintypes.MSG()
        while self.user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) > 0:
            self.user32.TranslateMessage(msg)
            self.user32.DispatchMessageW(msg)

        self.user32.UnhookWinEvent(self.hook)
        self.ole32.CoUninitialize()

        self.keylog.stop()

    def start(self):
        self.runner.start()

    def stop(self):
        win32api.PostThreadMessage(self.runner.ident, win32con.WM_QUIT, 0, 0)

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

            if length <= 1:
                return

            if self.active_app:
                self.active_app.switch_out()

            name = buff.value

            try:
                handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
            except Exception as e:
                logging.error(e)
                raise e

            path = win32process.GetModuleFileNameEx(handle, 0)

            if self.apps.get(pid):
                self.apps[pid].switch_into(self.active_pid)
            else:
                self.apps[pid] = Application(pid, name, path)

            self.active_app = self.apps[pid]
            self.active_pid = pid

    def key_changed_event(self, event):
        if self.active_app:
            self.active_app.ping()
