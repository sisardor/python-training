from PySide import QtGui, QtCore

class OutputsTreeUI(QtGui.QTreeView):
    def __init__(self, model=None, parent=None):
        QtGui.QTreeView.__init__(self, parent)

        self.header().setStretchLastSection(True)
        self.setMinimumSize(QtCore.QSize(200, 0))
        self.setAnimated(True)
        self.setItemsExpandable(False)

        self.setModel(model)

        QtCore.QObject.connect(model,
                               QtCore.SIGNAL("rowsInserted(QModelIndex, int, int)"),
                               self.row_inserted)

    def row_inserted(self, parent, start, end):
        self.expandAll()



