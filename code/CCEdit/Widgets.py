__author__ = 'Waigie'

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
        self.hide_dimensions()

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

    def show_dimensions(self):
        self.dimension_dock.setVisible(True)

    def hide_dimensions(self):
        self.dimension_dock.setVisible(False)

    def render_dimensiondock(self, dimensions, config):
        self.dimension_dock.redraw_tree(dimensions, config)


class DimensionDock(QDockWidget):
    def __init__(self, parent_window):
        QDockWidget.__init__(self, "Dimensions", parent_window)
        self.parent_window = parent_window

        self.central_widget = QWidget(self)
        self.setWidget(self.central_widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.dimension_tree = QTreeWidget()
        self.dimension_tree.setExpandsOnDoubleClick(False)
        self.dimension_tree.setColumnCount(3)
        self.dimension_tree.setColumnWidth(1, 24)
        self.dimension_tree.setColumnWidth(2, 24)
        self.dimension_tree.header().hide()
        self.dimension_tree.header().setResizeMode(0, QHeaderView.Stretch)
        self.dimension_tree.header().setStretchLastSection(False)

        layout.addWidget(self.dimension_tree)

        buttonBar = QVBoxLayout()

        self.addButton = QToolButton(self)
        self.addButton.setIcon(QIcon("../../resources/icons/add.png"))
        self.addButton.setToolTip("Add Dimension")
        self.addButton.setStyleSheet("background: transparent")
        buttonBar.addWidget(self.addButton)

        # layout.addChildLayout(buttonBar)
        layout.addLayout(buttonBar)

        self.central_widget.setLayout(layout)

    def redraw_tree(self, dimensions, config):
        self.dimension_tree.clear()
        self.dimension_tree.setColumnCount(3)
        self.dimension_tree.setColumnWidth(1, 24)
        self.dimension_tree.setColumnWidth(2, 24)
        self.dimension_tree.header().hide()
        self.dimension_tree.header().setResizeMode(0, QHeaderView.Stretch)
        self.dimension_tree.header().setStretchLastSection(False)

        for dimension_name in dimensions.keys():
            dimension = QTreeWidgetItem(self.dimension_tree, 0)
            dimension.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)
            dimension.setText(0, dimension_name)

            for alternative_name in dimensions[dimension_name]:
                alternative = QTreeWidgetItem(dimension, 0)
                alternative.setText(0, alternative_name)
                alternative.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                alternative.setCheckState(0, Qt.Checked)

                button = QToolButton(self.dimension_tree)
                button.setIcon(QIcon("../../resources/icons/remove.png"))
                button.setStyleSheet("background: transparent")
                button.setToolTip("Remove alternative")
                button.setFixedWidth(16)
                button.setFixedHeight(16)

                self.dimension_tree.setItemWidget(alternative, 2, button)

            add_button = QToolButton(self.dimension_tree)
            add_button.setIcon(QIcon("../../resources/icons/add.png"))
            add_button.setStyleSheet("background: transparent")
            add_button.setToolTip("Add alternative")
            add_button.setFixedWidth(16)
            add_button.setFixedHeight(16)

            add_alternative = QTreeWidgetItem(dimension, 0)
            self.dimension_tree.setItemWidget(add_alternative, 0, add_button)

            del_button = QToolButton(self.dimension_tree)
            del_button.setIcon(QIcon("../../resources/icons/remove.png"))
            del_button.setStyleSheet("background: transparent")
            del_button.setToolTip("Remove dimension")
            del_button.setFixedWidth(16)
            del_button.setFixedHeight(16)

            self.dimension_tree.setItemWidget(dimension, 2, del_button)
            dimension.setExpanded(True)



