__author__ = 'Waigie'

import os.path
from PySide.QtCore import *
from PySide.QtGui import *


class EditTab(QTextEdit):
    def __init__(self, filename=None):
        QTextEdit.__init__(self)
        self.dimensions = []
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
                                               "Python Choice Calculus (*.pycc);;All Files (*.*)")[0]
        if filename:
            self.__save_to_file(filename)
            self.__current_file = filename

    def get_filename(self):
        return os.path.basename(self.__current_file)

    def __save_to_file(self, filename):
        with open(filename, 'w') as file:
            file.write(self.toPlainText())


class DimensionDock(QDockWidget):
    def __init__(self, parent):
        QDockWidget.__init__(self, "Dimensions", parent)

        self.setAllowedAreas(Qt.DockWidgetAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea))

        self.central_widget = QWidget(self)
        self.setWidget(self.central_widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.table_widget = QTableWidget()
        self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)
        self.table_widget.setColumnCount(4)
        self.table_widget.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setVisible(False)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.verticalHeader().setResizeMode(QHeaderView.Fixed)
        self.table_widget.verticalHeader().setDefaultSectionSize(20)

        layout.addWidget(self.table_widget)

        self.add_button = QPushButton("Add dimension")

        layout.addWidget(self.add_button)

        self.central_widget.setLayout(layout)

class DimensionDialog(QWidget):
    def __init__(self):
        QWidget.__init__(self)