from PySide import QtCore
from models.version import Version, Output

GROUP_HEADER = QtCore.Qt.UserRole + 1

class GroupedListView(QtCore.QAbstractItemModel):
    """docstring for GroupedListView"""
    def __init__(self, root=None, parent=None):
        super(GroupedListView, self).__init__(parent)
        if not root:
            self.rootNode = Version()
        else:
            self.rootNode = root

    # Overriden public methods
    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole and index.column() == 0:
                return node.get_display_name()
        if index.column() == 0:
            if role == GROUP_HEADER and node.get_type_info() == 'version':
                return 'header'


    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Name"

    def columnCount(self, parent):
        return 1

    def rowCount(self, parent):
        if not parent.isValid():
            parent_node = self.rootNode
        else:
            parent_node = parent.internalPointer()

        return parent_node.childCount()

    def parent(self, index):
        node = self._get_node(index)
        parent_node = node.parent()

        if parent_node == self.rootNode:
            return QtCore.QModelIndex()
        return self.createIndex(parent_node.row(), 0, parent_node)

    def index(self, row, column, parent=QtCore.QModelIndex()):
        parent_node = self._get_node(parent)
        try:
            child_item = parent_node.child(row)
            if child_item:
                return self.createIndex(row, column, child_item)
            else:
                return QtCore.QModelIndex()
        except Exception as e:
            print e
            print 'index(%s, %s, %s)' % (row, column, parent)
            print parent_node, parent_node.children





    # Private class methods
    def insertRows(self, position, rows, child, parent=QtCore.QModelIndex()):
        parent_node = self._get_node(parent)

        self.beginInsertRows(parent, position, position + rows - 1)
        parent_node.insertChild(position, child)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        parent_node = self._get_node(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        for row in range(rows):
            success = parent_node.removeChild(position)

        self.endRemoveRows()
        return success

    def addOuput(self, versionJSON, outputJSON):
        is_found = False
        count = self.rootNode.childCount()

        for i in range(count):
            child = self.rootNode.child(i)
            if child.version['id'] == versionJSON['id']:
                child_index = self._find_node(versionJSON['version'])
                new_output = Output(output=outputJSON)
                self.insertRows(child.childCount(), 1, new_output, child_index)
                is_found = True
                break

        if not is_found:
            new_node = Version(version=versionJSON)
            new_output = Output(output=outputJSON, parent=new_node)

            self.insertRows(count, 1, new_node)
            return True

        return False

    def removeOuput(self, versionJSON, outputJSON):
        child_index = self._find_node(versionJSON['version'])
        node = child_index.internalPointer()
        # print 'before', node.children
        indices = [i for i, child in enumerate(node.children) if child.get_display_name() == outputJSON['type']]
        row = indices[0]
        self.removeRows(row, 1, child_index)

        # print 'after', node.children
        if not node.children:
            self.removeRows(child_index.row(), 1)

    # Private methods
    def _find_node(self, name):
        """
        Find a node in the model by it's name
        """
        startindex = self.index(0, 0)
        items = self.match(startindex, QtCore.Qt.DisplayRole, name, 1, QtCore.Qt.MatchExactly | QtCore.Qt.MatchWrap)
        try:
            return items[0]
        except IndexError:
            return QtCore.QModelIndex()

    def _get_node(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self.rootNode
