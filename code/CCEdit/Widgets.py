__author__ = 'Waigie'

from PySide.QtCore import *
from PySide.QtGui import *
from CCEdit.Services import CCHighlighter
import ntpath


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(1024, 768))
        self.setWindowTitle('CCEdit')

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        file_menu = QMenu("File")
        self.new_action = file_menu.addAction('New')
        self.new_action.setShortcut(QKeySequence.New)
        self.open_action = file_menu.addAction('Open File')
        self.open_action.setShortcut(QKeySequence.Open)
        self.open_folder_action = file_menu.addAction('Open Folder')
        self.open_folder_action.setShortcut("Alt+F")
        self.open_folder_action.setEnabled(False)
        self.save_action = file_menu.addAction('Save')
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_as_action = file_menu.addAction('Save As')
        self.save_as_action.setShortcut(QKeySequence.SaveAs)
        file_menu.addSeparator()
        self.close_action = file_menu.addAction('Close')
        self.close_action.setShortcut(QKeySequence.Close)

        action_menu = QMenu("Action")
        self.simplify_action = action_menu.addAction('Simplify')
        self.merge_action = action_menu.addAction('Merge')
        self.merge_action.setEnabled(False)

        self.menuBar().addMenu(file_menu)
        self.menuBar().addMenu(action_menu)

        # self.text_edit = QTextEdit(self)
        # self.text_edit.setStyleSheet("font: 10pt \"Courier New\";")
        # self.text_edit.setWordWrapMode(QTextOption.NoWrap)
        # self.highlighter = CCHighlighter(self.text_edit, '#')

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)

        layout.addWidget(self.tabs)

        self.central_widget.setLayout(layout)

    def get_current_text_widget(self):
        return self.tabs.currentWidget()

    def add_text_tab(self, name):
        tab_index = self.tabs.addTab(QTextEdit(), name)
        self.tabs.setCurrentIndex(tab_index)
        return tab_index

    def remove_tab(self, tab_index):
        self.tabs.removeTab(tab_index)

    def set_display_text(self, text):
        text_edit = self.tabs.currentWidget()
        text_edit.setText(text)

    def get_display_text(self):
        return self.tabs.currentWidget().toPlainText()

    def set_display_title(self, title):
        tab_index = self.tabs.currentIndex()
        self.tabs.setTabText(tab_index, title)