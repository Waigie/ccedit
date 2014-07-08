import CCLang

__author__ = 'Christoph Weygand'

from PySide.QtCore import QObject, Slot, Qt
from PySide.QtGui import QFileDialog, QApplication
from CCEdit.Models import ApplicationState, TabState
import CCLang.Parser
import CCLang.Lens
import collections


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
        self.view.dimension_dock.addButton.clicked.connect(self.add_dimension_handler)
        self.view.delete_alternative.connect(self.delete_alternative_handler)
        self.view.delete_dimension.connect(self.delete_dimension_handler)
        self.view.add_alternative.connect(self.add_alternative_handler)

        self.view.dimension_dock.dimension_tree.itemChanged.connect(self.tree_item_changed)


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
            self.view.get_current_text_widget().textChanged.connect(self.text_change_handler)
            self.view.get_current_text_widget().setText(tab_state.source)

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
        if tab_index > -1:
            self.view.show_dimensions()
        else:
            self.view.hide_dimensions()

    @Slot()
    def text_change_handler(self):
        self.state.set_active_view(self.view.get_display_text())
        self.view.set_display_title(self.state.active_title())

    @Slot()
    def add_dimension_handler(self):
        dimension_name = "NewDimension"
        count = 1
        while dimension_name in self.state.dimensions:
            count += 1
            dimension_name = "NewDimension"+str(count)

        self.state.dimensions[dimension_name] = ["Alternative1", "Alternative2"]

        self.view.render_dimensiondock(self.state.dimensions, self.state.config)

    @Slot()
    def delete_alternative_handler(self, dimension_name, alternative_num):
        self.state.dimensions[dimension_name].pop(alternative_num)
        self.view.render_dimensiondock(self.state.dimensions, self.state.config)

    @Slot()
    def delete_dimension_handler(self, dimension_name):
        self.state.dimensions.pop(dimension_name)
        self.view.render_dimensiondock(self.state.dimensions, self.state.config)

    @Slot()
    def add_alternative_handler(self, dimension_name):
        self.state.dimensions[dimension_name].append('Alternative'+str(len(self.state.dimensions[dimension_name])))
        self.view.render_dimensiondock(self.state.dimensions, self.state.config)

    @Slot()
    def tree_item_changed(self):
        new_config = {}
        new_dimensions = collections.OrderedDict()
        for i in range(self.view.dimension_dock.dimension_tree.topLevelItemCount()):
            dimension = self.view.dimension_dock.dimension_tree.topLevelItem(i)
            all_checked = True
            checked = []
            alternatives = []
            for j in range(dimension.childCount()-1):
                alternatives.append(dimension.child(j).text(0))
                if dimension.child(j).checkState(0) == Qt.CheckState.Checked:
                    checked.append(j)
                else:
                    all_checked = False

            new_dimensions[dimension.text(0)] = alternatives
            if not all_checked:
                new_config[dimension.text(0)] = checked

        self.state.dimensions = new_dimensions
        old_config = self.state.config
        self.state.config = new_config

        self.view.render_dimensiondock(self.state.dimensions, self.state.config)

        self.update_view(old_config)

    def update_view(self, old_config):
        parser = CCLang.Parser.LEPLParser("#")
        print(self.state.get_active_source(),self.state.get_active_view())
        new_src_ast = CCLang.Lens.update(old_config, parser.parse(self.state.get_active_source()), parser.parse(self.state.get_active_view()))
        self.state.set_active_source(new_src_ast.apply_and_print({}, '#'))
        self.state.set_active_view(new_src_ast.apply_and_print(self.state.config, '#'))
        self.view.set_display_text(self.state.get_active_view())

