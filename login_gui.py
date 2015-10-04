from tkinter import Label
from tkinter import Entry
from tkinter import Frame
from tkinter import StringVar
from tkinter import Button
from tkinter import E

from dependencies import *


class LoginGui(object):
    def __init__(self, root):
        self.welcome_text = 'Prihlaseny' if User.is_loaded_session() else "Tu bude vysledok"

        self.response_text = StringVar(root, value=self.welcome_text)

        self.top_frame = Frame(root, width=400, height=400)

        self.middle_frame = Frame(root, width=300, height=300)

        self.top_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.middle_frame.place(in_=self.top_frame, anchor='c', relx=.5, rely=.5)

        self.l_email = Label(self.middle_frame, text="Email")
        self.e_email = Entry(self.middle_frame)

        self.l_pass = Label(self.middle_frame, text="Password")
        self.e_pass = Entry(self.middle_frame, show="*")

        self.l_sign_up = Label(self.middle_frame, text="Sign up", fg='blue', cursor='hand2')

        self.l_req_result = Label(self.middle_frame, textvariable=self.response_text)

        self.b_submit = Button(self.middle_frame, text="Login")

        self.l_email.grid(row=0, sticky=E)
        self.e_email.grid(row=0, column=1)
        self.l_pass.grid(row=1, column=0, sticky=E)
        self.e_pass.grid(row=1, column=1)
        self.b_submit.grid(row=2, column=1, sticky=E)
        self.l_sign_up.grid(row=3, column=1, sticky=E)
        self.l_req_result.grid(row=4)

        self.l_sign_up.bind('<Button-1>', self.sing_up_callback)
        self.b_submit.bind('<Button-1>', self.login)

        root.mainloop()

    def login(self, event):
        response = User.login(self.e_email.get(), self.e_pass.get())
        self.response_text.set(response)

    @staticmethod
    def sing_up_callback(event):
        webbrowser.open_new(Config.SIGN_UP_URL)
