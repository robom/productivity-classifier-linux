import tkinter
import platform

if any(platform.win32_ver()):
    from win32 import win32api
    from win32 import win32gui
    from win32 import win32process
    import win32con
    import atexit
    import ctypes
    import ctypes.wintypes
    from ctypes import windll, CFUNCTYPE, POINTER, c_int, c_void_p, byref
    import pyHook
    import pythoncom
else:
    import Xlib
    import Xlib.display
    import psutil

from collections import namedtuple
import configparser
from os.path import expanduser
import requests
import webbrowser
import threading
import time

from logger.config import Config
from logger.stopwatch import Stopwatch
if any(platform.win32_ver()):
    from logger.key_events_windows import KeyEvents
else:
    from logger.key_events import KeyEvents
from logger.user import User
from logger.login_gui import LoginGui
from logger.server_communicator import ServerCommunicator
from logger.application import Application

if any(platform.win32_ver()):
    from logger.activity_watcher_windows import ActivityWatcher
else:
    from logger.activity_watcher import ActivityWatcher
