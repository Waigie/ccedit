__author__ = 'Waigie'

import json
import datetime
from PySide.QtCore import *


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


class CCFile:
    def __init__(self):
        self.dimensions = []
        self.code = ''

    def load_from_file(self, filename):
        pass
