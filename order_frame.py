#!/usr/bin/env python3

import time
import sys
import os
from os.path import join, dirname
from gui import *

class OrderFrame(GuiFrame):

    ORDER_STATUSES = {1: "New", 2: "Processed", 3: "Shipped", 4: "Canceled",}
    IDLE_TIME = 599

    def __init__(self, parent, controller, order):
        sys.path.append(os.getcwd())
        GuiFrame.__init__(self, parent, controller)
        self.order = order
        self.order_transaction_id = None
        self.order_status = tk.IntVar()
        self.order_status_id = 1
        self.new_order_count = 0
        self.logo = tk.PhotoImage(file="logo.ppm")
        self.update_last_user_interaction()

        style = Style()
        style.configure("style.Treeview", highlightthickness=0,  rowheight=32,
                        font=("Helvetica", 14),bd=3)
        style.configure("style.Treeview.Heading", font=("Helvetica", 12, "bold"))

        self.widgets = [{
            "name":"logo_label",
            "class":tk.Label,
            "init":{"master":None,"image":self.logo,"background":"#ffffff"},
            "grid":{"row":0,"column":0,"sticky":"w","padx":(40,0),"pady":20},
        },{
            "name":"spacer_frame",
            "class":tk.Frame,
            "init":{"master":None,"width":200,"height":30,"background":"#ffffff"},
            "grid":{"row":0,"column":1,"sticky":"w"},
        },{
            "name":"navigation_frame",
            "class":tk.Frame,
            "init":{"master":None,"background":"#ffffff"},
            "grid":{"row":0,"column":2,"sticky":"e","padx":(0,40)},
        },{
            "name":"new_button",
            "class":tk.Button,
            "init":{"master":"navigation_frame","width":7,"text":"New",
                    "command":lambda: self.print_order_list(1),},
            "grid":{"row":0},
        },{
            "name":"processed_button",
            "class":tk.Button,
            "init":{"master":"navigation_frame","width":7,"text":"Processed",
                    "command":lambda: self.print_order_list(2),},
            "grid":{"row":0,"column":1},
        },{
            "name":"shipped_button",
            "class":tk.Button,
            "init":{"master":"navigation_frame","width":7,"text":"Shipped",
                    "command":lambda: self.print_order_list(3),},
            "grid":{"row":0,"column":2},
        },{
            "name":"canceled_button",
            "class":tk.Button,
            "init":{"master":"navigation_frame","width":7,"text":"Canceled",
                    "command":lambda: self.print_order_list(4),},
            "grid":{"row":0,"column":3},
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
            "init":{"master":"body_frame","text":"Orders","background":"#fcfcfa",
                    "anchor":"w","font":controller.title_font},
            "grid":{"row":0,"columnspan":2,"sticky":"new","padx":40,"pady":10},
        },{
            "name":"hr_frame",
            "class":tk.Frame,
            "init":{"master":"body_frame","width":900,"background":"#8ab365","height":4},
            "grid":{"row":1,"columnspan":2,"sticky":"new","padx":40},
        },{
            "name":"orders_treeview",
            "class":Treeview,
            "init":{"master":"body_frame","show":"headings","padding":(2,2,2,2),
                    "style":"style.Treeview","height":13,
                    "columns":("email","transaction_id","order_status","created"),},
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
        },]

        self.draw_widgets()
        self.logo_label.image = self.logo
        self.new_button.configure(text="New")

        self.orders_treeview.heading("email", text="Email")
        self.orders_treeview.column("email", anchor="w", width=180)
        self.orders_treeview.heading("transaction_id", text="Transaction ID")
        self.orders_treeview.column("transaction_id", anchor="w", width=280)
        self.orders_treeview.heading("order_status", text="Status")
        self.orders_treeview.column("order_status", anchor="w", width=80)
        self.orders_treeview.heading("created", text="Time")
        self.orders_treeview.column("created", anchor="w", width=200)
        self.orders_treeview.grid(row=2, sticky="n", padx=(40, 5), pady=20)
        self.orders_treeview.bind("<ButtonRelease-1>", self.show_order)

    def get_orders(self, order_status_id):
        """ Sends a GET request to the orders API for a list of orders """
        results = self.order.get(params={"order_status_id": order_status_id})
        if type(results) is not list:
            self.process_result(results)
            return []
        else:
            return results

    def show_order(self, event):
        """ Sends a GET request for an order's details """
        self.update_last_user_interaction()
        row = self.orders_treeview.item(self.orders_treeview.selection()[0])
        self.order_transaction_id = row['values'][1]
        result = self.order.get(id=self.order_transaction_id)
        if "transaction_id" in result:
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
            result = self.order.put(
                id=self.order_transaction_id,
                data={
                    "order_status_id": updated_status_id,
                    "shipping_id": "N/A",
                },
            )
            if "transaction_id" in result:
                self.print_order_list(self.order_status_id)
            else:
                self.process_result(result)

    def print_order_list(self, order_status_id):
        results = self.get_orders(order_status_id)
        title_text = f"{self.ORDER_STATUSES[order_status_id]} Orders"
        self.order_status_id = order_status_id
        self.title_label.config(text=title_text)
        self.clear_order_details()
        self.orders_treeview.delete(*self.orders_treeview.get_children())
        if self.order_status_id > 1:
            self.update_last_user_interaction()
        else:
            if results is None:
                self.new_order_count = 0
            else:
                self.new_order_count = len(results)
        if results is not None:
            for result in results:
                values = (
                    result['email'],
                    result['transaction_id'],
                    result['order_status']['name'],
                    result['created'],
                )
                self.orders_treeview.insert("", "end", text="text", values=values)

    def clear_order_details(self):
        """ Sets the current transaction_id to None and erases text values """
        self.order_transaction_id = None
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
        if self.order_transaction_id is None:
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

