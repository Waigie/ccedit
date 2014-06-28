__author__ = 'Christoph Weygand'


class ApplicationState():
    def __init__(self):
        #self.mode = 1
        #TODO all changes applied to view, update source on save or other actions
        self.source = ""
        self.view = ""
        self.config = {}
        self.dimensions = {}
        self.filename = ""
        self.changed = False

    def update_text(self, text):
        self.view = text