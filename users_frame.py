#!/usr/bin/env python3

import time
import sys
import os
# from os.path import join, dirname
from frames import *
from gui import *

class UsersFrame(GuiFrame):

    IDLE_TIME = 119

    def __init__(self, parent, controller, user):
        sys.path.append(os.getcwd())
        GuiFrame.__init__(self, parent, controller)
        self.user = user
        self.user_id = None
        self.update_last_user_interaction()

        # style = Style()
        # style.configure("style.Treeview", highlightthickness=0,  rowheight=32,
        #                 font=("Helvetica", 14),bd=3)
        # style.configure("style.Treeview.Heading", font=("Helvetica", 12, "bold"))

        self.widgets = [{
            "name":"header_frame",
            "class":HeaderFrame, 
            "init":{"master":None,"controller":self.controller,},
            "grid":{"row":0,"sticky":"ew",}
        },{
            "name":"body_frame",
            "class":tk.Frame,
            "init":{"master":None,"background":"#fcfcfa"},
            "grid":{"row":1,"sticky":"ew"},
        },{
            "name":"title_frame",
            "class":tk.Frame,
            "init":{"master":"body_frame","background":"#fcfcfa"},
            "grid":{"row":0,"columnspan":2,"sticky":"new","padx":40,},
        },{
            "name":"title_label",
            "class":tk.Label,
            "init":{"master":"title_frame","text":"Users","background":"#fcfcfa",
                    "anchor":"w","font":controller.title_font},
            "grid":{"row":0,"sticky":"w","pady":10},
        },{
            "name":"filters_frame",
            "class":tk.Frame,
            "init":{"master":"title_frame","background":"#fcfcfa",},
            "grid":{"row":0,"column":2,"sticky":"e",},
        },{
            "name":"hr_frame",
            "class":tk.Frame,
            "init":{"master":"body_frame","width":900,"background":"#8ab365","height":4},
            "grid":{"row":1,"columnspan":2,"sticky":"new","padx":40},
        },{
            "name":"treeview_frame",
            "class":TreeviewFrame,
            "init":{
                "master": "body_frame",
                "controller": self.controller,
                "belongs_to": self,
                "columns":{
                    "id": {"text": "ID", "width": 0, "exclude": True, },
                    "email": {"text": "Email", "width": 180, },
                    "name": {"text": "Name", "width": 280, },
                    "phone": {"text": "Phone", "width": 80, },
                    "created": {"text": "Time", "width": 200, },
                },
            },
            "grid":{"row":2,"column":0,"sticky":"n","padx":(40,5),"pady":20,},
        },{
            "name":"details_frame",
            "class":tk.Frame,
            "init":{"master":"body_frame","background":"#fcfcfa",},
            "grid":{"row":2,"column":1,"sticky":"n","padx":(5,40),"pady":20,},
        },{
            "name":"user_email_label",
             "class":tk.Label,
             "init":{"master":"details_frame","background":"#fcfcfa",
                     "font":"Helvetica 12 bold","text":"Email:",},
             "grid":{"row":0,"columnspan":2,"sticky":"nw","pady":(3,0),},
         },{
            "name":"user_email_text",
            "class":tk.Text,
            "init":{"master":"details_frame","background":"#fcfcfa",
                    "highlightthickness":0,"width":50,"height":1,},
            "grid":{"row":1,"columnspan":2,"sticky":"new","padx":(5,0),},
        },{
            "name":"user_name_label",
            "class":tk.Label,
            "init":{"master":"details_frame","background":"#fcfcfa",
                    "font":"Helvetica 12 bold","text":"Transaction ID:",},
            "grid":{"row":2,"columnspan":2,"sticky":"nw","pady":(10,0),}
        },{
            "name":"user_name_text",
            "class":tk.Text,
            "init":{"master":"details_frame","background":"#fcfcfa",
                    "highlightthickness":0,"width":50,"height":1,},
            "grid":{"row":3,"columnspan":2,"sticky":"new","padx":(5,0),},
        },{
            "name":"order_address_label",
            "class":tk.Label,
            "init":{"master":"details_frame","background":"#fcfcfa",
                    "font":"Helvetica 12 bold","text":"Address:",},
            "grid":{"row":4,"columnspan":2,"sticky":"nw","pady":(10,0),}
        },{
            "name":"order_address_text",
            "class":tk.Text,
            "init":{"master":"details_frame","background":"#fcfcfa",
                    "highlightthickness":0,"width":50,"height":4,},
            "grid":{"row":5,"columnspan":2,"sticky":"new","padx":(5,0),},
        },{
            "name":"details_hr_1_frame",
            "class":tk.Frame,
            "init":{"master":"details_frame","background":"#d0cbc1","height":1,},
            "grid":{"row":6,"columnspan":2,"sticky":"ew","pady":(10,10),}
        },{
            "name":"tag_description_label",
            "class":tk.Label,
            "init":{"master":"details_frame","background":"#fcfcfa",
                    "font":"Helvetica 12 bold","text":"Shape, Size, & Color:",},
            "grid":{"row":7,"sticky":"nw",}
        },{
            "name":"tag_description_text",
            "class":tk.Text,
            "init":{"master":"details_frame","background":"#fcfcfa",
                    "highlightthickness":0,"width":24,"height":1,},
            "grid":{"row":8,"sticky":"new","padx":(5,0),},
        },{
            "name":"pet_type_label",
            "class":tk.Label,
            "init":{"master":"details_frame","background":"#fcfcfa",
                    "font":"Helvetica 12 bold","text":"Pet Type:",},
            "grid":{"row":7,"column":1,"sticky":"nw",}
        },{
            "name":"pet_type_text",
            "class":tk.Text,
            "init":{"master":"details_frame","background":"#fcfcfa",
                    "highlightthickness":0,"width":24,"height":1,},
            "grid":{"row":8,"column":1,"sticky":"new","padx":(5,0),},
        },{
            "name":"tag_line_1_label",
            "class":tk.Label,
            "init":{"master":"details_frame","background":"#fcfcfa",
                    "font":"Helvetica 12 bold","text":"Tag Front:",},
            "grid":{"row":9,"column":0,"sticky":"nw","pady":(10,0),}
        },{
            "name":"tag_line_1_text",
            "class":tk.Text,
            "init":{"master":"details_frame","background":"#fcfcfa",
                    "highlightthickness":0,"width":24,"height":1,},
            "grid":{"row":10,"column":0,"sticky":"nw","padx":(5,0),},
        },{
            "name":"tag_line_2_text",
            "class":tk.Text,
            "init":{"master":"details_frame","background":"#fcfcfa",
                    "highlightthickness":0,"width":24,"height":1,},
            "grid":{"row":11,"column":0,"sticky":"nw","padx":(5,0),},
        },{
            "name":"tag_back_label",
            "class":tk.Label,
            "init":{"master":"details_frame","background":"#fcfcfa",
                    "font":"Helvetica 12 bold","text":"Tag Back:",},
            "grid":{"row":9,"column":1,"sticky":"nw","pady":(10,0),}
        },{
            "name":"sitename_text",
            "class":tk.Text,
            "init":{"master":"details_frame","background":"#fcfcfa",
                    "highlightthickness":0,"width":24,"height":1,},
            "grid":{"row":10,"column":1,"sticky":"new","padx":(5,0),},
        },{
            "name":"pet_tracking_id_text",
            "class":tk.Text,
            "init":{"master":"details_frame","background":"#fcfcfa",
                    "highlightthickness":0,"width":24,"height":1,},
            "grid":{"row":11,"column":1,"sticky":"new","padx":(5,0),},
        },{
            "name":"details_hr_2_frame",
            "class":tk.Frame,
            "init":{"master":"details_frame","background":"#d0cbc1","height":1,},
            "grid":{"row":12,"columnspan":2,"sticky":"ew","pady":(10,10),}
        },{
            "name":"update_label",
            "class":tk.Label,
            "init":{"master":"details_frame","background":"#fcfcfa",
                    "font":"Helvetica 12 bold","text":"Update Status To:",
                    "state":tk.DISABLED,},
            "grid":{"row":13,"columnspan":2,"sticky":"nw",}
        },{
            "name":"navigation_frame",
            "class":NavigationFrame, 
            "init":{"master":None,"controller":self.controller,},
            "grid":{"row":2,"sticky":"nsew",}
        },]

        self.draw_widgets()

    def get_users(self):
        """ Sends a GET request to the users API for a list of users """
        results = self.user.get()
        if results is not None:
            if "message" in results:
                self.process_result(results)
            else:
                return results
        else:
            return {}

    def show_details(self, event):
        """ Sends a GET request for an user's details """
        self.update_last_user_interaction()
        row = self.treeview_frame.tree.item(self.treeview_frame.tree.selection()[0])
        self.user_id = row['values'][0]
        result = self.user.get(id=self.user_id)
        if result is not None:
            if "id" in result:
                user_email = result['email']
                user_name = result['name']
                # order_transaction_id = result['transaction_id']
                # order_address = "\n".join((
                #     result['name'],
                #     f"{result['address_1']}\n{result['address_2']}"
                #         if result['address_2']
                #         else result['address_1'],
                #     f"{result['city']}, {result['state']} {result['zip']}"
                # ))
                # tag = result['tags'][0]
                # tag_size = "Small" if tag['is_small'] == 1 else "Large"
                # tag_description = f"{tag['tag_type']['name']}, {tag_size}, " \
                #                   f"{tag['tag_color']['name']}"
                # pet_type = tag['pet']['pet_type']['name']
                # tag_line_1 = tag['line_1']
                # tag_line_2 = tag['line_2'] or ""
                # sitename = "TrackMyPets.com"
                # pet_tracking_id = f"ID: {tag['pet']['tracking_id']}"
                self.print_user_details(
                    user_email_text=user_email,
                    user_name_text=user_name,
                    # order_address_text=order_address,
                    # tag_description_text=tag_description,pet_type_text=pet_type,
                    # tag_line_1_text=tag_line_1, tag_line_2_text=tag_line_2,
                    # sitename_text=sitename, pet_tracking_id_text=pet_tracking_id
                )
            else:
                self.process_result(result)

    def print_user_list(self):
        results = self.get_users()
        self.clear_user_details()
        self.treeview_frame.tree.delete(*self.treeview_frame.tree.get_children())
        if "data" in results:
            for result in results['data']:
                values = (
                    result['id'],
                    result['email'],
                    result['name'],
                    result['email'],
                    result['created'],
                )
                self.treeview_frame.tree.insert("", "end", text="text", values=values)

    def clear_user_details(self):
        """ Sets the current transaction_id to None and erases text values """
        self.user_id = None
        self.print_user_details()

    def print_user_details(self, **details):
        """ Replaces text values with highlighted user inromation """
        self.treeview_frame.configure_paginate_buttons()
        for child in self.details_frame.winfo_children():
            if child.winfo_class() == "Text":
                child.delete(1.0, tk.END)
        for key, value in details.items():
            text = getattr(self, key)
            text.insert(tk.END, value)

    def update_last_user_interaction(self):
        self.last_user_interaction = int(time.time())

    def process_result(self, result):
        """ Verifies if user is still logged in and debugs """
        if type(result) is dict and "message" in result:
            if result['message'] == "Unauthenticated.":
                self.controller.raise_frame(self.controller.frames['LoginFrame'])
        print(result)

