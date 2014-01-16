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
    def __init__(self, parent_window):
        QDockWidget.__init__(self, "Dimensions", parent_window)
        self.parent_window = parent_window

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
        self.add_button.clicked.connect(self.on_add_dimension)
        layout.addWidget(self.add_button)
        self.central_widget.setLayout(layout)

        self.dialog = None

    @Slot()
    def on_add_dimension(self):
        if self.parent_window.tab_widget.currentIndex() < 0:
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Error')
            msg_box.setText('Creating dimensions is not possible without open document.')
            msg_box.exec_()
        else:
            self.dialog = DimensionDialog(self.parent_window)
            self.dialog.show()


class DimensionDialog(QDialog):
    def __init__(self, parent_window):
        QDialog.__init__(self, parent_window)
        self.parent_window = parent_window
        self.setWindowTitle('New dimension')
        self.setMinimumSize(QSize(300, 200))
        self.setMaximumSize(QSize(300, 200))

        layout = QFormLayout()

        self.dimension_name = QLineEdit()
        layout.addRow("Dimension", self.dimension_name)

        self.choices = QTextEdit()
        layout.addRow(QLabel("Choices (on per line)"))
        layout.addRow(self.choices)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        bottom_line_layout = QHBoxLayout()
        bottom_line_layout.addWidget(self.ok_button)
        bottom_line_layout.addWidget(self.cancel_button)

        layout.addRow(bottom_line_layout)

        self.setLayout(layout)

    @Slot()
    def on_cancel(self):
        self.hide()

    def on_ok(self):
        if self.parent_window.tab_widget.currentIndex() < 0:
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Error')
            msg_box.setText('Creating dimension is not possible without open document.')
            msg_box.exec_()
        else:
            pass




