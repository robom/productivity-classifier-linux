from logger.dependencies import *


def main():
    while True:
        aw = ActivityWatcher()
        aw.watch()
        aw.end_keylog()
        LoginGui.show_login()
        if not User.is_loaded_session():
            return


if __name__ == "__main__":
    main()
