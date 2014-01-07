__author__ = 'Christoph Weygand'

import sys
import os.path
from PySide.QtCore import *
from PySide.QtGui import *


class CCEdit(QMainWindow):
    """Main Window for CCEdit"""
    def __init__(self, qt_app):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle('CCEdit')
        self.qt_app = qt_app

        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet('margin: 0;')

        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.file_menu = QMenu("File")
        self.new_action = self.file_menu.addAction('New')
        self.new_action.triggered.connect(self.on_new)
        self.open_action = self.file_menu.addAction('Open')
        self.open_action.triggered.connect(self.on_open)
        self.save_action = self.file_menu.addAction('Save')
        self.save_action.triggered.connect(self.on_save)
        self.save_as_action = self.file_menu.addAction('Save As')
        self.save_as_action.triggered.connect(self.on_save_as)
        self.file_menu.addSeparator()
        self.close_action = self.file_menu.addAction('Close')
        self.close_action.triggered.connect(self.qt_app.quit)

        self.action_menu = QMenu("Action")
        self.compile_action = self.action_menu.addAction('Compile')

        self.menuBar().addMenu(self.file_menu)
        self.menuBar().addMenu(self.action_menu)

        self.text_widget = QTextEdit(self.central_widget)
        self.text_widget.setStyleSheet('font: 9pt "Courier";')
        layout.addWidget(self.text_widget)

        self.central_widget.setLayout(layout)

        self.current_file = None
        self.__update_title()

    @Slot()
    def on_new(self):
        self.current_file = None
        self.text_widget.setText('')

    @Slot()
    def on_open(self):
        file_name = QFileDialog.getOpenFileName(None, "Open File", os.path.expanduser("~"),
                                                "Text files (*.txt);;All Files (*.*)")[0]
        self.current_file = file_name
        with open(file_name, 'r') as file:
            data = file.read()

        self.text_widget.setText(data)
        self.__update_title()

    @Slot()
    def on_save(self):
        print(self.current_file)
        if self.current_file is not None:
            self.__save_file()
        else:
            self.on_save_as()

    @Slot()
    def on_save_as(self):
        file_name = QFileDialog.getSaveFileName(None, "Save File", os.path.expanduser("~"),
                                                "Text files (*.txt);;All Files (*.*)")[0]
        if(file_name):
            self.current_file = file_name
            self.__save_file()
            self.__update_title()

    def run(self):
        self.show()
        self.qt_app.exec_()

    def __update_title(self):
        if self.current_file is not None:
            self.setWindowTitle('CCEdit - %s' % os.path.basename(self.current_file))
        else:
            self.setWindowTitle('CCEdit - Untitled')

    def __save_file(self):
        if self.current_file is None:
            Exception('Filename not set')
        with open(self.current_file, 'w') as file:
                file.write(self.text_widget.toPlainText())

def main():
    qt_app = QApplication(sys.argv)
    CCEdit(qt_app).run()

if __name__ == '__main__':
    main()
