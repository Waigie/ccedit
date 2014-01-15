from PySide.QtCore import Qt
from PySide.QtGui import *

__author__ = 'Christoph'


class CCDimensionDock(QDockWidget):
    def __init__(self, parent):
        QDockWidget.__init__(self, "Dimension", parent)

        self.setAllowedAreas(Qt.DockWidgetAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea))

        self.central_widget = QWidget(self)
        self.setWidget(self.central_widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.dimension_list = QListWidget(self.central_widget)
        self.dimension_list.setMinimumWidth(150)
        self.dimension_list.addItems(["Foo", "Bar", "Baz"])

        layout.addWidget(self.dimension_list)

        self.central_widget.setLayout(layout)
