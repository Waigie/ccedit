__author__ = 'Christoph Weygand'

import sys
from PySide.QtCore import *
from PySide.QtGui import *
import logging
import CCEdit.Widgets
import CCEdit.Models
import CCEdit.Services


class MainController(QObject):
    def __init__(self, qt_app, view):
        super(MainController, self).__init__()

        self.view = view
        self.view.set_new_handler(self.new_action)
        self.view.set_close_handler(self.close_action)
        #self.view.set_add_dimension_handler(self._add_dimension)
        self.view.open_action.triggered.connect(self.open_action)
        self.view.text_edit.textChanged.connect(self.code_changed)
        self.view.show()

        logHandler = CCEdit.Services.Logger(self.view.log_dock)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', '%H:%M:%S')
        logHandler.setFormatter(formatter)
        self.log = logging.getLogger('CCEdit')
        self.log.addHandler(logHandler)
        self.log.setLevel(logging.INFO)
        self.log.info("CCEdit stated")

        self.file = CCEdit.Models.File(self.log)

        self.qt_app = qt_app

        self.tab_dict = dict()

    @Slot()
    def _update_log(self):
        self.view.update_log_view(self.log.__str__())

    @Slot()
    def update_view(self):
        self.view.set_text(self.file.generate_output())

    @Slot()
    def open_action(self):
        filename = QFileDialog.getOpenFileName(self.view, "Open File", "", "All Files (*.*)")
        if filename[0]:
            self.file = CCEdit.Models.File(self.log, filename[0])
        else:
            self.file = CCEdit.Models.File(self.log)
        self.log.info("Open file: %s", filename[0])
        self.update_view()

    def new_action(self):
        self.log.info("New file")
        self.file = CCEdit.Models.File(self.log)
        self.file.code_changed.connect(self.update_view)
        self.file.dimension_changed.connect(self.update_view)
        self.update_view()

    def close_action(self):
        self.qt_app.exit()

    @Slot()
    def code_changed(self):
        self.file.code = self.view.text_edit.toPlainText()

    @Slot()
    def simplify_action(self):
        pass


def main():
    qt_app = QApplication(sys.argv)
    main_window = CCEdit.Widgets.MainWindow()
    MainController(qt_app, main_window)
    qt_app.exec_()

if __name__ == '__main__':
    main()
