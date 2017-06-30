from PySide import QtCore, QtGui
from PySide.QtGui import QStyledItemDelegate


class VersionDelegate(QtGui.QStyledItemDelegate):
    """docstring for VersionDelegate"""
    def __init__(self, parent=None):
        super(VersionDelegate, self).__init__(parent)


    def paint(self, painter, option, index):

        if index.column() == 0:
            # print option.rect, option.rect.top()
            x = option.rect.x()
            y = option.rect.y()
            print '{ x: %s, y: %s}'%(x, y)
            image = QtGui.QImage(str(
                '/Users/zeromax/MAVIS_WORKPLACE/static/skyline/59540cc279a4ba139b8154ca/59540d3479a4ba139b8154f6_med.jpg'))
            pixmap = QtGui.QPixmap.fromImage(image)
            pixmap.scaledToHeight(35, QtCore.Qt.FastTransformation)
            painter.drawPixmap(x+5, y+5, 50, 35, pixmap)


        if index.column() == 6:
            node = index.internalPointer()
            print node
            image = QtGui.QImage(str('/Users/zeromax/MAVIS_WORKPLACE/static/skyline/59540cc279a4ba139b8154ca/59540d3479a4ba139b8154f6_med.jpg'))
            pixmap = QtGui.QPixmap.fromImage(image)
            pixmap.scaledToHeight(35, QtCore.Qt.FastTransformation)
            painter.drawPixmap(option.rect, pixmap)
            pass
        else:
            QStyledItemDelegate.paint(self, painter, option, index)
    #     pass


class VersionTreeModel(QtCore.QAbstractItemModel):
    """docstring for VersionTreeModel"""
    def __init__(self, root=None, parent=None):
        super(VersionTreeModel, self).__init__(parent)
        self.rootNode = root

    # def hasChildren(self, index):
    #     node = self.getNode(index)
    #     if node._parent() is None:
    #         return True
    #
    #     return node.hasOutputs()

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
        # if role == QtCore.Qt.DecorationRole:
        #     if index.column() == 0:
        #         path = node.getThumbnail()
        #         return QtGui.QIcon(QtGui.QPixmap(path))


        if role == QtCore.Qt.DisplayRole:
            typeInfo = node.getType()
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
            print "giving size hint"
            return QtCore.QSize(50,50)


if __name__ == '__main__':
    pass