__author__ = 'Waigie'

import json
import datetime
from PySide.QtCore import *
from CCParser.LeplGrammar import parse


class Log(QObject):

    log_update = Signal()

    def __init__(self, max_size=0):
        super(Log, self).__init__()

        self.buffer = []
        self.max_size = max_size

    def write(self, text):
        self.buffer.append(self.LogMessage(text))
        self.log_update.emit()

    def __str__(self):
        output = ""
        for line in self.buffer:
            output += line.__str__()+"\n"
        return output

    class LogMessage:
        def __init__(self, message):
            self.time = datetime.datetime.now()
            self.message = message

        def __str__(self):
            return self.time.strftime("%H:%M:%S")+": "+self.message


class Dimension:
    def __init__(self, name, choices=[]):
        self.name = name
        self.choices = choices
        self.instances = []


class DimensionInstance:
    def __init__(self):
        pass


class File(QObject):
    code_changed = Signal()
    dimension_changed = Signal()

    def __init__(self, log, filename=None):
        super(File, self).__init__()
        self.dimensions = []
        self.code = ''
        self.changed = False
        self.filename = filename
        self.log = log
        if self.filename:
            self.load_from_file(self.filename)

    def load_from_file(self, filename):
        file = open(filename, 'r')
        self.code = file.read()
        result = parse(self.code)
        if result:
            self.log.write("Parser result:\n"+str(result[0]))

    def generate_output(self):
        return self.code

    def add_dimension(self, name, choices):
        self.dimensions.append(Dimension(name, choices))
        self.dimension_changed.emit()
