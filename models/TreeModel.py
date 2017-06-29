from PySide import QtGui, QtCore, QtNetwork
from Entity import Entity
from models.BaseModel import DataSource
from utils.bcolors import bcolors
from utils.detect_color import detectColor
from utils.json2obj import json2obj
from PySide.QtGui import (QItemDelegate, QStyledItemDelegate, QStyle, QColor, QBrush)
import resources.icons
class StarDelegate(QStyledItemDelegate):
    """ A subclass of QStyledItemDelegate that allows us to render our
        pretty star ratings.
    """

    def __init__(self, parent=None):
        super(StarDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        """ Paint the items in the table.

            If the item referred to by <index> is a StarRating, we handle the
            painting ourselves. For the other items, we let the base class
            handle the painting as usual.

            In a polished application, we'd use a better check than the
            column number to find out if we needed to paint the stars, but
            it works for the purposes of this example.
        """
        if index.column() == 2:
            starRating = StarRating(index.data())

            # If the row is currently selected, we need to make sure we
            # paint the background accordingly.
            if option.state & QStyle.State_Selected:
                # The original C++ example used option.palette.foreground() to
                # get the brush for painting, but there are a couple of
                # problems with that:
                #   - foreground() is obsolete now, use windowText() instead
                #   - more importantly, windowText() just returns a brush
                #     containing a flat color, where sometimes the style
                #     would have a nice subtle gradient or something.
                # Here we just use the brush of the painter object that's
                # passed in to us, which keeps the row highlighting nice
                # and consistent.
                painter.fillRect(option.rect, painter.brush())

            # Now that we've painted the background, call starRating.paint()
            # to paint the stars.
            starRating.paint(painter, option.rect, option.palette)
        else:
            QStyledItemDelegate.paint(self, painter, option, index)

    def sizeHint(self, option, index):
        """ Returns the size needed to display the item in a QSize object. """
        if index.column() == 2:
            starRating = StarRating(index.data())
            return starRating.sizeHint()
        else:
            return QStyledItemDelegate.sizeHint(self, option, index)

    # The next 4 methods handle the custom editing that we need to do.
    # If this were just a display delegate, paint() and sizeHint() would
    # be all we needed.

    def createEditor(self, parent, option, index):
        """ Creates and returns the custom StarEditor object we'll use to edit
            the StarRating.
        """
        if index.column() == 2:
            combo = QtGui.QComboBox(parent)
            li = []
            li.append("Zero")
            li.append("One")
            li.append("Two")
            li.append("Three")
            li.append("Four")
            li.append("Five")
            combo.addItems(li)
            return combo

            editor = StarEditor(parent)
            editor.editingFinished.connect(self.commitAndCloseEditor)
            return editor
        else:
            return QStyledItemDelegate.createEditor(self, parent, option, index)

    def setEditorData(self, editor, index):
        """ Sets the data to be displayed and edited by our custom editor. """
        if index.column() == 2:
            editor.starRating = StarRating(index.data())
        else:
            QStyledItemDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        """ Get the data from our custom editor and stuffs it into the model.
        """
        if index.column() == 2:
            model.setData(index, editor.starRating.starCount)
        else:
            QStyledItemDelegate.setModelData(self, editor, model, index)

    def commitAndCloseEditor(self):
        """ Erm... commits the data and closes the editor. :) """
        editor = self.sender()

        # The commitData signal must be emitted when we've finished editing
        # and need to write our changed back to the model.
        self.commitData.emit(editor)
        self.closeEditor.emit(editor)

BORDER_COLOR_FOR_DELEGATE = "#3e4041"



class ComboDelegate(QtGui.QStyledItemDelegate):
    """
    A delegate that places a fully functioning QComboBox in every
    cell of the column to which it's applied
    """
    def __init__(self, parent=None):
        super(ComboDelegate, self).__init__(parent)

    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        editor.setCurrentIndex(editor.findData(value))

    def createEditor(self, parent, option, index):
        field = index.model()._getEntityType('status')
        options = field['options']
        combo = QtGui.QComboBox(parent)
        for o in options:
            combo.addItem(o['name'], o['label'])

        # combo.connect(self.commitAndCloseEditor)
        return combo

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def paint(self, painter, option, index):
        painter.save()
        value = index.data(QtCore.Qt.DisplayRole)

        # set background color
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        field = index.model()._getEntityType('status')
        options = field['options']
        o = (item for item in options if item["name"] == value or item["name"] == value).next()
        background = o['color']
        if option.state & QStyle.State_Selected:
            painter.setBrush(QtGui.QBrush(QtCore.Qt.white))
            painter.setBrush(QtGui.QBrush(QColor(background)))
        else:
            painter.setBrush(QtGui.QBrush(QColor(background)))
        painter.drawRect(option.rect)

        # set borders
        painter.setPen(QtGui.QPen(QColor(BORDER_COLOR_FOR_DELEGATE), 1))
        painter.drawLine(option.rect.topRight(), option.rect.bottomRight())
        painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())

        # set text color
        textColor = detectColor(background)
        painter.setPen(QtGui.QPen(QColor(textColor)))
        painter.drawText(option.rect, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter, value)
        painter.restore()


