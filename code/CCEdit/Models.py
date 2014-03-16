__author__ = 'Waigie'

import json
import datetime
from PySide.QtCore import *
from CCLang.Parser import LEPLParser


class File(QObject):

    def __init__(self, log, filename=None):
        super(File, self).__init__()
        self.code = ''
        self.changed = False
        self.filename = filename
        self.log = log
        if self.filename:
            self.load_from_file(self.filename)

    def load_from_file(self, filename):
        file = open(filename, 'r')
        self.code = file.read()

    def generate_output(self):
        return self.code
