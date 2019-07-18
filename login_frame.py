#!/usr/bin/env python3

import sys
import os
from gui import *

class LoginFrame(GuiFrame):

    def __init__(self, parent, controller, auth):
        sys.path.append(os.getcwd())
        GuiFrame.__init__(self, parent, controller)
        self.auth = auth
        self.logo = tk.PhotoImage(file="logo.ppm")
        self.widgets = [{
            "name":"logo_label",
            "class":tk.Label,
            "init":{"master":None,"image":self.logo,"background":"#ffffff"},
            "grid":{"row":0,"column":0,"sticky":"w","padx":(40,0),"pady":20},
        },{
            "name":"spacer_frame",
            "class":tk.Frame,
            "init":{"master":None,"width":200,"height":30,
                    "background":"#ffffff"},
            "grid":{"row":0,"column":1,"columnspan":2,"sticky":"w"},
        },{
            "name":"border_frame",
            "class":tk.Frame,
            "init":{"master":None,"background":"#d0cbc1","height":1},
            "grid":{"row":1,"column":0,"columnspan":3,"sticky":"ew"},
        },{
            "name":"body_frame",
            "class":tk.Frame,
            "init":{"master":None,"background":"#fcfcfa"},
            "grid":{"row":2,"columnspan":3,"sticky":"nsew"},
        },{
            "name":"title_label",
            "class":tk.Label,
            "init":{"master":"body_frame","text":"Login","background":"#fcfcfa",
                    "anchor":"w","font":controller.title_font},
            "grid":{"row":0,"columnspan":2,"sticky":"new","padx":40,"pady":10},
        },{
            "name":"hr_frame",
            "class":tk.Frame,
            "init":{"master":"body_frame","width":900,"background":"#8ab365",
                    "height":4},
            "grid":{"row":1,"columnspan":2,"sticky":"new","padx":40},
        },{
            "name":"form_frame",
            "class":tk.Frame,
            "init":{"master":"body_frame","background":"#fcfcfa"},
            "grid":{"row":2,"columnspan":2,"sticky":"ns","padx":410,"pady":155},
        },{
            "name":"username_label",
            "class":tk.Label,
            "init":{"master":"form_frame","background":"#fcfcfa",
                    "text":"Username:",},
            "grid":{"row":0,"sticky":"w","pady":(10,0)},
        },{
            "name":"username_entry",
            "class":tk.Entry,
            "init":{"master":"form_frame","width":40,},
            "grid":{"row":1,"sticky":"w"},
        },{
            "name":"password_label",
            "class":tk.Label,
            "init":{"master":"form_frame","background":"#fcfcfa",
                    "text":"Password:",},
            "grid":{"row":2,"sticky":"w","pady":(10,0)},
        },{
            "name":"password_entry",
            "class":tk.Entry,
            "init":{"master":"form_frame","width":40,"show":"*"},
            "grid":{"row":3,"sticky":"w"},
        },{
            "name":"login_button",
            "class":tk.Button,
            "init":{"master":"form_frame","text":"Login","highlightbackground":"#fcfcfa",
                    "command":lambda:self.login(),},
            "grid":{"row":4,"sticky":"e","pady":(10,10)},
        },]

        self.draw_widgets()
        self.logo_label.image = self.logo

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        token = self.auth.request_new_token(username=username, password=password)
        if token:
            self.controller.raise_frame(self.controller.frames['OrderFrame'])
            self.controller.frames['OrderFrame'].order.token = token
            self.controller.frames['OrderFrame'].print_order_list(1)

