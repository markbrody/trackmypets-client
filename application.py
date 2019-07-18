#!/usr/bin/env python3

import time
import sys
from auth import *
from order import *
from gui import *
from login_frame import *
from order_frame import *

class Application:

    POLL_INTERVAL = 300

    def __init__(self):
        self.gui = Gui()
        self.auth = Auth()
        self.order = Order(self.auth.token)
        self.__build()

    def __build(self):
        self.gui.configure(background="#fcfcfa")
        order_frame = OrderFrame(self.gui.container, self.gui, self.order)
        login_frame = LoginFrame(self.gui.container, self.gui, self.auth)
        self.gui.frames = {"OrderFrame": order_frame, "LoginFrame": login_frame}
        for frame in self.gui.frames.values():
            frame.grid(row=0, sticky="nsew")

    def run(self):
        order_frame = self.gui.frames['OrderFrame']
        if self.auth.token is not None:
            self.gui.raise_frame(order_frame)
            order_frame.print_order_list(order_frame.order_status_id)

        # self.gui.mainloop()
        """ Instead of running mainloop(), we'll simulate it by updating gui in
            our own loop. This way we can also poll for new orders when the user
            has been idle. """
        while True:
            try:
               self.gui.update_idletasks()
               self.gui.update()
            except:
                print("Could not update gui")
                sys.exit(1)
            else:
                now = int(time.time())
                if (now % self.POLL_INTERVAL == 0 and
                        self.gui.top_frame == order_frame):
                    self.poller(now)
                if not self.gui.button_is_fixed:
                    self.gui.button_is_fixed = True
                    self.gui.button_fix()

    def poller(self, now):
        order_frame = self.gui.frames['OrderFrame']
        if now - order_frame.last_user_interaction > order_frame.IDLE_TIME:
            new_orders = order_frame.get_orders(1)
            if len(new_orders) > order_frame.new_order_count:
                order_frame.print_order_list(1)
                self.gui.bell()
        time.sleep(1)


def run_application():
    application = Application()
    application.run()

if __name__ == "__main__":
    run_application()

