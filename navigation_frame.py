#!/usr/bin/env python3

import os
import sys
from gui import *

class NavigationFrame(GuiFrame):

    def __init__(self, parent, controller):
        sys.path.append(os.getcwd())
        GuiFrame.__init__(self, parent, controller)
        self.orders_button_image = tk.PhotoImage(file="orders.ppm")
        self.users_button_image = tk.PhotoImage(file="users.ppm")
        self.widgets = [{
            "name": "menu_border_frame",
            "class": tk.Frame,
            "init": {
                "master": None,
                "background": "#d0cbc1",
                "height": 1
            },
            "grid": {
                "row": 0,
            },
        },{
            "name": "menu_frame",
            "class": tk.Frame,
            "init": {
                "master": None,
                "background": "#fff",},
            "grid": {
                "row": 1,
                "padx": (40,40),
                "pady": 20,
            },
        },{
            "name": "orders_button",
            "class": tk.Button,
            "init": {
                "master": "menu_frame",
                "background": "#fff",
                "image": self.orders_button_image,
                "command": lambda: self.controller.raise_frame(
                    self.controller.frames['OrderFrame']
                ),
            },
            "grid": {
                "row": 0,
            },
        },{
            "name": "users_button",
            "class": tk.Button,
            "init": {
                "master": "menu_frame",
                "background": "#fff",
                "image": self.users_button_image,
                "command": lambda: self.controller.raise_frame(
                    self.controller.frames['UserFrame']
                ),
            },
            "grid": {
                "row": 0,
                "column": 1,
            },
        }]
        self.draw_widgets()


