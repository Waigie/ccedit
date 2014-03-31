__author__ = 'Waigie'

import os.path
from PySide.QtCore import *
from PySide.QtGui import *
from CCEdit.Services import CCHighlighter


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
        self.new_action.triggered.connect(self.on_new)
        self.open_action = file_menu.addAction('Open')
        self.open_action.setShortcut(QKeySequence.Open)
        self.open_action.triggered.connect(self.on_open)
        self.save_action = file_menu.addAction('Save')
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.triggered.connect(self.on_save)
        self.save_as_action = file_menu.addAction('Save As')
        self.save_as_action.setShortcut(QKeySequence.SaveAs)
        self.save_as_action.triggered.connect(self.on_save_as)
        file_menu.addSeparator()
        self.close_action = file_menu.addAction('Close')
        self.close_action.setShortcut(QKeySequence.Close)
        self.close_action.triggered.connect(self.on_close)

        self.new_handler = None
        self.open_handler = None
        self.save_handler = None
        self.save_as_handler = None
        self.close_handler = None
        self.add_dimension_handler = None

        action_menu = QMenu("Action")
        self.simplify_action = action_menu.addAction('Simplify')
        self.merge_action = action_menu.addAction('Merge')

        self.menuBar().addMenu(file_menu)
        self.menuBar().addMenu(action_menu)

        self.text_edit = QTextEdit(self)
        self.text_edit.setStyleSheet("font: 10pt \"Courier New\";")
        self.text_edit.setWordWrapMode(QTextOption.NoWrap)
        self.highlighter = CCHighlighter(self.text_edit, '#')

        layout.addWidget(self.text_edit)

        self.central_widget.setLayout(layout)

        self.log_dock = LogDock(self)
        self.addDockWidget(Qt.DockWidgetArea(Qt.BottomDockWidgetArea), self.log_dock)

        self.dimension_dock = DimensionDock(self)
        self.addDockWidget(Qt.DockWidgetArea(Qt.LeftDockWidgetArea), self.dimension_dock)

    def update_log_view(self, data):
        self.log_dock.set_data(data)

    def set_new_handler(self, handler: callable):
        self.new_handler = handler

    def set_open_handler(self, handler):
        self.open_handler = handler

    def set_save_handler(self, handler):
        self.save_handler = handler

    def set_save_as_handler(self, handler):
        self.save_as_handler = handler

    def set_close_handler(self, handler):
        self.close_handler = handler

    def set_add_dimension_handler(self, handler):
        self.dimension_dock.set_add_handler(handler)

    def set_text(self, text):
        self.text_edit.setText(text)

    @Slot()
    def on_new(self):
        try:
            self.new_handler()
        except TypeError:
            pass

    @Slot()
    def on_open(self):
        try:
            self.open_handler()
        except TypeError:
            pass

    @Slot()
    def on_save(self):
        try:
            self.save_handler()
        except TypeError:
            pass

    @Slot()
    def on_save_as(self):
        try:
            self.save_as_handler()
        except TypeError:
            pass

    @Slot()
    def on_close(self):
        try:
            self.close_handler()
        except TypeError:
            pass

    def set_choices(self, choices):
        self.dimension_dock.table_widget.setRowCount(len(choices))
        for i in range(len(choices)):
            label = QTableWidgetItem()
            label.setText(choices[i].name())
            self.dimension_dock.table_widget.setItem(i, 0, label)
            combobox = QComboBox()
            combobox.addItems(['No Selection']+list(map(lambda x: str(x+1), range(choices[i].alternative_count()))))
            self.dimension_dock.table_widget.setCellWidget(i, 1, combobox)


class SimplifyWindow(QDialog):
    def __init__(self, parent, choices):
        QDialog.__init__(self, parent)
        self.setFixedSize(400, 400)
        self.setWindowTitle("Generate Simplified Source")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        table_view = QTableWidget(self)
        table_view.setSelectionMode(QAbstractItemView.NoSelection)
        table_view.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        table_view.horizontalHeader().setVisible(False)
        table_view.verticalHeader().setVisible(False)
        table_view.verticalHeader().setResizeMode(QHeaderView.Fixed)
        table_view.verticalHeader().setDefaultSectionSize(20)
        table_view.setColumnCount(2)
        table_view.setRowCount(len(choices))
        row = 0
        for choice in choices:
            table_view.setItem(row, 0, QTableWidgetItem(choice.name()))
            combobox = QComboBox()
            combobox.addItems(['No Selection']+list(map(lambda x: str(x+1), range(choice.alternative_count()))))
            table_view.setCellWidget(row, 1, combobox)
            row += 1

        layout.addWidget(table_view)

        button_box = QWidget(self)
        #button_box.setFixedHeight(50)
        button_box_layout = QHBoxLayout()
        self.simplify_button = QPushButton('Simplify')
        self.abort_button = QPushButton('Abort')
        button_box_layout.addWidget(self.simplify_button)
        button_box_layout.addWidget(self.abort_button)
        button_box.setLayout(button_box_layout)

        layout.addWidget(button_box)

        self.setLayout(layout)


class LogDock(QDockWidget):
    def __init__(self, parent_window):
        QDockWidget.__init__(self, parent_window)
        self.setWindowTitle('Log')
        #self.setAllowedAreas(Qt.DockWidgetAreas(Qt.BottomDockWidgetArea))

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.setWidget(self.text_edit)

    def print(self, data):
        self.text_edit.append(data)


class DimensionDock(QDockWidget):
    def __init__(self, parent_window):
        QDockWidget.__init__(self, "Choices", parent_window)
        self.parent_window = parent_window
        self.central_widget = QWidget(self)
        self.setWidget(self.central_widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.tree_view = QTreeWidget()
        self.tree_view.setHeaderLabel('Dimensions')
        #self.tree_view.setExpandsOnDoubleClick(False)
        # self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)
        # self.table_widget.setColumnCount(2)
        # self.table_widget.verticalHeader().setVisible(False)
        # self.table_widget.verticalHeader().setResizeMode(QHeaderView.Fixed)
        # self.table_widget.verticalHeader().setDefaultSectionSize(20)
        layout.addWidget(self.tree_view)

        self.add_button = QPushButton("Add dimension")
        layout.addWidget(self.add_button)
        self.central_widget.setLayout(layout)

        self.dialog = None


class TopLevelTreeItem(QTreeWidgetItem):
    def __init__(self, data):
        QTreeWidgetItem.__init__(self, data)


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
        self.ok_button.setDefault(True)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        bottom_line_layout = QHBoxLayout()
        bottom_line_layout.addWidget(self.ok_button)
        bottom_line_layout.addWidget(self.cancel_button)

        layout.addRow(bottom_line_layout)

        self.setLayout(layout)

    def get_dimension_name(self):
        return self.dimension_name.text()

    def get_choices(self):
        return self.choices.toPlainText().split("\n")