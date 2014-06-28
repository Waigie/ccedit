__author__ = 'Christoph Weygand'

from PySide.QtCore import QObject, Slot
from PySide.QtGui import QFileDialog, QApplication
from CCEdit.Models import ApplicationState, TabState


class MainController(QObject):
    def __init__(self, view):
        super(MainController, self).__init__(view)

        self.state = ApplicationState()
        self.view = view
        self.set_view_handler()
        self.view.show()

    def set_view_handler(self):
        self.view.new_action.triggered.connect(self.new_handler)
        self.view.open_action.triggered.connect(self.open_handler)
        self.view.save_action.triggered.connect(self.save_handler)
        self.view.save_as_action.triggered.connect(self.save_as_handler)
        self.view.close_action.triggered.connect(self.close_handler)
        self.view.tabs.tabCloseRequested.connect(self.close_tab_handler)
        self.view.tabs.currentChanged.connect(self.tab_changed_handler)
        # self.view.text_edit.textChanged.connect(self.text_change_handler)

    @Slot()
    def new_handler(self):
        self.state.tabs.append(TabState())

        self.view.add_text_tab('[Untitled]')
        self.view.get_current_text_widget().textChanged.connect(self.text_change_handler)

    @Slot()
    def open_handler(self):
        filename = QFileDialog.getOpenFileName(self.view, "Open File", "", "All Files (*.*)")
        if filename[0]:
            tab_state = TabState()
            tab_state.filename = filename[0]
            file = open(filename[0])
            tab_state.source = file.read()
            file.close()
            self.state.tabs.append(tab_state)

            self.view.add_text_tab(tab_state.title())
            self.view.get_current_text_widget().setText(tab_state.source)
            self.view.get_current_text_widget().textChanged.connect(self.text_change_handler)

    @Slot()
    def save_handler(self):
        if self.state.get_active_filename():
            self.state.save_active(self.state.get_active_filename())
            self.view.set_display_title(self.state.active_title())
        else:
            self.save_as_handler()

    @Slot()
    def save_as_handler(self):
        filename = QFileDialog.getSaveFileName()
        if filename[0]:
            self.state.save_active(filename[0])
            self.view.set_display_title(self.state.active_title())

    @Slot()
    def close_handler(self):
        QApplication.exit()

    @Slot()
    def close_tab_handler(self, tab_index):
        self.state.tabs.pop(tab_index)
        self.state.active_tab = self.view.tabs.currentIndex()
        self.view.remove_tab(tab_index)

    @Slot()
    def tab_changed_handler(self, tab_index):
        self.state.active_tab = tab_index

    @Slot()
    def text_change_handler(self):
        self.state.set_active_source(self.view.get_display_text())
        self.view.set_display_title(self.state.active_title())

