from PySide import QtCore

ROW_HIGHT = 50


class VersionTreeModel(QtCore.QAbstractItemModel):
    """docstring for VersionTreeModel"""
    def __init__(self, shoppingCart, root=None, parent=None):
        super(VersionTreeModel, self).__init__(parent)
        self.rootNode = root
        self.shoppingCart = shoppingCart

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
        parent_node = node.parent()

        if parent_node == self.rootNode:
            return QtCore.QModelIndex()
        return self.createIndex(0, 0, parent_node)

    def index(self, row, column, parent):
        parent_node = self.getNode(parent)

        child_node = parent_node.child(row)

        if child_node:
            return self.createIndex(row, column, child_node)
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
        # if role == QtCore.Qt.DecorationRole:
        #     if index.column() == 0:
        #         path = node.get_thumbnail()
        #         return QtGui.QIcon(QtGui.QPixmap(path))

        typeInfo = node.get_type_info()
        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                if typeInfo == 'version':
                    return node.version['version']
                else:
                    return node.version['type']
            elif index.column() == 1:
                if typeInfo == 'version':
                    return node.version['createdBy']
                else:
                    return '[N/A]'
            elif index.column() == 2:
                return node.version['createdAt']
        elif role == QtCore.Qt.SizeHintRole:
            return QtCore.QSize(100,ROW_HIGHT)
        elif role == QtCore.Qt.UserRole:
            imagePath = node.get_thumbnail()
            if imagePath:
                return imagePath
            else:
                return ':/thumbnail-missing.svg'

        elif role == QtCore.Qt.CheckStateRole and index.column() == 0:
            return node.isChecked()


    def setData(self, index, value, role=QtCore.Qt.EditRole):
        print 'setData'
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

    def flags(self, index):
        if index.column() == 0:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

if __name__ == '__main__':
    pass