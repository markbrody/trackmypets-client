#!/usr/bin/env python3

import time
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
    gui.configure(background="#fcfcfa")

    gui.frames['OrderFrame'] = OrderFrame(
        gui.container,
        gui,
        application.order
    )
    gui.frames['OrderFrame'].grid(row=0, sticky="nsew")

    gui.frames['LoginFrame'] = LoginFrame(
        gui.container,
        gui,
        application.auth
    )
    gui.frames['LoginFrame'].grid(row=0, sticky="nsew")

    order_frame = gui.frames['OrderFrame']
    if application.auth.token is not None:
        gui.raise_frame(order_frame)
        order_frame.get_orders(order_frame.order_status_id)

    # gui.mainloop()
    while True:
        now = int(time.time())
        if now % 10 == 0 and gui.top_frame == order_frame:
            if now - order_frame.last_user_interaction > order_frame.IDLE_TIME:
                order_frame.get_orders(1)
            time.sleep(1)
        gui.update_idletasks()
        gui.update()

