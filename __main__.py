from logger.dependencies import *


def main():
    logging.basicConfig(filename='error.log', level=logging.ERROR)

    TrackerController().run()
    # ActivityWatcher().watch()
    # TrackerView.show()
    # while True:
        # aw = ActivityWatcher()
        # aw.watch()
        # aw.end_keylog()
        # TrackerView.show()


if __name__ == "__main__":
    main()
