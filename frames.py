#!/usr/bin/env python3

from gui import *

class HeaderFrame(GuiFrame):

    def __init__(self, parent, controller):
        GuiFrame.__init__(self, parent, controller)
        self.logo_image = tk.PhotoImage(file="logo.ppm")
        self.widgets = [{
            "name": "header_frame",
            "class": tk.Frame,
            "init": {"master": None, "background": "#ffffff",},
            "grid": {"row": 0, "sticky": "ew", },
        },{
            "name": "header_label",
            "class": tk.Label,
            "init": {
                "master": "header_frame",
                 "image": self.logo_image,
                 "background": "#ffffff",
            },
            "grid": {"row":0, "sticky":"w", "padx": (40,0), "pady": 20, },
        },{
            "name": "header_border_frame",
            "class": tk.Frame,
            "init": {"master": None, "background": "#d0cbc1", "height": 1, },
            "grid": {"row": 1, "sticky": "ew", },
        }, ]
        self.draw_widgets()
        self.header_label.image = self.logo_image

class NavigationFrame(GuiFrame):

    def __init__(self, parent, controller):
        GuiFrame.__init__(self, parent, controller)
        self.dashboard_active_button_image = tk.PhotoImage(file="dashboard-active.ppm")
        self.dashboard_inactive_button_image = tk.PhotoImage(file="dashboard-inactive.ppm")
        self.orders_active_button_image = tk.PhotoImage(file="orders-active.ppm")
        self.orders_inactive_button_image = tk.PhotoImage(file="orders-inactive.ppm")
        self.users_active_button_image = tk.PhotoImage(file="users-active.ppm")
        self.users_inactive_button_image = tk.PhotoImage(file="users-inactive.ppm")
        self.widgets = [{
            "name": "menu_border_frame",
            "class": tk.Frame,
            "init": {"master": None, "background": "#d0cbc1", "height": 1, },
            "grid": {"row": 0, "sticky": "ew", },
        },{
            "name": "menu_frame",
            "class": tk.Frame,
            "init": {"master": None, "background": "#ffffff", },
            "grid": {"row": 1, "padx": (40, 40), "pady": 10, },
        },{
            "name": "orders_button",
            "class": tk.Button,
            "init": {
                "master": "menu_frame",
                "background": "#ffffff",
                "highlightthickness": 0,
                "bd": 0,
                "image": self.orders_inactive_button_image,
                "command": lambda: self.controller.raise_frame(
                    self.controller.frames['OrdersFrame']
                ),
            },
            "grid": { "row": 0, "padx": 3, },
        },{
            "name": "users_button",
            "class": tk.Button,
            "init": {
                "master": "menu_frame",
                "highlightthickness": 0,
                "bd": 0,
                "image": self.users_inactive_button_image,
                "command": lambda: self.controller.raise_frame(
                    self.controller.frames['UsersFrame']
                ),
            },
            "grid": {"row": 0, "column": 1, "padx": 3, },
        }, ]
        self.draw_widgets()
    
    def navigate_to(self, frame):
        self.controller.frames['UsersFrame']


class TreeviewFrame(GuiFrame):

    def __init__(self, parent, controller, **kwargs):
        belongs_to = kwargs.pop("belongs_to", self)
        columns = kwargs.pop("columns", {})
        GuiFrame.__init__(self, parent, controller, )
        self.configure(background="#fcfcfa")
        style = Style()
        style.configure("style.Treeview", highlightthickness=0,  rowheight=32,
                        font=("Helvetica", 14),bd=3)
        style.configure("style.Treeview.Heading", font=("Helvetica", 12, "bold"))
        self.tree = Treeview(
            self,
            show="headings",
            padding=(2,2,2,2),
            style="style.Treeview",
            height=11,
            columns=list(columns.keys())
        )

        excludes = []
        for column, foo in columns.items():
            self.tree.heading(column, text=foo['text'])
            self.tree.column(column, width=foo['width'], anchor="w")
            if "exclude" in foo:
                excludes.append(column)

        display = []
        for column in self.tree["columns"]:
            if not f"{column}" in excludes:
                display.append(column)
        self.tree["display"] = display
        self.tree.bind("<ButtonRelease-1>", belongs_to.show_details)
        self.tree.grid(row=0, sticky="ew")

        self.widgets = [{
            "name":"paginate_frame",
            "class":tk.Frame,
            "init":{"master": None, "background": "#fcfcfa", },
            "grid":{"row": 1, "sticky": "e", "pady": (8,0), },
        },{
            "name":"previous_button",
            "class":tk.Button,
            "init":{"master":"paginate_frame","width":1,"text":"<",
                    "background":"#fcfcfa","command":lambda: self.print_order_list(3),},
            "grid":{"row":0,"column":0,},
        },{
            "name":"next_button",
            "class":tk.Button,
            "init":{"master":"paginate_frame","width":1,"text":">",
                    "background":"#fcfcfa","command":lambda: self.print_order_list(4),},
            "grid":{"row":0,"column":1,},
        }, ]
        self.draw_widgets()

    def configure_paginate_buttons(self):
        self.previous_button.configure(state=tk.DISABLED)
        self.next_button.configure(state=tk.DISABLED)

