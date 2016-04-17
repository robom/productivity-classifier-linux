from logger.dependencies import *


class TrackerController(object):
    def __init__(self):
        self.root = tkinter.Tk()
        self.model = ActivityWatcher()
        self.view = TrackerView(self.root)
        self.is_tracking = False
        self.view.b_toggle_tracking["text"] = "Start tracking"
        self.view.b_toggle_tracking.bind("<Button>", self.toggle_tracking)

    def run(self):
        self.root.title("OS Activity Tracker")
        self.root.deiconify()
        self.root.mainloop()

    def toggle_tracking(self, event):
        if self.is_tracking:
            self.model.stop()
            self.is_tracking = False
            self.view.b_toggle_tracking["text"] = "Start tracking"
        else:
            self.model.start()
            self.is_tracking = True
            self.view.b_toggle_tracking["text"] = "Stop tracking"
