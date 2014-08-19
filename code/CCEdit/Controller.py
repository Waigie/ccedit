__author__ = 'Christoph Weygand <christophweygand@gmail.com>'

import CCLang
from PySide.QtCore import QObject, Slot, Qt
from PySide.QtGui import QFileDialog, QApplication, QMessageBox
from CCEdit.Models import ApplicationState, TabState
import CCLang.Parser
import CCLang.Lens
import collections
import ntpath, json


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
        self.view.add_dimension.connect(self.add_dimension_handler)
        self.view.delete_alternative.connect(self.delete_alternative_handler)
        self.view.delete_dimension.connect(self.delete_dimension_handler)
        self.view.add_alternative.connect(self.add_alternative_handler)

        self.view.dimension_dock.dimension_tree.itemChanged.connect(self.tree_item_changed)
        self.view.dimensions_reorder.connect(self.dimensions_reorder)


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

            self.load_configuration(ntpath.dirname(filename[0]))

            self.view.get_current_text_widget().textChanged.connect(self.text_change_handler)
            self.view.get_current_text_widget().setText(tab_state.source)
            self.view.render_dimensiondock(self.state.dimensions, self.state.config)

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
        if dimension_name in self.state.config:
            self.state.config.pop(dimension_name)
        self.view.render_dimensiondock(self.state.dimensions, self.state.config)

    @Slot()
    def add_alternative_handler(self, dimension_name):
        self.state.dimensions[dimension_name].append('Alternative'+str(len(self.state.dimensions[dimension_name])+1))
        self.view.render_dimensiondock(self.state.dimensions, self.state.config)

    @Slot()
    def tree_item_changed(self):
        new_config = {}
        new_dimensions = collections.OrderedDict()
        for i in range(self.view.dimension_dock.dimension_tree.topLevelItemCount()-1):
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

    @Slot()
    def dimensions_reorder(self, order):
        new_dimensions = collections.OrderedDict()
        print(self.state.dimensions)
        for dimension in order:
            new_dimensions[dimension] = self.state.dimensions[dimension]
        self.state.dimensions = new_dimensions

    def update_view(self, old_config):
        parser = CCLang.Parser.LEPLParser("#")
        if self.state.get_active_changed():
            src_ast = CCLang.Lens.update(old_config, parser.parse(self.state.get_active_source()), parser.parse(self.state.get_active_view()), order=list(self.state.dimensions.keys()))
            self.state.set_active_source(src_ast.apply_and_print({}, '#'))
        else:
            src_ast = parser.parse(self.state.get_active_source())

        self.state.set_active_view(src_ast.apply_and_print(self.state.config, '#'), changed=False)
        self.view.set_display_text(self.state.get_active_view())

    def load_configuration(self, dirname):
        config_file = dirname + ntpath.sep + ".ccedit"

        if ntpath.isfile(config_file):
            file = open(config_file, mode="r")
            config = file.read()
            config_parsed = json.loads(config)
            self.state.dimensions = collections.OrderedDict(sorted(config_parsed.items()))
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Configuration?")
            msgBox.setText("No configuration file found")
            msgBox.setInformativeText("Would you like to generate a dimension configuration from the opened file?")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            ret = msgBox.exec()
            if ret == QMessageBox.Yes:
                parser = CCLang.Parser.LEPLParser("#")
                source = self.state.get_active_source()
                source_ast = parser.parse(source)
                dimensions = source_ast.dims()
                dimensions_dict = collections.OrderedDict()
                for dimension in dimensions:
                    dimensions_dict[dimension.name()] = list(map(lambda n: "Alternative "+str(n), range(1, dimension.alternative_count()+1)))
                self.state.dimensions = dimensions_dict

