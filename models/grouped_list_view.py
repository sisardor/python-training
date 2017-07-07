from PySide import QtCore
from models.Version import Version, Output


class GroupedListView(QtCore.QAbstractItemModel):
    """docstring for GroupedListView"""
    def __init__(self, root=None, parent=None):
        super(GroupedListView, self).__init__(parent)
        if not root:
            self.rootNode = Version()
        else:
            self.rootNode = root

    def columnCount(self, parent):
        return 1

    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self.rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    def parent(self, index):
        node = self.getNode(index)
        parentNode = node.parent()

        if parentNode == self.rootNode:
            return QtCore.QModelIndex()
        return self.createIndex(parentNode.row(), 0, parentNode)

    def index(self, row, column, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)
        # print 'index(%s, %s, %s)'%(row, column, parent)

        try:
            childItem = parentNode.child(row)
        except Exception as e:
            print e
            print 'index(%s, %s, %s)' % (row, column, parent)
            print parentNode, parentNode.children


        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()

        typeInfo = node.getType()
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                if typeInfo == 'version':
                    return node.version['version']
                else:
                    return node.version['type']

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self.rootNode

    def insertRows(self, position, rows, child, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)

        self.beginInsertRows(parent, position, position + rows - 1)
        parentNode.insertChild(position, child)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        for row in range(rows):
            success = parentNode.removeChild(position)

        self.endRemoveRows()
        return success

    def findlayer(self, name):
        """
        Find a layer in the model by it's name
        """
        startindex = self.index(0, 0)
        items = self.match(startindex, QtCore.Qt.DisplayRole, name, 1, QtCore.Qt.MatchExactly | QtCore.Qt.MatchWrap)
        try:
            return items[0]
        except IndexError:
            return QtCore.QModelIndex()

    def addOuput(self, versionJSON, outputJSON):
        is_found = False
        count = self.rootNode.childCount()

        for i in range(count):
            child = self.rootNode.child(i)
            if child.version['id'] == versionJSON['id']:
                child_index = self.findlayer(versionJSON['version'])
                newOutput = Output(output=outputJSON)
                self.insertRows(child.childCount(), 1, newOutput, child_index)
                is_found = True
                break

        if not is_found:
            newNode = Version(version=versionJSON)
            newOutput = Output(output=outputJSON, parent=newNode)

            self.insertRows(count, 1, newNode)
            return True

        return False

    def removeOuput(self, versionJSON, outputJSON):
        child_index = self.findlayer(versionJSON['version'])
        node = child_index.internalPointer()
        # print 'before', node.children
        indices = [i for i, child in enumerate(node.children) if child.get_display_name() == outputJSON['type']]
        row = indices[0]
        self.removeRows(row, 1, child_index)

        # print 'after', node.children
        if not node.children:
            self.removeRows(child_index.row(), 1)


    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Name"
