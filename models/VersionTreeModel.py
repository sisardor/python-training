from PySide import QtCore, QtGui
from PySide.QtGui import QStyledItemDelegate


class VersionDelegate(QtGui.QStyledItemDelegate):
    """docstring for VersionDelegate"""
    def __init__(self, parent=None):
        super(VersionDelegate, self).__init__(parent)


    # def paint(self, painter, option, index):
    #     print 'paint'
    #     QStyledItemDelegate.paint(self, painter, option, index)
    #     pass


class VersionTreeModel(QtCore.QAbstractItemModel):
    """docstring for VersionTreeModel"""
    def __init__(self, root=None, parent=None):
        super(VersionTreeModel, self).__init__(parent)
        self.rootNode = root


    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self.rootNode
        else:
            parentNode = parent.internalPointer()
        return parentNode.childCount()

    def columnCount(self, parent):
        return 3

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self.rootNode

    def parent(self, index):
        node = self.getNode(index)
        parentNode = node._parent()

        if parentNode == self.rootNode:
            return QtCore.QModelIndex()
        return self.createIndex(parentNode.row(), 0, parentNode)

    def index(self, row, column, parent):
        parentNode = self.getNode(parent)

        childItem = parentNode.child(row)

        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()


    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Name"
            elif section == 1:
                return "Published by"
            elif section == 2:
                return "Modified"

    def data(self, index, role):

        if not index.isValid():
            print 'error'
            return None
        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return node.version.version
            elif index.column() == 1:
                return node.version.createdBy
            elif index.column() == 2:
                return node.version.createdAt
        pass


if __name__ == '__main__':
    pass