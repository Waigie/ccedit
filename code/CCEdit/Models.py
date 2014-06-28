__author__ = 'Christoph Weygand'

import ntpath


class ApplicationState():
    def __init__(self):
        self.tabs = []
        self.active_tab = -1
        self.config = {}
        self.dimensions = {}

    def update_view(self, view):
        if self.active_tab > -1:
            self.tabs[self.active_tab].view = view

    def active_title(self):
        return self.tabs[self.active_tab].title()

    def get_active_source(self):
        return self.tabs[self.active_tab].source

    def set_active_source(self, source):
        if self.active_tab > -1:
            if source != self.tabs[self.active_tab].source:
                self.tabs[self.active_tab].changed = True
            self.tabs[self.active_tab].source = source

    def get_active_filename(self):
        return self.tabs[self.active_tab].filename

    def save_active(self, filename):
        file = open(filename, mode="w")
        file.write(self.get_active_source())
        file.close()
        self.tabs[self.active_tab].filename = filename
        self.tabs[self.active_tab].changed = False


class TabState():
    def __init__(self):
        self.source = ""
        self.view = ""
        self.config = {}
        self.dimensions = {}
        self.filename = ""
        self.changed = False

    def title(self):
        if self.filename:
            title = ntpath.basename(self.filename)
        else:
            title = "[Untitled]"
        if self.changed:
            title += " *"
        return title