class TreeModel(QtCore.QAbstractItemModel, DataSource):
    """docstring for TreeModel"""
    def __init__(self, root, parent=None, *args, **kwargs):
        super(TreeModel, self).__init__(parent)
        super(DataSource, self).__init__(*args, **kwargs)
        self.rootNode = root

        if self.rootNode._parent() is None and self.rootNode.entity is None:
            self.rootNode.setDataSource(self._getDataSource())

        self.EntityTypes = self.fetch(path='CommonFields')
        self.numRows = 0
        self.xTotalCount = self.getXtotalCount()

    """private"""
    def _getEntityType(self, field):
        return (item for item in self.EntityTypes if item["name"] == field).next()

    def hasChildren(self, index):
        node = self.getNode(index)
        if node._parent() is None:
            return True
        return node.hasChildren()

    def canFetchMore(self, index):
        node = self.getNode(index)
        if node._parent() is not None and self.hasChildren(index):
            if node.childCount() == node.entity['$dependencyCount']:
                return False
            return True
        if self.numRows < self.xTotalCount:
            return True
        else:
            # print(bcolors.FAIL + "\t end" + bcolors.ENDC)
            return False

    def fetchMore(self, index):
        node = self.getNode(index)
        if node._parent() is not None:
            # print "expend -> ", node.entity['id']
            data = self.rootNode.fetchChildren(id=node.entity['id'])
            for entity in data:
                child_node = Entity("untitled", entity)
                node.insertChild(0, child_node)

        if node._parent() is None:
            max_fetch = 50
            remainder_rows = self.xTotalCount - self.numRows
            rows_to_fetch = min(max_fetch, remainder_rows)
            # print bcolors.OKGREEN + "\t fetching... \t { skip: %s, limit: %s }" % (self.numRows, rows_to_fetch) + bcolors.ENDC
            if rows_to_fetch > 0:
                self.beginInsertRows(QtCore.QModelIndex(), self.numRows, self.numRows + rows_to_fetch - 1)

                data = self.rootNode.fetch(skip=self.numRows, limit=rows_to_fetch)
                self.xTotalCount = self.rootNode.getXTotalCount()

                jj = 0
                for entity in data:
                    tmp_count = self.numRows + jj
                    child_node = Entity("untitled", entity)
                    self.rootNode.insertChild(tmp_count, child_node)
                    jj += 1

                self.endInsertRows()
                self.numRows += rows_to_fetch

        return

    def rowCount(self, parent):
        # return self.numRows
        if not parent.isValid():
            parentNode = self.rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    def columnCount(self, parent):
        return 2

    def setColumnWidth(self, column, width):
        pass

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return node.entity['name']
            elif index.column() == 1:
                return node.entity['type']
            elif index.column() == 2:
                return node.entity['fields']['status']
            elif index.column() == 3:
                return node.entity['fields']['priority']
            else:
                return node.typeInfo()

        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                typeInfo = node.typeInfo()
                if typeInfo == "sequence":
                    # url = 'http://10.0.0.146:8002/geotest/57d861566fef3a0001c879b1/580fdded7ad29f000132c694_med.jpg'
                    # data = urllib.urlopen(url).read()
                    # image = QtGui.QImage()
                    # image.loadFromData(data)
                    # return QtGui.QIcon(QtGui.QPixmap(image))
                    return QtGui.QIcon(QtGui.QPixmap(":/thumbnail-missing.svg"))
                elif node.entity['category'] == "groups":
                    imagePath = node.getThumbnail()
                    if imagePath:
                        return QtGui.QIcon(QtGui.QPixmap(imagePath))
                elif node.entity['category'] == "tasks":
                    return QtGui.QIcon(QtGui.QPixmap(":/icon-tasks.svg"))
                elif typeInfo == "Camera":
                    return QtGui.QIcon(QtGui.QPixmap(":/Camera.jpg"))
                else:
                    url = 'http://10.0.0.146:8002/geotest/57ffe93aef8a9100011593ea/582a4918c9831f000149b0e3_sm.jpg'
                    # download_url = QtCore.QUrl(url)
                    # manager = QtNetwork.QNetworkAccessManager()
                    # request = QtNetwork.QNetworkRequest(download_url)
                    # reply = manager.get(request)
                    # print reply


                    # data = urllib.urlopen(url).read()
                    # image = QtGui.QImage()
                    # image.loadFromData(data)
                    # return QtGui.QIcon(QtGui.QPixmap(image))

                    return QtGui.QIcon(QtGui.QPixmap(":/thumbnail-missing.svg"))

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self.rootNode

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)

        self.beginInsertRows(parent, position, position + rows - 1)
        for row in range(rows):
            child_count = parentNode.childCount()
            # print self.numRows, "  ", row
            count_tmp = self.numRows + (10 - row)
            entity = json2obj(
                '{"dependencyCount":0,"category":"tasks","path":"/mnt/x19/mavisdev/projects/geotest/sequence/mdm_0202/shots/mdm_0202_0100/assets/tuktuka/model/tuktuk_model","name":"untitled-' + str(count_tmp) + '","description":"published plate 6310","latest":"58c6ffe6e925cc00016a6b58","fileImportPath":"","isGlobal":false,"project":"geotest","fields":{"priority":"high","status":"revised","grouping":"vehi","comp_status":"Waiting","prod_status":"MEDIUM"},"createdBy":"trevor","createdAt":"2017-04-13T22:08:33.983Z","updatedAt":"2017-04-18T20:35:28.557Z","id":"589b4f9dc599d10001375de9","type":"model","mediaIds":[],"parentId":"589b4f10c599d10001375de2","isTest":false}')
            # Node('New', entity, self.rootNode)
            child_node = Entity("untitled" + str(child_count), entity)
            success = parentNode.insertChild(position, child_node)
        self.endInsertRows()

        return success

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        for row in range(rows):
            success = parentNode.removeChild(position)

        self.endRemoveRows()
        return success

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        print '#### setData', index.column()
        if index.isValid():
            if role == QtCore.Qt.EditRole and index.column() == 2:
                node = index.internalPointer()
                result = node.setFieldStatus(value, ds=self._getDataSource())
                self.dataChanged.emit(index, index)
                return True

            if role == QtCore.Qt.EditRole:
                node = index.internalPointer()
                node.setProjectName(value)
                self.dataChanged.emit(index, index)
                return True
        return False

    def headerData(self, section, orientation, role):
        # if role == QtCore.Qt.DecorationRole:
        # 	print "QtCore.Qt.DecorationRole %s"%role

        if role == QtCore.Qt.SizeHintRole:
            if section == 0:
                return QtCore.QSize(350, 25)
            else:
                return QtCore.QSize(100, 25)

        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Name"
            elif section == 1:
                return "Type"
            elif section == 2:
                return "Status"
            elif section == 3:
                return "Priority"
            elif section == 4:
                return "Assignees"
            else:
                return "Type"

    def flags(self, index):
        if index.column() == 2 or index.column() == 3:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

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


if __name__ == '__main__':
    import sys
    import pprint
    sys.path.append("/mnt/x19/mavisdev/mavis_scripts/pydraulx")
    from connection import mavis as mavis

    conn = mavis.getMavis(username='cdeng', password='ASD123qwe')
    response = conn.get('Entities/rampage')
    pp = pprint.PrettyPrinter(indent=4)


    print '\n========================================'
    pp.pprint(response)
