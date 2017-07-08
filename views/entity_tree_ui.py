from PySide import QtGui, QtCore

from models.combobox_delegate import ComboboxDelegate


class EntityTreeUI(QtGui.QTreeView):
    """docstring for EntityTreeUI"""
    def __init__(self, model, parent=None):
        QtGui.QTreeView.__init__(self, parent)
        self.header().setStretchLastSection(True)
        self.setItemDelegateForColumn(2, ComboboxDelegate(self))
        self.setAnimated(True)
        self.setMinimumSize(QtCore.QSize(302, 0))
        self.setMaximumSize(QtCore.QSize(302, 1500))

        self.setModel(model)
        self.setStyleSheet("""
            QTreeView QHeaderView::section,
            QTreeView {

                font-size:12px
            }
        """)

    def resizeEvent(self, event):
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 100)
        pass
