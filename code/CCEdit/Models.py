__author__ = 'Christoph Weygand <christophweygand@gmail.com>'

import ntpath
import collections
import json

class ApplicationState():
    def __init__(self):
        self.tabs = []
        self.active_tab = -1
        self.config = {}
        self.dimensions = collections.OrderedDict()

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

    def get_active_view(self):
        return self.tabs[self.active_tab].view

    def set_active_view(self, view, changed=True):
        if self.active_tab > -1:
            if view != self.tabs[self.active_tab].view:
                self.tabs[self.active_tab].changed = changed
            self.tabs[self.active_tab].view = view

    def get_active_filename(self):
        return self.tabs[self.active_tab].filename

    def save_active(self, filename):
        file = open(filename, mode="w")
        file.write(self.get_active_source())
        file.close()

        dimension_data = json.dumps(self.dimensions)
        directory = ntpath.dirname(filename)
        dimension_file = directory + ntpath.sep + ".ccedit"

        file = open(dimension_file, mode="w")
        file.write(dimension_data)
        file.close()

        self.tabs[self.active_tab].filename = filename
        self.tabs[self.active_tab].changed = False

    def get_active_changed(self):
        return self.tabs[self.active_tab].changed


class TabState():
    def __init__(self):
        self.source = ""
        self.view = ""
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