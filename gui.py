#!/usr/bin/env python

import time
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox as tkmessagebox
from tkinter.ttk import Treeview, Style

class Gui(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        self.winfo_toplevel().title("Track My Pets")
        self.title_font = tk.font.Font(family="Helvetica", size=48)
        self.container = tk.Frame(self, background="#fcfcfa")
        self.container.grid(row=0, column=0)
        self.frames = {}
        self.top_frame = None
        self.button_is_fixed = False

    def button_fix(self):
        window_dimensions = self.winfo_geometry()
        delimiter = window_dimensions.find("+")
        if delimiter >= 0:
            window_dimensions = window_dimensions[0:delimiter]
        geometry = window_dimensions.split("x")
        w = int(geometry[0]) + 1
        h = int(geometry[1]) + 1
        self.geometry(f"{w}x{h}")

    def raise_frame(self, frame):
        self.top_frame = frame
        self.button_is_fixed = False
        frame.tkraise()


class GuiFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Grid.columnconfigure(self, 0, weight=1)
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

if __name__ == "__main__":
    gui = Gui()
    gui.foo = tk.Label(text="foo").grid()
    gui.mainloop()
    

