__author__ = 'Christoph Weygand'


class ApplicationState():
    def __init__(self):
        self.mode = 1
        self.code = ""
        self.projection = ""
        self.config = {}
        self.dimensions = {}
        self.filename = ""
        self.changed = False

    def set_projection_mode(self):
        self.mode = 2

    def set_normal_mode(self):
        self.mode = 1

    def update_text(self, text):
        if self.mode == 1:
            if self.code != text:
                self.changed = True
            self.code = text
        elif self.mode == 2:
            self.projection = text