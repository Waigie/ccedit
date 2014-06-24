__author__ = 'Christoph Weygand'

import sys
from PySide.QtGui import QApplication
from CCEdit.Widgets import MainWindow
from CCEdit.Controller import MainController

if __name__ == '__main__':
    qt_app = QApplication(sys.argv)
    main_window = MainWindow()
    MainController(main_window)
    qt_app.exec_()