__author__ = 'Christoph Weygand'

import sys
from PySide.QtCore import *
from PySide.QtGui import *
import CCEdit.Widgets
import CCEdit.Models


class MainController(QObject):
    def __init__(self, qt_app, view):
        super(MainController, self).__init__()

        self.view = view
        self.view.set_new_handler(self.new_action)
        self.view.set_close_handler(self.close_action)
        self.view.set_add_dimension_handler(self._add_dimension)
        self.view.show()

        self.log = CCEdit.Models.Log()
        self.log.log_update.connect(self._update_log)

        self.file = CCEdit.Models.File()
        self.file.dimension_changed.connect(self.update_view)

        self.qt_app = qt_app

        self.tab_dict = dict()

    @Slot()
    def _update_log(self):
        self.view.update_log_view(self.log.__str__())

    @Slot()
    def _add_dimension(self):
        dialog = CCEdit.Widgets.DimensionDialog(self.view)
        res = dialog.exec_()
        if res == QDialog.Accepted:
            name = dialog.get_dimension_name()
            choices = dialog.get_choices()
            self.file.add_dimension(name, choices)

    @Slot()
    def update_view(self):
        pass

    def new_action(self):
        self.file.disconnect()
        self.file = CCEdit.Models.File()
        self.file.code_changed.connect(self.update_view)
        self.file.dimension_changed.connect(self.update_view)
        self._update_view()

    def close_action(self):
        self.qt_app.exit()

    def _update_view(self):
        self.view.set_text(self.file.generate_output())


def main():
    qt_app = QApplication(sys.argv)
    main_window = CCEdit.Widgets.MainWindow()
    MainController(qt_app, main_window)
    qt_app.exec_()

if __name__ == '__main__':
    main()
