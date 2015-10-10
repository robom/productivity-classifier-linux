from dependencies import *

# from config import Config
# from login_gui import LoginGui
# from user import User
# from activity_watcher import ActivityWatcher


if __name__ == '__main__':
    # if User.is_loaded_session():
    while True:
        # try:
        ActivityWatcher().watch()
        # except:
        #     pass
        LoginGui.show_login()
        # else:
        #     LoginGui.show_login()
        #     ActivityWatcher().start()
