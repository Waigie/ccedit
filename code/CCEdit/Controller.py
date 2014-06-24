__author__ = 'Christoph Weygand'

from PySide.QtCore import QObject, Slot
from PySide.QtGui import QFileDialog, QApplication
from CCEdit.Models import ApplicationState


class MainController(QObject):
    def __init__(self, view):
        super(MainController, self).__init__(view)

        self.state = None
        self.view = view
        self.set_view_handler()
        self.view.show()
        self.new_handler()

    def set_view_handler(self):
        self.view.new_action.triggered.connect(self.new_handler)
        self.view.open_action.triggered.connect(self.open_handler)
        self.view.save_action.triggered.connect(self.save_handler)
        self.view.save_as_action.triggered.connect(self.save_as_handler)
        self.view.close_action.triggered.connect(self.close_handler)
        self.view.text_edit.textChanged.connect(self.text_change_handler)

    @Slot()
    def new_handler(self):
        self.state = ApplicationState()
        self.view.set_text(self.state.code)
        self.view.set_title(self.state.filename, self.state.changed)

    @Slot()
    def open_handler(self):
        filename = QFileDialog.getOpenFileName(self.view, "Open File", "", "All Files (*.*)")
        if filename[0]:
            self.state = ApplicationState()
            self.state.filename = filename[0]
            file = open(filename[0])
            self.state.code = file.read()
            file.close()
            self.view.set_text(self.state.code)
            self.view.set_title(self.state.filename, self.state.changed)

    @Slot()
    def save_handler(self):
        if self.state.filename:
            file = open(self.state.filename, mode="w")
            file.write(self.state.code)
            file.close()
            self.state.changed = False
            self.view.set_title(self.state.filename, self.state.changed)
        else:
            self.save_as_handler()
        pass

    @Slot()
    def save_as_handler(self):
        filename = QFileDialog.getSaveFileName()
        if filename[0]:
            file = open(filename[0], mode="w")
            file.write(self.state.code)
            file.close()
            self.state.filename = filename[0]
            self.state.changed = False
            self.view.set_title(self.state.filename, self.state.changed)

    @Slot()
    def close_handler(self):
        QApplication.exit()

    @Slot()
    def text_change_handler(self):
        self.state.update_text(self.view.text_edit.toPlainText())
        self.view.set_title(self.state.filename, self.state.changed)

