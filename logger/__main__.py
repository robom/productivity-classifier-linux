from logger.dependencies import *


def main():
    while True:
        ActivityWatcher().watch()
        LoginGui.show_login()


if __name__ == "__main__":
    main()
