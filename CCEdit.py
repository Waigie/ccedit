__author__ = 'Christoph Weygand'

import sys
import os.path
from PySide.QtCore import *
from PySide.QtGui import *
from CCEdit.Widgets import EditTab, DimensionDock


class CCEdit(QMainWindow):
    """Main Window for CCEdit"""
    def __init__(self, qt_app):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle('CCEdit')
        self.qt_app = qt_app

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.file_menu = QMenu("File")
        self.new_action = self.file_menu.addAction('New')
        self.new_action.setShortcut(QKeySequence.New)
        self.new_action.triggered.connect(self.on_new)
        self.open_action = self.file_menu.addAction('Open')
        self.open_action.setShortcut(QKeySequence.Open)
        self.open_action.triggered.connect(self.on_open)
        self.save_action = self.file_menu.addAction('Save')
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.triggered.connect(self.on_save)
        self.save_as_action = self.file_menu.addAction('Save As')
        self.save_as_action.setShortcut(QKeySequence.SaveAs)
        self.save_as_action.triggered.connect(self.on_save_as)
        self.file_menu.addSeparator()
        self.close_action = self.file_menu.addAction('Close')
        self.close_action.setShortcut(QKeySequence.Close)
        self.close_action.triggered.connect(self.qt_app.quit)

        self.menuBar().addMenu(self.file_menu)

        self.tab_widget = QTabWidget(self.central_widget)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.on_close_tab)
        layout.addWidget(self.tab_widget)

        self.central_widget.setLayout(layout)

        self.dimension_dock = DimensionDock(self)
        self.addDockWidget(Qt.DockWidgetArea(1), self.dimension_dock)

    @Slot()
    def on_new(self):
        self.tab_widget.addTab(EditTab(), 'Unsaved')

    @Slot()
    def on_open(self):
        filename = QFileDialog.getOpenFileName(None, "Open File", os.path.expanduser("~"),
                                               "Python CC (*.pycc);;Text files (*.txt);;All Files (*.*)")[0]
        tab = self.tab_widget.addTab(EditTab(filename), os.path.basename(filename))
        self.tab_widget.setCurrentIndex(tab)


    @Slot()
    def on_save(self):
        tab = self.tab_widget.currentIndex()
        self.tab_widget.widget(tab).save()
        self.__update_title()

    @Slot()
    def on_save_as(self):
        tab = self.tab_widget.currentIndex()
        self.tab_widget.widget(tab).save_sas()
        self.__update_title()

    @Slot()
    def on_close_tab(self, num):
        self.tab_widget.removeTab(num)

    def run(self):
        self.show()
        self.qt_app.exec_()

    def __update_title(self):
        tab = self.tab_widget.currentIndex()
        self.tab_widget.setTabText(tab, self.tab_widget.widget(tab).get_filename())
        pass


def main():
    qt_app = QApplication(sys.argv)
    CCEdit(qt_app).run()

if __name__ == '__main__':
    main()
