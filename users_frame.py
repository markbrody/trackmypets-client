#!/usr/bin/env python3

import time
import sys
import os
from alert import *
from frames import *
from gui import *
from PIL import Image, ImageTk

import urllib.request
import io

class UsersFrame(GuiFrame):

    IDLE_TIME = 119
    THUMBNAIL_SIZE = 32

    def __init__(self, parent, controller, user):
        sys.path.append(os.getcwd())
        GuiFrame.__init__(self, parent, controller)
        self.model = user
        self.user_id = None
        self.update_last_user_interaction()

        self.widgets = [{
            "name": "header_frame",
            "class": HeaderFrame, 
            "init": {"master":None, "controller":self.controller, },
            "grid": {"row":0, "sticky": "ew", }
        },{
            "name": "body_frame",
            "class": tk.Frame,
            "init": {"master":None, "background": "#fcfcfa"},
            "grid": {"row":1, "sticky": "ew"},
        },{
            "name": "title_frame",
            "class": tk.Frame,
            "init": {"master": "body_frame", "background": "#fcfcfa"},
            "grid": {"row":0, "columnspan":2, "sticky": "new", "padx":40, },
        },{
            "name": "title_label",
            "class": tk.Label,
            "init": {"master": "title_frame", "text": "Users", "background": "#fcfcfa",
                    "anchor": "w", "font":controller.title_font},
            "grid": {"row":0, "sticky": "w", "pady":10},
        },{
            "name": "filters_frame",
            "class": tk.Frame,
            "init": {"master": "title_frame", "background": "#fcfcfa", },
            "grid": {"row":0, "column":2, "sticky": "e", },
        },{
            "name": "hr_frame",
            "class": tk.Frame,
            "init": {"master": "body_frame", "width":900, "background": "#8ab365", "height":4},
            "grid": {"row":1, "columnspan":2, "sticky": "new", "padx":40},
        },{
            "name": "treeview_frame",
            "class": TreeviewFrame,
            "init": {
                "master": "body_frame",
                "controller": self.controller,
                "belongs_to": self,
                "columns": {
                    "id": {"text": "ID", "width": 0, "exclude": True, },
                    "email": {"text": "Email", "width": 182, },
                    "name": {"text": "Name", "width": 253, },
                    "phone": {"text": "Phone", "width": 105, },
                    "created": {"text": "Time", "width": 200, },
                },
            },
            "grid": {"row":2, "column":0, "sticky": "n", "padx": (40,5), "pady":20, },
        },{
            "name": "details_frame",
            "class": tk.Frame,
            "init": {"master": "body_frame", "background": "#fcfcfa", },
            "grid": {"row":2, "column":1, "sticky": "n", "padx": (5,40), "pady":20, },
        },{
            "name": "user_email_label",
            "class": tk.Label,
            "init": {"master": "details_frame", "background": "#fcfcfa",
                     "font": "Helvetica 12 bold", "text": "Email: ", },
            "grid": {"row":0, "columnspan":2, "sticky": "nw", "pady": (3,0), },
         },{
            "name": "user_email_text",
            "class": tk.Text,
            "init": {"master": "details_frame", "background": "#fcfcfa",
                    "highlightthickness":0, "width":50, "height":1, },
            "grid": {"row":1, "columnspan":2, "sticky": "new", "padx": (5,0), },
        },{
            "name": "user_name_label",
            "class": tk.Label,
            "init": {"master": "details_frame", "background": "#fcfcfa",
                    "font": "Helvetica 12 bold", "text": "Name: ", },
            "grid": {"row":2, "sticky": "nw", "pady": (10,0), }
        },{
            "name": "user_name_text",
            "class": tk.Text,
            "init": {"master": "details_frame", "background": "#fcfcfa",
                    "highlightthickness":0, "width":24, "height":1, },
            "grid": {"row":3, "sticky": "new", "padx": (5,0), },
        },{
            "name": "user_phone_label",
            "class": tk.Label,
            "init": {"master": "details_frame", "background": "#fcfcfa",
                    "font": "Helvetica 12 bold", "text": "Phone: ", },
            "grid": {"row":2, "column":1, "sticky": "nw", "pady": (10,0), }
        },{
            "name": "user_phone_text",
            "class": tk.Text,
            "init": {"master": "details_frame", "background": "#fcfcfa",
                    "highlightthickness":0, "width":24, "height":1, },
            "grid": {"row":3, "column":1, "sticky": "new", "padx": (5,0), },
        },{
            "name": "user_address_label",
            "class": tk.Label,
            "init": {"master": "details_frame", "background": "#fcfcfa",
                    "font": "Helvetica 12 bold", "text": "Address: ", },
            "grid": {"row":4, "columnspan":2, "sticky": "nw", "pady": (10,0), }
        },{
            "name": "user_address_text",
            "class": tk.Text,
            "init": {"master": "details_frame", "background": "#fcfcfa",
                    "highlightthickness":0, "width":50, "height":4, },
            "grid": {"row":5, "columnspan":2, "sticky": "new", "padx": (5,0), },
        },{
            "name": "details_hr_1_frame",
            "class": tk.Frame,
            "init": {"master": "details_frame", "background": "#d0cbc1", "height":1, },
            "grid": {"row":6, "columnspan":2, "sticky": "ew", "pady": (10,10), }
        },{
            "name": "pets_label",
            "class": tk.Label,
            "init": {"master": "details_frame", "background": "#fcfcfa",
                    "font": "Helvetica 12 bold", "text": "Pets", },
            "grid": {"row":7, "columnspan":2, "sticky": "nw", }
        },{
            "name": "pets_frame",
            "class": tk.Frame,
            "init": {"master": "details_frame", "background": "#d0cbc1", "height":48, },
            "grid": {"row":8, "columnspan":2, "sticky": "ew", "pady": (10,10), }
        },{
            "name": "details_hr_1_frame",
            "class": tk.Frame,
            "init": {"master": "details_frame", "background": "#d0cbc1", "height":1, },
            "grid": {"row":9, "columnspan":2, "sticky": "ew", "pady": (10,10), }
        },{
            "name": "navigation_frame",
            "class": NavigationFrame, 
            "init": {
                "master": None,
                "controller": self.controller,
                "buttons": {
                    "orders": "inactive",
                    "users": "active",
                },
            },
            "grid": {"row": 2, "sticky": "nsew", }
        },]

        self.draw_widgets()
        for column in range(1, 4):
            tk.Grid.columnconfigure(self.pets_frame, column, weight=1)


    def get_users(self):
        """ Sends a GET request to the users API for a list of users """
        results = self.model.get()
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
        result = self.model.get(id=self.user_id)
        if result is not None:
            if "id" in result:
                email = result['email']
                name = result['name'] or ""
                phone = result['phone'] or ""
                address_1 = result['address_1'] or ""
                address_2 = result['address_2'] or ""
                city = result['city'] or ""
                state = result['state'] or ""
                zip = result['zip'] or ""

                user_email = email
                user_name = name
                user_phone = f"({phone[:3]}) {phone[3:6]}-{phone[6:10]}" if phone else ""
                user_address = "\n".join((
                    name,
                    f"{address}\n{address_2}" if address_2 else address_1,
                    f"{city}, {state} {zip}" if city else ""
                ))
                user_pets = result['pets']

                self.print_user_details(
                    user_email_text=user_email,
                    user_name_text=user_name,
                    user_phone_text=user_phone,
                    user_address_text=user_address,
                    user_pets=user_pets
                )
            else:
                self.process_result(result)

    def print_user_list(self):
        results = self.get_users()
        self.clear_user_details()
        try:
            if "data" in results:
                self.treeview_frame.print_list(results)
        except:
            alert = Alert("An error occurred.")

    def clear_user_details(self):
        """ Sets the current transaction_id to None and erases text values """
        self.user_id = None
        self.print_user_details()

    def print_user_details(self, **details):
        """ Replaces text values with highlighted user information """
        pets = details.pop("user_pets", [])
        for child in self.details_frame.winfo_children():
            if child.winfo_class() == "Text":
                child.delete(1.0, tk.END)
        for child in self.pets_frame.winfo_children():
            child.destroy()
        for key, value in details.items():
            text = getattr(self, key)
            text.insert(tk.END, value)
        for column in range(0, 4):
            label = tk.Label(self.pets_frame, background="#fcfcfa", height=1)
            label.grid(row=0, column=column, sticky="nsew")
        row = 0
        for pet in pets:
            self.print_pet(pet, row)
            row += 1

    def print_pet(self, pet, row):
        photo_image = ImageTk.PhotoImage(self.photo_image(pet['thumbnail_url']))
        image_label = tk.Label(self.pets_frame, background="#fcfcfa")
        image_label.configure(image=photo_image, width=self.THUMBNAIL_SIZE,
                              height=self.THUMBNAIL_SIZE)
        image_label.grid(row=row, sticky="nsew", ipadx=5, ipady=2)
        image_label.image = photo_image
        name_label = tk.Label(self.pets_frame, text=pet['name'],
                              background="#fcfcfa", anchor="w")
        name_label.grid(row=row, column=1, sticky="nsew", ipadx=5)
        pet_type_label = tk.Label(self.pets_frame, text=pet['pet_type']['name'],
                                  background="#fcfcfa")
        pet_type_label.grid(row=row, column=2, sticky="nsew", ipadx=5)
        tracking_id_label = tk.Label(self.pets_frame, text=pet['tracking_id'],
                                     background="#fcfcfa")
        tracking_id_label.grid(row=row, column=3, sticky="nsew", ipadx=5)

    def photo_image(self, url):
        request = urllib.request.urlopen(url)
        data = request.read()
        request.close()
        image = Image.open(io.BytesIO(data))
        return image.resize(
            (self.THUMBNAIL_SIZE, self.THUMBNAIL_SIZE),
            Image.ANTIALIAS
        )

    def update_last_user_interaction(self):
        self.last_user_interaction = int(time.time())

    def process_result(self, result):
        """ Verifies if user is still logged in and debugs """
        if type(result) is dict and "message" in result:
            if result['message'] == "Unauthenticated.":
                self.controller.raise_frame(self.controller.frames['LoginFrame'])
        print(result)

