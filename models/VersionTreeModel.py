from PySide import QtCore, QtGui
from PySide.QtCore import QRectF
from PySide.QtGui import QStyledItemDelegate, QColor

ROW_HIGHT = 50
BORDER_COLOR_FOR_DELEGATE = "#3e4041"
THUMB_WIDTH = 70
THUMB_HIEGHT = 40
MARGIN = 5

class VersionDelegate(QtGui.QStyledItemDelegate):
    """docstring for VersionDelegate"""
    def __init__(self, parent=None):
        super(VersionDelegate, self).__init__(parent)

    def paint(self, painter, option, index):

        if index.column() == 0:
            if option.state & QtGui.QStyle.State_Selected:
                QStyledItemDelegate.paint(self, painter, option, index)

            # paint checkbox
            checkbox = index.data(QtCore.Qt.CheckStateRole)

            node = index.internalPointer()
            print node
            # paint thumbnail
            thumbnail_path = index.data(QtCore.Qt.UserRole)
            thumbnail_image = QtGui.QPixmap(thumbnail_path).scaled(THUMB_WIDTH, THUMB_HIEGHT)
            r = QtCore.QRect(option.rect.left() + MARGIN, option.rect.top() + MARGIN, THUMB_WIDTH, THUMB_HIEGHT)
            painter.drawPixmap(r, thumbnail_image)

            # paint name
            name = index.data(QtCore.Qt.DisplayRole)
            r = QtCore.QRect(option.rect.left() + THUMB_WIDTH + MARGIN + MARGIN,
                             option.rect.top(),
                             option.rect.width() - THUMB_WIDTH - MARGIN,
                             option.rect.height())

            painter.drawText(r, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft, name)


            # paint borders
            painter.setPen(QtGui.QPen(QtGui.QColor(BORDER_COLOR_FOR_DELEGATE), 1))
            # right border
            painter.drawLine(option.rect.topRight(), option.rect.bottomRight())
            # bottom border
            #if node.getType() == 'version':
            painter.drawLine(QtCore.QPoint(0, option.rect.bottom()), option.rect.bottomRight())
            pass
        else:
            painter.setPen(QtGui.QPen(QtGui.QColor(BORDER_COLOR_FOR_DELEGATE), 1))
            painter.drawLine(option.rect.topRight(), option.rect.bottomRight())
            painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())
            QStyledItemDelegate.paint(self, painter, option, index)



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

        typeInfo = node.getType()
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
            imagePath = node.getThumbnail()
            if imagePath:
                return imagePath
            else:
                return ':/thumbnail-missing.svg'

        elif role == QtCore.Qt.CheckStateRole and index.column() == 0:
            if node.isChecked():
                return QtCore.Qt.Checked
            else:
                return QtCore.Qt.Unchecked

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            if role == QtCore.Qt.CheckStateRole:
                node = index.internalPointer()
                node.setChecked(value)
                self.dataChanged.emit(index, index)
                return True

        return False

    def flags(self, index):
        # if index.isValid():
        #     return 0
        if index.column() == 0:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

if __name__ == '__main__':
    pass