__author__ = 'Waigie'

import json
import datetime
from PySide.QtCore import *
from CCLang.Parser import LEPLParser


class File(QObject):

    def __init__(self, log, filename=None):
        super(File, self).__init__()
        self.code = ''
        self.changed = False
        self.filename = filename
        self.log = log
        if self.filename:
            self.load_from_file(self.filename)

    def load_from_file(self, filename):
        file = open(filename, 'r')
        self.changed = False
        self.code = file.read()

    def generate_output(self):
        return self.code


class TreeItem(object):
    def __init__(self, data, parent=None):
        self.parent_item = parent
        self.item_data = data
        self.child_items = []

    def append_child(self, item):
        self.child_items.append(item)

    def child(self, row):
        return self.child_items[row]

    def child_count(self):
        return len(self.child_items)

    def column_count(self):
        return len(self.item_data)

    def data(self, column):
        try:
            return self.item_data[column]
        except IndexError:
            return None

    def parent(self):
        return self.parent_item

    def row(self):
        if self.parent_item:
            return self.parent_item.child_items.index(self)
        return 0


class DimensionTree(QAbstractItemModel):
    def __init__(self, parent=None):
        super(DimensionTree, self).__init__(parent)

        self.root_item = TreeItem(("Dimension", "Color"))
        #self.setupModelData(data.split('\n'), self.root_item)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().column_count()
        else:
            return self.root_item.column_count()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.root_item.data(section)

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        child_item = index.internalPointer()
        parent_item = child_item.parent()

        if parent_item == self.root_item:
            return QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()

        return parent_item.child_count()

    def append(self, item):
        self.root_item.append_child(item)


