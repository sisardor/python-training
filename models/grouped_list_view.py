from PySide import QtCore


class GroupedListView(QtCore.QAbstractItemModel):
    """docstring for GroupedListView"""
    def __init__(self,root=None, parent=None):
        super(GroupedListView, self).__init__(parent)
        self.rootNode = root
        print root


    def columnCount(self, parent):
        return 1

    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self.rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    def _parent(self):
        return self.parent

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

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return 'foo'

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self.rootNode

    def insertRows(self, position, item, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)

        self.beginInsertRows(parent, position, position + 1)
        parentNode.insertChild(position, item)
        self.endInsertRows()
        return True