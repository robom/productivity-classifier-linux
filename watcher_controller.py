from logger.dependencies import *


class WatcherController(object):
    def __init__(self):
        self.root = Tkinter.Tk()
        self.model = ActivityWatcher()
        self.view = WatcherView(self.root)
        self.is_tracking = False
        self.view.b_toggle_tracking["text"] = "Start watching"
        self.view.b_toggle_tracking.bind("<Button>", self.toggle_tracking)

    def run(self):
        self.root.title("OS Activity Watcher")
        self.root.deiconify()
        self.root.mainloop()

    def toggle_tracking(self, event):
        if self.is_tracking:
            self.model.stop()
            self.is_tracking = False
            self.view.b_toggle_tracking["text"] = "Start watching"
        else:
            self.model.start()
            self.is_tracking = True
            self.view.b_toggle_tracking["text"] = "Stop watching"
