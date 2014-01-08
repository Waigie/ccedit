__author__ = 'Christoph Weygand'

import os.path
from PySide.QtGui import QTextEdit, QFileDialog


class CCEditTab(QTextEdit):
    def __init__(self, filename=None):
        QTextEdit.__init__(self)
        self.setStyleSheet('font: 9pt "Courier";')
        if filename:
            self.__current_file = filename
            self.__loadfile(filename)
        else:
            self.__current_file = None

    def __loadfile(self, filename):
        with open(filename, 'r') as file:
            data = file.read()
        self.setText(data)
        self.__current_file = filename

    def save(self):
        if self.__current_file:
            self.__save_to_file(self.__current_file)
        else:
            self.save_as()

    def save_as(self):
        filename = QFileDialog.getSaveFileName(None, "Save File", os.path.expanduser("~"),
                                               "Python Choice Calculus (*.pycc);;Text files (*.txt);;All Files (*.*)")[0]
        if filename:
            self.__save_to_file(filename)
            self.__current_file = filename

    def get_filename(self):
        return os.path.basename(self.__current_file)

    def __save_to_file(self, filename):
        with open(filename, 'w') as file:
            file.write(self.toPlainText())