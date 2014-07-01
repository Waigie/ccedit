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

        self.menuBar().addMenu(file_menu)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)

        self.dimension_dock = DimensionDock(self)
        self.addDockWidget(Qt.DockWidgetArea(Qt.LeftDockWidgetArea), self.dimension_dock)

        layout.addWidget(self.tabs)
        self.central_widget.setLayout(layout)

    def get_current_text_widget(self):
        return self.tabs.currentWidget()

    def add_text_tab(self, name):
        text_edit = QTextEdit()
        text_edit.setStyleSheet("font: 10pt \"Courier New\";")
        text_edit.setWordWrapMode(QTextOption.NoWrap)
        CCHighlighter(text_edit, '#')

        tab_index = self.tabs.addTab(text_edit, name)
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


class DimensionDock(QDockWidget):
    def __init__(self, parent_window):
        QDockWidget.__init__(self, "Dimensions", parent_window)
        self.parent_window = parent_window

        self.central_widget = QWidget(self)
        self.setWidget(self.central_widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # self.table_widget = QTableWidget()
        # self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)
        # self.table_widget.setColumnCount(4)
        # self.table_widget.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        # self.table_widget.horizontalHeader().setVisible(False)
        # self.table_widget.verticalHeader().setVisible(False)
        # self.table_widget.verticalHeader().setResizeMode(QHeaderView.Fixed)
        # self.table_widget.verticalHeader().setDefaultSectionSize(20)
        # layout.addWidget(self.table_widget)

        self.dimension_tree = QTreeWidget()
        self.dimension_tree.setExpandsOnDoubleClick(False)
        self.dimension_tree.setColumnCount(3)
        self.dimension_tree.setColumnWidth(1, 24)
        self.dimension_tree.setColumnWidth(2, 24)
        dimension = QTreeWidgetItem(self.dimension_tree, 0)
        dimension.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)
        for i in range(3):
            alternative = QTreeWidgetItem(str(i))
            alternative.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
            alternative.setCheckState(0, Qt.Checked)
            dimension.addChild(alternative)
        #self.dimension_tree.addTopLevelItem(dimension)
        dimension.setText(0,"A")
        editbutton = QToolButton(self.dimension_tree)
        editbutton.setIcon(QIcon.fromTheme('edit'))
        editbutton.setFixedWidth(24)
        delbutton = QToolButton(self.dimension_tree)
        delbutton.setIcon(QIcon.fromTheme('delete'))
        delbutton.setFixedWidth(24)
        self.dimension_tree.setItemWidget(dimension, 1, editbutton)
        self.dimension_tree.setItemWidget(dimension, 2, delbutton)
        dimension.setExpanded(True)

        layout.addWidget(self.dimension_tree)

        self.central_widget.setLayout(layout)