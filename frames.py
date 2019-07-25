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

    def __init__(self, parent, controller, buttons):
        GuiFrame.__init__(self, parent, controller)
        self.buttons = buttons
        # self.dashboard_active_image = tk.PhotoImage(file="dashboard-active.ppm")
        self.orders_active_image = tk.PhotoImage(file="orders-active.ppm")
        self.users_active_image = tk.PhotoImage(file="users-active.ppm")
        # self.dashboard_inactive_image = tk.PhotoImage(file="dashboard-inactive.ppm")
        self.orders_inactive_image = tk.PhotoImage(file="orders-inactive.ppm")
        self.users_inactive_image = tk.PhotoImage(file="users-inactive.ppm")

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
        }, ]

        i = 0
        for button, state in self.buttons.items():
            self.widgets.append({
                "name": f"{button}_button",
                "class": tk.Button,
                "init": {
                    "master": "menu_frame",
                    "background": "#ffffff",
                    "highlightthickness": 0,
                    "highlightbackground": "#ffffff",
                    "bd": 0,
                    "image": getattr(self, f"{button}_{state}_image"),
                    "command": lambda frame=button: self.navigate_to(frame),
                },
                "grid": { "row": 0, "column": i, "padx": 3, },
            })
            i += 1

        self.draw_widgets()
        self.orders_button.image = self.orders_active_image
        self.users_button.image = self.users_inactive_image
    
    def navigate_to(self, frame):
        frame_index = "%sFrame" % frame.capitalize()
        self.controller.raise_frame(self.controller.frames[frame_index])


class TreeviewFrame(GuiFrame):

    def __init__(self, parent, controller, **kwargs):
        self.belongs_to = kwargs.pop("belongs_to", self)
        self.columns = kwargs.pop("columns", {})
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
            columns=list(self.columns.keys())
        )

        excludes = []
        for column, foo in self.columns.items():
            self.tree.heading(column, text=foo['text'])
            self.tree.column(column, width=foo['width'], anchor="w")
            if "exclude" in foo:
                excludes.append(column)

        display = []
        for column in self.tree["columns"]:
            if not f"{column}" in excludes:
                display.append(column)
        self.tree["display"] = display
        self.tree.bind("<ButtonRelease-1>", self.belongs_to.show_details)
        self.tree.grid(row=0, sticky="ew")
        self.widgets = [{
            "name": "paginate_frame",
            "class": tk.Frame,
            "init": {"master": None, "background": "#fcfcfa", },
            "grid": {"row": 1, "sticky": "e", "pady": (9,0), },
        },{
            "name": "previous_button",
            "class": tk.Button,
            "init": {"master": "paginate_frame", "width": 1, "text": "<",
                     "background": "#fcfcfa", "highlightbackground": "#fcfcfa", },
            "grid": {"row": 0, "column": 0, },
        },{
            "name": "next_button",
            "class": tk.Button,
            "init": {"master": "paginate_frame", "width": 1, "text": ">",
                     "background": "#fcfcfa", "highlightbackground": "#fcfcfa", },
            "grid": {"row": 0, "column": 1, },
        }, ]
        self.draw_widgets()


    def print_list(self, results):
        if results is not None:
            self.tree.delete(*self.tree.get_children())
            for result in results['data']:
                values = [result[column] for column in self.columns]
                self.tree.insert("", "end", text="text", values=values)
            self.configure_paginate_buttons(
                results['prev_page_url'],
                results['next_page_url']
            )

    def configure_paginate_buttons(self, previous_url, next_url):
        previous_state = tk.NORMAL if previous_url is not None else tk.DISABLED
        previous_command = lambda: self.print_list(self.belongs_to.model.request(url=previous_url)) if previous_url is not None else None 
        next_state = tk.NORMAL if next_url is not None else tk.DISABLED
        next_command = lambda: self.print_list(self.belongs_to.model.request(url=next_url)) if next_url is not None else None 
        self.previous_button.configure(
            state=previous_state,
            command=previous_command
        )
        self.next_button.configure(
            state=next_state,
            command=next_command
        )


