#!/usr/bin/env python3

import time
import sys
import os
from alert import *
from frames import *
from gui import *

class OrdersFrame(GuiFrame):

    ORDER_STATUSES = {1: "New", 2: "Processed", 3: "Shipped", 4: "Canceled",}
    IDLE_TIME = 119

    def __init__(self, parent, controller, order):
        sys.path.append(os.getcwd())
        GuiFrame.__init__(self, parent, controller)
        self.model = order
        self.order_id = None
        self.order_status = tk.IntVar()
        self.order_status_id = 1
        self.new_order_count = 0
        self.update_last_user_interaction()
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
            "init":{"master":"title_frame","text":"Orders","background":"#fcfcfa",
                    "anchor":"w","font":controller.title_font},
            "grid":{"row":0,"sticky":"w","pady":10},
        },{
            "name":"filters_frame",
            "class":tk.Frame,
            "init":{"master":"title_frame","background":"#fcfcfa",},
            "grid":{"row":0,"column":1,"sticky":"e",},
        },{
            "name":"new_button",
            "class":tk.Button,
            "init":{"master":"filters_frame","width":7,"text":"New",
                    "background":"#fcfcfa","highlightbackground":"#fcfcfa",
                    "command":lambda: self.print_order_list(1),},
            "grid":{"row":0,"column":0,"sticky":"e","padx":(5,0),},
        },{
            "name":"processed_button",
            "class":tk.Button,
            "init":{"master":"filters_frame","width":7,"text":"Processed",
                    "background":"#fcfcfa","highlightbackground":"#fcfcfa",
                    "command":lambda: self.print_order_list(2),},
            "grid":{"row":0,"column":1,"sticky":"e","padx":(5,0),},
        },{
            "name":"shipped_button",
            "class":tk.Button,
            "init":{"master":"filters_frame","width":7,"text":"Shipped",
                    "background":"#fcfcfa","highlightbackground":"#fcfcfa",
                    "command":lambda: self.print_order_list(3),},
            "grid":{"row":0,"column":2,"sticky":"e","padx":(5,0),},
        },{
            "name":"canceled_button",
            "class":tk.Button,
            "init":{"master":"filters_frame","width":7,"text":"Canceled",
                    "background":"#fcfcfa","highlightbackground":"#fcfcfa",
                    "command":lambda: self.print_order_list(4),},
            "grid":{"row":0,"column":3,"sticky":"e","padx":(5,0),},
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
                    "email": {"text": "Email", "width": 182, },
                    "transaction_id": {"text": "Transaction ID", "width": 278, },
                    "order_status_name": {"text": "Status", "width": 80, },
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
            "name":"order_email_label",
             "class":tk.Label,
             "init":{"master":"details_frame","background":"#fcfcfa",
                     "font":"Helvetica 12 bold","text":"Email:",},
             "grid":{"row":0,"columnspan":2,"sticky":"nw","pady":(3,0),},
         },{
            "name":"order_email_text",
            "class":tk.Text,
            "init":{"master":"details_frame","background":"#fcfcfa",
                    "highlightthickness":0,"width":50,"height":1,},
            "grid":{"row":1,"columnspan":2,"sticky":"new","padx":(5,0),},
        },{
            "name":"order_transaction_id_label",
            "class":tk.Label,
            "init":{"master":"details_frame","background":"#fcfcfa",
                    "font":"Helvetica 12 bold","text":"Transaction ID:",},
            "grid":{"row":2,"columnspan":2,"sticky":"nw","pady":(10,0),}
        },{
            "name":"order_transaction_id_text",
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
            "name":"update_frame",
            "class":tk.Frame,
            "init":{"master":"details_frame","background":"#fcfcfa",},
            "grid":{"row":14,"columnspan":2,"ipadx":0,"ipady":0,},
        },{
            "name":"deselect_radiobutton",
            "class":tk.Radiobutton,
            "init":{"master":"update_frame","background":"#fcfcfa","value":0,
            "variable":self.order_status,"text":"",},
            "grid":{"row":0,"padx":(0,30)},
        },{
            "name":"processed_radiobutton",
            "class":tk.Radiobutton,
            "init":{"master":"update_frame","background":"#fcfcfa","value":2,
                    "variable":self.order_status,"text":"Processed",
                    "state":tk.DISABLED,},
            "grid":{"row":0,"padx":(0,30)},
        },{
            "name":"shipped_radiobutton",
            "class":tk.Radiobutton,
            "init":{"master":"update_frame","background":"#fcfcfa","value":3,
                    "variable":self.order_status,"text":"Shipped",
                    "state":tk.DISABLED,},
            "grid":{"row":0,"column":1,"padx":(0,30)},
        },{
            "name":"canceled_radiobutton",
            "class":tk.Radiobutton,
            "init":{"master":"update_frame","background":"#fcfcfa","value":4,
                    "variable":self.order_status,"text":"Canceled",
                    "state":tk.DISABLED,},
            "grid":{"row":0,"column":2,"padx":(0,30)},
        },{
            "name":"update_button",
            "class":tk.Button,
            "init":{"master":"update_frame","background":"#fcfcfa",
                    "text":"Update","command":lambda: self.update_order(),
                    "state":tk.DISABLED,"highlightbackground":"#fcfcfa",},
            "grid":{"row":1,"columnspan":3,"sticky":"ew","pady":(20,0),},
        },{
            "name": "navigation_frame",
            "class": NavigationFrame, 
            "init": {
                "master": None,
                "controller": self.controller,
                "buttons": {
                    "orders": "active",
                    "users": "inactive",
                },
            },
            "grid": {"row": 2, "sticky": "nsew", },
        },]

        self.draw_widgets()
        tk.Grid.columnconfigure(self.title_frame, 1, weight=1)

    def get_orders(self, order_status_id):
        """ Sends a GET request to the orders API for a list of orders """
        results = self.model.get(params={"order_status_id": order_status_id})
        if results is not None:
            if "message" in results:
                self.process_result(results)
            else:
                return results
        else:
            return {}

    def show_details(self, event):
        """ Sends a GET request for an order's details """
        self.update_last_user_interaction()
        row = self.treeview_frame.tree.item(self.treeview_frame.tree.selection()[0])
        self.order_id = row['values'][0]
        result = self.model.get(id=self.order_id)
        if result is not None:
            if "id" in result:
                order_email = result['email']
                order_transaction_id = result['transaction_id']
                order_address = "\n".join((
                    result['name'],
                    f"{result['address_1']}\n{result['address_2']}"
                        if result['address_2']
                        else result['address_1'],
                    f"{result['city']}, {result['state']} {result['zip']}"
                ))
                tag = result['tags'][0]
                tag_size = "Small" if tag['is_small'] == 1 else "Large"
                tag_description = f"{tag['tag_type']['name']}, {tag_size}, " \
                                  f"{tag['tag_color']['name']}"
                pet_type = tag['pet']['pet_type']['name']
                tag_line_1 = tag['line_1']
                tag_line_2 = tag['line_2'] or ""
                sitename = "TrackMyPets.com"
                pet_tracking_id = f"ID: {tag['pet']['tracking_id']}"
                self.print_order_details(
                    order_email_text=order_email,
                    order_transaction_id_text=order_transaction_id, 
                    order_address_text=order_address,
                    tag_description_text=tag_description,pet_type_text=pet_type,
                    tag_line_1_text=tag_line_1, tag_line_2_text=tag_line_2,
                    sitename_text=sitename, pet_tracking_id_text=pet_tracking_id
                )
            else:
                self.process_result(result)

    def update_order(self):
        """ Sends a PUT request to the order API """
        self.update_last_user_interaction()
        updated_status_id = self.order_status.get()
        if updated_status_id > 0:
            result = self.model.put(
                id=self.order_id,
                data={
                    "order_status_id": updated_status_id,
                    "shipping_id": "N/A",
                },
            )
            if "id" in result:
                self.print_order_list(self.order_status_id)
            else:
                self.process_result(result)

    def print_order_list(self, order_status_id):
        results = self.get_orders(order_status_id)
        title_text = f"{self.ORDER_STATUSES[order_status_id]} Orders"
        self.title_label.config(text=title_text)
        self.order_status_id = order_status_id
        self.clear_order_details()
        try:
            if self.order_status_id > 1:
                self.update_last_user_interaction()
            else:
                if "data" in results:
                    self.new_order_count = len(results['data'])
                else:
                    self.new_order_count = 0
            if "data" in results:
                self.treeview_frame.print_list(results)
        except:
            alert = Alert("An error occurred.")

    def clear_order_details(self):
        """ Sets the current transaction_id to None and erases text values """
        self.order_id = None
        self.print_order_details()

    def print_order_details(self, **details):
        """ Replaces text values with highlighted order inromation """
        self.configure_radiobuttons()
        for child in self.details_frame.winfo_children():
            if child.winfo_class() == "Text":
                child.delete(1.0, tk.END)
        for child in self.update_frame.winfo_children():
            if child.winfo_class() == "Radiobutton":
                child.deselect()
        for key, value in details.items():
            text = getattr(self, key)
            text.insert(tk.END, value)
        self.deselect_radiobutton.select()

    def update_last_user_interaction(self):
        self.last_user_interaction = int(time.time())

    def process_result(self, result):
        """ Verifies if user is still logged in and debugs """
        if type(result) is dict and "message" in result:
            if result['message'] == "Unauthenticated.":
                self.controller.raise_frame(self.controller.frames['LoginFrame'])
        print(result)

    def configure_radiobuttons(self):
        """ Called when rewriting the order details, an order must be selected
            in order to enable the form.  Buttons are enable/disabled based on
            the order status """
        if self.order_id is None:
            self.processed_radiobutton.config(state=tk.DISABLED)
            self.shipped_radiobutton.config(state=tk.DISABLED)
            self.canceled_radiobutton.config(state=tk.DISABLED)
            self.update_label.config(state=tk.DISABLED)
            self.update_button.config(state=tk.DISABLED)
        else:
            if (self.order_status_id == 2):
                processed_state = tk.DISABLED
                shipped_state = tk.NORMAL
                # canceled_state = tk.NORMAL
                canceled_state = tk.DISABLED # Only cancel new orders
            else:
                processed_state = tk.NORMAL if self.order_status_id == 1 else tk.DISABLED
                shipped_state = tk.NORMAL if self.order_status_id == 1 else tk.DISABLED
                canceled_state = tk.NORMAL if self.order_status_id == 1 else tk.DISABLED
            self.processed_radiobutton.config(state=processed_state)
            self.shipped_radiobutton.config(state=shipped_state)
            self.canceled_radiobutton.config(state=canceled_state)
            self.update_label.config(state=tk.DISABLED if self.order_status_id > 2 else tk.NORMAL)
            self.update_button.config(state=tk.DISABLED if self.order_status_id > 2 else tk.NORMAL)

