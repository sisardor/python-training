from PySide import QtCore, QtGui

from sources.constants import LATEST_VERSION, NODE_ID, ROW_HIGHT, HEADER_HEIGHT


class VersionTreeModel(QtCore.QAbstractItemModel):
    """docstring for VersionTreeModel"""

    def __init__(self, shoppingCart, root=None, parent=None):
        super(VersionTreeModel, self).__init__(parent)
        self.rootNode = root
        self.shoppingCart = shoppingCart

        count = self.rootNode.childCount()
        for i in range(count):
            self.rootNode.child(i).setCheckedState(self.shoppingCart.is_checked)

        self.shoppingCart.removeItem.connect(self._uncheck_item)

    # Overriden public methods
    def data(self, index, role):
        # if role == QtCore.Qt.DisplayRole:
        #     return 'test'
        if not index.isValid():
            print 'error'
            return None
        node = index.internalPointer()
        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                path = node.get_thumbnail()
                if path:
                    return QtGui.QIcon(QtGui.QPixmap(path))
                return QtGui.QIcon(QtGui.QPixmap(":/thumbnail-missing.svg"))

        type_info = node.get_type_info()
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                if type_info == 'version':
                    return node.version['version']
                else:
                    return node.version['type']


            elif index.column() == 1:
                if type_info == 'version':
                    return node.version['createdBy']
                else:
                    return '[N/A]'
            elif index.column() == 2:
                return node.get_created_at()
        # elif role == QtCore.Qt.SizeHintRole:
        #     return QtCore.QSize(100,ROW_HIGHT)
        elif role == QtCore.Qt.UserRole:
            imagePath = node.get_thumbnail()
            if imagePath:
                return imagePath
            else:
                return ':/thumbnail-missing.svg'
        elif role == NODE_ID:
            return node.get_id()
        elif role == LATEST_VERSION and node.is_latest_version():
            return True
        elif role == QtCore.Qt.CheckStateRole and index.column() == 0:
            return node.isChecked()

    def setData(self, index, value, role=QtCore.Qt.EditRole):

        if index.isValid():
            if role == QtCore.Qt.CheckStateRole:
                node = index.internalPointer()
                node.setChecked(value)
                if node.get_type_info() == 'output':
                    outputJSON = node.version
                    versionJSON = node.parent().version
                    if value:
                        self.shoppingCart.addOuput(versionJSON, outputJSON)
                    else:
                        self.shoppingCart.removeOuput(versionJSON, outputJSON)
                else:
                    count = node.childCount()
                    versionJSON = node.version
                    for i in range(count):
                        outputJSON = node.child(i).version

                        if value:
                            self.shoppingCart.addOuput(versionJSON, outputJSON)
                        else:
                            self.shoppingCart.removeOuput(versionJSON, outputJSON)

                self.dataChanged.emit(index, 0)
                return True

        return False

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.SizeHintRole:
            return QtCore.QSize(100, HEADER_HEIGHT)

        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Name"
            elif section == 1:
                return "Published by"
            elif section == 2:
                return "Modified"

    def columnCount(self, parent):
        return 3

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
        if not index.isValid():
            return 0

        if index.column() == 0:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

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

    def _find_node(self, name, startindex=None):
        """
        Find a node in the model by it's name
        """
        if not startindex:
            startindex = self.index(0, 0)

        if not startindex:
            return QtCore.QModelIndex()
        items = self.match(startindex, QtCore.Qt.DisplayRole, name, 1, QtCore.Qt.MatchExactly | QtCore.Qt.MatchWrap)
        try:
            return items[0]
        except IndexError:
            return QtCore.QModelIndex()

    def _uncheck_item(self, id):
        count = self.rootNode.childCount()
        for i in range(count):
            child_node = self.index(0,0, self.index(i,0))
            if not child_node.isValid():
                return
            indices = self.match(child_node, NODE_ID, id, 1, QtCore.Qt.MatchExactly | QtCore.Qt.MatchWrap)
            if indices:
                node = indices[0].internalPointer()
                node.setChecked(0)
                self.dataChanged.emit(child_node,0)
                break

if __name__ == '__main__':
    pass