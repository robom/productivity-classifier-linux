from dependencies import *

from config import Config
from login_gui import LoginGui
from user import User
from activity_watcher import ActivityWatcher


def show_login():
    root = tkinter.Tk()
    LoginGui(root)
    root.mainloop()


if __name__ == '__main__':
    if User.is_loaded_session():
        ActivityWatcher().start()
    else:
        show_login()
