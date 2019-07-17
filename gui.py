#!/usr/bin/env python

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox as tkmessagebox
from tkinter.ttk import Treeview, Style

class Gui(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.winfo_toplevel().title("Track My Pets")
        self.title_font = tk.font.Font(family="Helvetica", size=48)
        self.container = tk.Frame(self, background="#fcfcfa")
        self.container.grid(row=0, column=0)
        self.frames = {}
        #  self.after(10, print("slept 10"))

    def raise_frame(self, frame_name):
        self.frames[frame_name].tkraise()

class GuiFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def draw_widgets(self):
        for widget in self.widgets:
            master = widget['init'].pop("master", None)
            if master is not None:
                parent = getattr(self, master)
                setattr(self, widget['name'], widget['class'](parent, **widget['init']))
            else:
                setattr(self, widget['name'], widget['class'](self, **widget['init']))
            w = getattr(self, widget['name'])
            w.grid(**widget['grid'])

class LoginFrame(GuiFrame):

    def __init__(self, parent, controller, auth):
        GuiFrame.__init__(self, parent, controller)
        self.auth = auth
        self.logo = tk.PhotoImage(file="images/logo.ppm")
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
            "grid":{"row":2,"columnspan":2,"sticky":"ns","padx":375,"pady":105},
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
            "init":{"master":"form_frame","text":"Login",
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
            self.controller.raise_frame("OrderFrame")
            self.controller.frames['OrderFrame'].order.token = token
            self.controller.frames['OrderFrame'].get_orders(1)

class OrderFrame(GuiFrame):

    def __init__(self, parent, controller, order):
        GuiFrame.__init__(self, parent, controller)
        self.order = order
        self.logo = tk.PhotoImage(file="images/logo.ppm")
        self.order_status = tk.IntVar()
        self.order_status_id = 1

        style = Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=3,
                        font=("Helvetica", 14), rowheight=32)
        style.configure("mystyle.Treeview.Heading", font=("Helvetica", 12, "bold"))

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
                    "command":lambda: self.get_orders(1)},
            "grid":{"row":0},
        },{
            "name":"processed_button",
            "class":tk.Button,
            "init":{"master":"navigation_frame","width":7,"text":"Processed",
                    "command":lambda: self.get_orders(2)},
            "grid":{"row":0,"column":1},
        },{
            "name":"shipped_button",
            "class":tk.Button,
            "init":{"master":"navigation_frame","width":7,"text":"Shipped",
                    "command":lambda: self.get_orders(3)},
            "grid":{"row":0,"column":2},
        },{
            "name":"canceled_button",
            "class":tk.Button,
            "init":{"master":"navigation_frame","width":7,"text":"Canceled",
                    "command":lambda: self.get_orders(4)},
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
                    "style":"mystyle.Treeview","height":13,
                    "columns":("email","transaction_id","order_status","created"),},
            "grid":{"row":2,"sticky":"n","padx":(40,5),"pady":20,},
        },{
            "name":"details_frame",
            "class":tk.Frame,
            "init":{"master":"body_frame","background":"#fcfcfa",},
            "grid":{"row":2,"column":1,"sticky":"n","padx":(5, 40),"pady":20,},
        },{
            "name":"order_email_label",
             "class":tk.Label,
             "init":{"master":"details_frame","background":"#fcfcfa",
                     "font":"Helvetica 12 bold","text":"Email:",},
             "grid":{"row":0,"columnspan":2,"sticky":"nw",},
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
            "grid":{"row":6,"columnspan":2,"sticky":"ew","pady":(10,0),}
        },{
            "name":"tag_description_label",
            "class":tk.Label,
            "init":{"master":"details_frame","background":"#fcfcfa",
                    "font":"Helvetica 12 bold","text":"Shape, Size, & Color:",},
            "grid":{"row":7,"sticky":"nw","pady":(10,0),}
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
            "grid":{"row":7,"column":1,"sticky":"nw","pady":(10,0),}
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
            "grid":{"row":12,"columnspan":2,"sticky":"ew","pady":(10,0),}
        },{
            "name":"update_label",
            "class":tk.Label,
            "init":{"master":"details_frame","background":"#fcfcfa",
                    "font":"Helvetica 12 bold","text":"Update Status To:",},
            "grid":{"row":13,"columnspan":2,"sticky":"nw","pady":(10,0),}
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
            "variable":self.order_status,"text":"Processed",},
            "grid":{"row":0,"padx":(0,30)},
        },{
            "name":"shipped_radiobutton",
            "class":tk.Radiobutton,
            "init":{"master":"update_frame","background":"#fcfcfa","value":3,
                    "variable":self.order_status,"text":"Shipped",},
            "grid":{"row":0,"column":1,"padx":(0,30)},
        },{
            "name":"canceled_radiobutton",
            "class":tk.Radiobutton,
            "init":{"master":"update_frame","background":"#fcfcfa","value":4,
                    "variable":self.order_status,"text":"Canceled",},
            "grid":{"row":0,"column":2,"padx":(0,30)},
        },{
            "name":"update_button",
            "class":tk.Button,
            "init":{"master":"update_frame","background":"#fcfcfa",
                    "text":"Update","command":lambda: self.save_order_status,},
            "grid":{"row":1,"columnspan":3,"sticky":"ew","pady":(20,0),},
        },]

        self.draw_widgets()
        self.logo_label.image = self.logo

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
        self.order_status_id = order_status_id
        self.configure_radiobuttons()
        self.print_order()
        self.orders_treeview.delete(*self.orders_treeview.get_children())
        results = self.order.get(params={"order_status_id": order_status_id})
        if type(results) is list:
            for result in results:
                values = (
                    result['email'],
                    result['transaction_id'],
                    result['order_status']['name'],
                    result['created'],
                )
                self.orders_treeview.insert("", "end", text="text", values=values)
        elif type(results) is dict:
            print(results)

    def show_order(self, event):
        # print((event.x, event.y))
        row = self.orders_treeview.item(self.orders_treeview.selection()[0])
        transaction_id = row['values'][1]
        result = self.order.get(id=transaction_id)
        if type(result) is dict:
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
            self.print_order(
                order_email_text=order_email,
                order_transaction_id_text=order_transaction_id, 
                order_address_text=order_address,
                tag_description_text=tag_description,pet_type_text=pet_type,
                tag_line_1_text=tag_line_1, tag_line_2_text=tag_line_2,
                sitename_text=sitename, pet_tracking_id_text=pet_tracking_id
            )

    def print_order(self, **details):
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

    def configure_radiobuttons(self):
        if (self.order_status_id == 2):
            processed_state = tk.DISABLED
            shipped_state = tk.NORMAL
            canceled_state = tk.NORMAL
        else:
            processed_state = tk.NORMAL if self.order_status_id == 1 else tk.DISABLED
            shipped_state = tk.NORMAL if self.order_status_id == 1 else tk.DISABLED
            canceled_state = tk.NORMAL if self.order_status_id == 1 else tk.DISABLED
        self.processed_radiobutton.configure(state=processed_state)
        self.shipped_radiobutton.configure(state=shipped_state)
        self.canceled_radiobutton.configure(state=canceled_state)
        self.update_label.configure(state=tk.DISABLED if self.order_status_id > 2 else tk.NORMAL)
        self.update_button.configure(state=tk.DISABLED if self.order_status_id > 2 else tk.NORMAL)


if __name__ == "__main__":
    gui = Gui()
    gui.mainloop()
    

