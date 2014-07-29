__author__ = 'Waigie'

from PySide.QtCore import *
from PySide.QtGui import *
from CCEdit.Services import CCHighlighter


class MainWindow(QMainWindow):
    delete_alternative = Signal(str, int)
    delete_dimension = Signal(str)
    add_alternative = Signal(str)
    add_dimension = Signal()
    config_changed = Signal()

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
        self.delete_icon = QIcon("../../resources/icons/remove.png")
        self.add_icon = QIcon("../../resources/icons/add.png")

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
        self.dimension_tree.itemClicked.connect(self.item_clicked)
        AddDimensionTreeItem(self.dimension_tree, 0, self.add_icon)

        layout.addWidget(self.dimension_tree)

        self.central_widget.setLayout(layout)

    def redraw_tree(self, dimensions, config):
        self.dimension_tree.blockSignals(True)

        for dimension in dimensions.keys():
            dimension_item = self.dimension_tree.findItems(dimension, Qt.MatchExactly)
            if not dimension_item:
                dimension_item = DimensionTreeItem(None, 0, dimension, self.delete_icon)
                dimension_item.setText(0, dimension)
                self.dimension_tree.insertTopLevelItem(self.dimension_tree.topLevelItemCount()-1, dimension_item)

                add_alternative = AddAlternativeTreeItem(None, 0, self.add_icon)
                add_alternative.dimension = dimension
                dimension_item.addChild(add_alternative)

            else:
                dimension_item = dimension_item[0]

            dimension_item.setExpanded(True)

            if dimension in config:
                self.update_alternatives(dimension_item, dimensions[dimension], config[dimension])
            else:
                self.update_alternatives(dimension_item, dimensions[dimension], [])

        for i in reversed(range(self.dimension_tree.topLevelItemCount())):
            item = self.dimension_tree.topLevelItem(i)
            if isinstance(item, AddDimensionTreeItem):
                continue

            if not item.text(0) in dimensions:
                self.dimension_tree.takeTopLevelItem(i)

        self.dimension_tree.blockSignals(False)

    def update_alternatives(self, item, alternatives, config):
        print(config)
        counter = 0
        for i in range(min(item.childCount(), len(alternatives))):
            if isinstance(item.child(i), AddAlternativeTreeItem):
                continue
            item.child(i).setText(0, alternatives[i])
            item.child(i).dimension = item.text(0)
            item.child(i).alternative_num = i
            if i in config or not config:
                item.child(i).setCheckState(0, Qt.Checked)
            else:
                item.child(i).setCheckState(0, Qt.Unchecked)

            counter += 1

        if item.childCount() > len(alternatives):
            for i in reversed(range(len(alternatives), item.childCount())):
                if isinstance(item.child(i), AddAlternativeTreeItem):
                    continue
                item.takeChild(i)
        else:
            for i in range(counter, len(alternatives)):
                child = AlternativeTreeItem(None, 0, alternatives[i], Qt.Checked, self.delete_icon)
                child.dimension = item.text(0)
                child.alternative_num = i
                if i in config or not config:
                    child.setCheckState(0, Qt.Checked)
                else:
                    child.setCheckState(0, Qt.Unchecked)

                item.insertChild(item.childCount()-1, child)


        # for alternative in alternatives:
        #     if item.child(counter) and isinstance(item.child(counter), AddAlternativeTreeItem):
        #         item.child(counter).setText(0, alternative)
        #         item.child(counter).dimension = item.text(0)
        #         item.child(counter).alternative_num = counter
        #     else:
        #         child = AlternativeTreeItem(None, 0, alternative, Qt.Checked, self.delete_icon)
        #         child.dimension = item.text(0)
        #         child.alternative_num = counter
        #         item.insertChild(item.childCount()-1, child)
        #
        #     counter += 1
        #
        # if counter < item.childCount():
        #     for i in range(counter, item.childCount()):
        #         child = item.child(i)
        #         if isinstance(child, AddAlternativeTreeItem):
        #             continue
        #
        #         item.takeChild(i)

        # self.dimension_tree.clear()
        #
        # for dimension_name in dimensions.keys():
        #
        #     dimension = DimensionTreeItem(self.dimension_tree, 0, dimension_name, self.delete_icon)
        #     dimension.setText(0, dimension_name)
        #
        #     alternative_num = 0
        #     for alternative_name in dimensions[dimension_name]:
        #         if dimension_name in config and alternative_num in config[dimension_name]:
        #             alternative = AlternativeTreeItem(dimension, 0, alternative_name, Qt.Checked, self.delete_icon)
        #         elif dimension_name in config:
        #             alternative = AlternativeTreeItem(dimension, 0, alternative_name, Qt.Unchecked, self.delete_icon)
        #         else:
        #             alternative = AlternativeTreeItem(dimension, 0, alternative_name, Qt.Checked, self.delete_icon)
        #
        #         alternative.dimension = dimension_name
        #         alternative.alternative_num = alternative_num
        #
        #         alternative_num += 1
        #
        #     add_alternative = AddAlternativeTreeItem(dimension, 0, self.add_icon)
        #     add_alternative.dimension = dimension_name
        #
        #     dimension.setExpanded(True)
        #
        # AddDimensionTreeItem(self.dimension_tree, 0, self.add_icon)
        # #self.dimension_tree.itemChanged.emit(None, 0)

        # return None

    @Slot()
    def item_clicked(self, item, col):
        if isinstance(item, AddAlternativeTreeItem) and col == 0:
            self.parent_window.add_alternative.emit(item.dimension)
        elif isinstance(item, AlternativeTreeItem) and col == 2:
            self.parent_window.delete_alternative.emit(item.dimension, item.alternative_num)
        elif isinstance(item, DimensionTreeItem) and col == 2:
            self.parent_window.delete_dimension.emit(item.dimension)
        elif isinstance(item, AddDimensionTreeItem) and col == 0:
            self.parent_window.add_dimension.emit()


class AlternativeTreeItem(QTreeWidgetItem):
    def __init__(self, parent, col, name, checkstate, icon):
        QTreeWidgetItem.__init__(self, parent, col)
        self.setText(0, name)
        self.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
        self.setCheckState(0, checkstate)
        self.dimension = ''
        self.setIcon(2, icon)
        self.alternative_num = ''


class AddAlternativeTreeItem(QTreeWidgetItem):
    def __init__(self, parent, col, icon):
        QTreeWidgetItem.__init__(self, parent, col)
        self.setIcon(0, icon)
        self.dimension = ''


class DimensionTreeItem(QTreeWidgetItem):
    def __init__(self, parent, col, name, icon):
        QTreeWidgetItem.__init__(self, parent, col)
        self.setText(0, name)
        self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)
        self.dimension = name
        self.setIcon(2, icon)


class AddDimensionTreeItem(QTreeWidgetItem):
    def __init__(self, parent, col, icon):
        QTreeWidgetItem.__init__(self, parent, col)
        self.setIcon(0, icon)
        self.dimension = ''