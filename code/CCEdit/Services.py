__author__ = 'Waigie'

from PySide.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont
from PySide.QtCore import *
import re
import logging


class CCHighlighter(QSyntaxHighlighter):
    def __init__(self, parent, choice_marker):
        QSyntaxHighlighter.__init__(self, parent)
        self.choice_marker = choice_marker
        self.colors = [Qt.blue, Qt.red, Qt.green]
        self.choice_start = re.compile('#[A-Za-z0-9_]+<')
        self.identifier_end = re.compile('<')
        self.choice_end = re.compile('(?<=>)')

    def highlightBlock(self, text):
        state = self.previousBlockState()
        identifier = False

        for i in range(len(text)):
            if self.choice_start.match(text, i):
                state += 1
                identifier = True
            if self.identifier_end.match(text, i):
                identifier = False
            if self.choice_end.match(text, i):
                state -= 1

            if state >= 0:
                format = QTextCharFormat()
                format.setForeground(self.colors[state % len(self.colors)])
                if identifier:
                    #format.setFontItalic(True)
                    format.setFontWeight(QFont.Bold)
                self.setFormat(i, 1, format)



        self.setCurrentBlockState(state)


class Logger(logging.Handler):

    def __init__(self, container):
        logging.Handler.__init__(self)
        self.container = container

    def emit(self, record):
        msg = self.format(record)
        self.container.print(msg)
        print(self.format(record))


class Config():
    @staticmethod()
    def search_config_file(path):

        pass