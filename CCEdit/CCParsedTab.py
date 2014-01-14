__author__ = 'Christoph Weygand'

import re
from PySide.QtGui import QWidget, QHBoxLayout, QTableWidget, QTextEdit, QSizePolicy, QHeaderView, QAbstractItemView, \
    QLabel, QComboBox
from PySide.QtCore import *


class CCParsedTab(QWidget):
    def __init__(self, parser_result):
        QWidget.__init__(self)
        self._parser_result = parser_result

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSizeConstraint(QHBoxLayout.SetMinimumSize)

        self.table_widget = QTableWidget()
        self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)
        self.table_widget.setRowCount(2)
        self.table_widget.setColumnCount(2)
        self.table_widget.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.table_widget.setHorizontalHeaderLabels(["Dimension", "Choice"])
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.verticalHeader().setResizeMode(QHeaderView.Fixed)
        self.table_widget.verticalHeader().setDefaultSectionSize(20)
        sp_table = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sp_table.setHorizontalStretch(1)
        self.table_widget.setSizePolicy(sp_table)

        layout.addWidget(self.table_widget)

        self.text_widget = QTextEdit()
        sp_text = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sp_text.setHorizontalStretch(4)
        self.text_widget.setReadOnly(True)
        self.text_widget.setSizePolicy(sp_text)
        self.text_widget.setStyleSheet('font: 9pt "Courier";')
        self.text_widget.setText(self._parser_result.get_text())

        layout.addWidget(self.text_widget)

        self.setLayout(layout)

        self._fill_table()

    def _fill_table(self):
        colors = ['yellow', 'orange', 'green', 'red']

        dimensions = self._parser_result.get_dimensions()
        row = 0
        for dimension in dimensions:
            dimension_name = QLabel(dimension[0])
            dimension_name.setStyleSheet('background: %s' % colors[row % len(colors)])
            self.table_widget.setCellWidget(row, 0, dimension_name)
            choices_widget = QComboBox()
            choices = dimension[1]
            choices.insert(0, "No choice")
            choices_widget.addItems(choices)
            choices_widget.setStyleSheet('background: white')
            choices_widget.setStyleSheet('border: none')
            choices_widget.currentIndexChanged.connect(self.on_choice_change)
            self.table_widget.setCellWidget(row, 1, choices_widget)
            row += 1

    @Slot()
    def on_choice_change(self):
        text = self._parser_result.get_text()
        for row in range(self.table_widget.rowCount()):
            label = self.table_widget.cellWidget(row, 0)
            choices = self.table_widget.cellWidget(row, 1)
            if choices.currentIndex() == 0:
                continue
            regex = self._build_regex(label.text(), choices.count()-1)
            pattern = re.compile(regex)
            matches = pattern.search(text)
            for match in matches.groups():
                results = re.search("<(.+)>", match)
                variants = [s.strip() for s in results.groups()[0].split(",")]
                text = text.replace(match, variants[choices.currentIndex()-1])
        self.text_widget.setText(text)

    @staticmethod
    def _build_regex(dim, count):
        regex = "("+dim+"<"
        for i in range(count):
            regex += ".+,[ ]?"
        regex = regex[:-5]
        regex += ">)"
        return regex


