#!/usr/bin/env python3

import tkinter as tk

class Alert(tk.Tk):

    def __init__(self, text=None):
        self.text = text
        self.open()

    def open(self):
        self.root = tk.Tk()
        self.root.winfo_toplevel().title("Track My Pets")
        bold = tk.Label(self.root, text="Notice:", font="Helvetica 14 bold")
        bold.grid(row=0, padx=(10, 0), pady=(10, 0))
        text = tk.Label(self.root, text=self.text, font="Helvetica 14")
        text.grid(row=0, column=1, padx=(0, 10), pady=(10, 0))
        button = tk.Button(self.root, text="OK", command=self.close)
        button.grid(row=1, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        self.root.after(250, self.resize)
        self.root.mainloop()

    def close(self):
        self.root.destroy()

    def resize(self):
        window_dimensions = self.root.winfo_geometry()
        delimiter = window_dimensions.find("+")
        if delimiter >= 0:
            window_dimensions = window_dimensions[0:delimiter]
        geometry = window_dimensions.split("x")
        w = int(geometry[0]) + 1
        h = int(geometry[1]) + 1
        self.root.geometry(f"{w}x{h}")


if __name__ == "__main__":
    alert = Alert("foo")

