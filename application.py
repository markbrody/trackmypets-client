#!/usr/bin/env python3

import time
import sys
from auth import *
from check_updates import *
from model import *
from gui import *
from login_frame import *
from orders_frame import *
from users_frame import *

class Application:

    POLL_INTERVAL = 60

    def __init__(self):
        self.auth = Auth()
        self.check_updates = CheckUpdates(self.auth.token)
        self.order = Order(self.auth.token)
        self.user = User(self.auth.token)
        self.gui = Gui()
        self.__build()

    def __build(self):
        self.gui.configure(background="#fcfcfa")
        self.gui.frames = {
            "OrdersFrame": OrdersFrame(self.gui.container, self.gui, self.order),
            "UsersFrame": UsersFrame(self.gui.container, self.gui, self.user),
            "LoginFrame": LoginFrame(self.gui.container, self.gui, self.auth),
        }
        for frame in self.gui.frames.values():
            frame.grid(row=0, sticky="nsew")

    def run(self):
        orders_frame = self.gui.frames['OrdersFrame']
        if self.auth.token is not None:
            self.gui.frames['OrdersFrame'].print_order_list(orders_frame.order_status_id)
            self.gui.frames['UsersFrame'].print_user_list()
            self.gui.raise_frame(orders_frame)

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
                        self.gui.top_frame == orders_frame):
                    self.poller(now)
                if not self.gui.button_is_fixed:
                    self.gui.button_is_fixed = True
                    self.gui.button_fix()

    def poller(self, now):
        orders_frame = self.gui.frames['OrdersFrame']
        if now - orders_frame.last_user_interaction > orders_frame.IDLE_TIME:
            new_orders = orders_frame.get_orders(1)
            if len(new_orders) > orders_frame.new_order_count:
                orders_frame.print_order_list(1)
                self.gui.bell()
            else:
                orders_frame.print_order_list(orders_frame.order_status_id)
        time.sleep(1)


def run_application():
    application = Application()
    application.run()

if __name__ == "__main__":
    run_application()

