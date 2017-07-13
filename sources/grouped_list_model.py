from PySide import QtCore

from sources.constants import GROUP_HEADER
from sources.version import Version, Output


class GroupedListView(QtCore.QAbstractItemModel):
    """docstring for GroupedListView"""
    removeItem = QtCore.Signal(str)
    def __init__(self, root=None, parent=None):
        super(GroupedListView, self).__init__(parent)
        self._record = []
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
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parent_node = self.rootNode
        else:
            parent_node = parent.internalPointer()
        return parent_node.childCount()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        node = self._get_node(index)
        parent_node = node.parent()

        if parent_node == self.rootNode:
            return QtCore.QModelIndex()
        return self.createIndex(parent_node.row(), 0, parent_node)

    def index(self, row, column, parent=QtCore.QModelIndex()):
        if self.hasIndex(row, column, parent):
            parent_node = self._get_node(parent)

            child_node = parent_node.child(row)

            if child_node:
                return self.createIndex(row, column, child_node)
        return QtCore.QModelIndex()

    def flags(self, index):
        return 0

    # def fetchMore(self, index)

    # def canFetchMore(self, index)

    # def hasChildren(self, index)


    # Internal class methods
    def _get_node(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self.rootNode

    def _find_node(self, name):
        """
        Find a node in the model by it's name
        """
        startindex = self.index(0, 0)
        if not startindex:
            return QtCore.QModelIndex()
        items = self.match(startindex, QtCore.Qt.DisplayRole, name, 1, QtCore.Qt.MatchExactly | QtCore.Qt.MatchWrap)
        try:
            return items[0]
        except IndexError:
            return QtCore.QModelIndex()



    # Private class methods
    def insertRows(self, position, rows, child, parent=QtCore.QModelIndex()):
        parent_node = self._get_node(parent)

        self.beginInsertRows(parent, position, position + rows - 1)
        parent_node.insertChild(position, child)
        self.endInsertRows()
        return True

    def removeRow(self, row, parent = QtCore.QModelIndex()):
        parent_node = self._get_node(parent)
        self.beginRemoveRows(parent, row, row)
        success = parent_node.removeChild(row)
        self.endRemoveRows()
        return success

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        print "\n\t\t ...removeRows() Starting position: '%s'" % position, 'with the total rows to be deleted: ', rows
        parent_node = self._get_node(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        parent_node.children = parent_node.children[:position] + parent_node.children[position + rows:]
        self.endRemoveRows()

        return True

    def addOuput(self, versionJSON, outputJSON):
        is_found = False
        count = self.rootNode.childCount()

        for i in range(count):
            child = self.rootNode.child(i)
            if child.version['id'] == versionJSON['id']:
                child_index = self._find_node(versionJSON['version'])
                new_output = Output(output=outputJSON)
                self.insertRows(child.childCount(), 1, new_output, child_index)
                self._record.append(outputJSON['id'])
                is_found = True
                break

        if not is_found:
            new_node = Version(version=versionJSON)
            new_output = Output(output=outputJSON, parent=new_node)
            self._record.append(outputJSON['id'])
            self.insertRows(count, 1, new_node)
            return True

        return False

    def removeIndex(self, index):
        node = self._get_node(index)
        id = node.get_id()

        parent_index = self.parent(index)
        if self.removeRow(index.row(), parent_index):
            self._record.remove(id)
            self.removeItem.emit(id)
            if not self.rowCount(parent_index):
                self.removeRow(parent_index.row())

    def removeOuput(self, versionJSON, outputJSON):
        count = self.rootNode.childCount()
        if not count:
            return
        child_index = self._find_node(versionJSON['version'])
        if not child_index.isValid():
            return
        node = child_index.internalPointer()
        # print 'before', node.children
        indices = [i for i, child in enumerate(node.children) if child.get_id() == outputJSON['id']]
        if indices:
            row = indices[0]

            result = self.removeRow(row, child_index)
            if result:
                self._record.remove(outputJSON['id'])
            else:
                print 'error removing row'


        self.removeItem.emit(outputJSON['id'])

        # print 'after', node.children
        if not node.children:
            self.removeRows(child_index.row(), 1)

    def is_checked(self, id):
        try:
            self._record.index(id)
            return True
        except:
            return False

    def get_info(self):
        return self._record

    # Private methods



