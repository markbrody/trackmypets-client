#!/usr/bin/env python3

import tkinter as tk
from alert import *
from auth import *
from version import *

class CheckUpdates(tk.Tk):

    VERSION = 1.0

    def __init__(self, token=None):
        if token is not None:
            self.version = Version(token).get()
            if "desktop_version" in self.version:
                self.compare()

    def compare(self):
        if self.VERSION < self.version['desktop_version']:
            alert = Alert("A new version is available.")


if __name__ == "__main__":
    auth = Auth()
    check_updates = CheckUpdates(auth.token)

