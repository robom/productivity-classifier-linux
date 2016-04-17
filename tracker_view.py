from tkinter import Frame
from tkinter import Button
from tkinter import E


class TrackerView(object):
    def __init__(self, root):
        self.top_frame = Frame(root, width=250, height=100)

        self.middle_frame = Frame(root, width=100, height=100)

        self.top_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.middle_frame.place(in_=self.top_frame, anchor='c', relx=.5, rely=.5)

        self.b_toggle_tracking = Button(self.middle_frame)
        self.b_toggle_tracking.grid(row=1, column=1, sticky=E)


