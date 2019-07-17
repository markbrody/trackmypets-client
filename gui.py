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
        self.top_frame = None

    def raise_frame(self, frame):
        self.top_frame = frame
        frame.tkraise()


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

if __name__ == "__main__":
    gui = Gui()
    gui.foo = tk.Label(text="foo").grid()
    gui.mainloop()
    

