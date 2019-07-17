#!/usr/bin/env python3

from auth import *
from order import *
from gui import *
from login_frame import *
from order_frame import *

class Application:

    def __init__(self):
        self.gui = Gui()
        self.auth = Auth()
        self.order = Order(self.auth.token)


if __name__ == "__main__":
    application = Application()
    token = application.order.token
    gui = application.gui

    gui.frames['LoginFrame'] = LoginFrame(
        gui.container,
        gui,
        application.auth
    )
    gui.frames['LoginFrame'].grid(row=0, sticky="nsew")

    gui.frames['OrderFrame'] = OrderFrame(
        gui.container,
        gui,
        application.order
    )
    gui.frames['OrderFrame'].grid(row=0, sticky="nsew")

    start_frame = "OrderFrame" if application.auth.token is not None else "LoginFrame"
    gui.raise_frame(start_frame)
    gui.mainloop()

