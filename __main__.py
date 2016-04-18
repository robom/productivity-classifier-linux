from logger.dependencies import *


def main():
    logging.basicConfig(filename='activity_watcher.log', level=Config.load_logging_level(),
                        format='%(asctime)s %(levelname)s: %(message)s')

    WatcherController().run()


if __name__ == "__main__":
    main()
