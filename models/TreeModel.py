from PySide import QtGui, QtCore, QtNetwork
import resources.icons
from Entity import Entity
from models.BaseModel import DataSource
from utils.bcolors import bcolors
from utils.json2obj import json2obj


class TreeModel(QtCore.QAbstractItemModel, DataSource):
    """docstring for TreeModel"""
    def __init__(self, root, parent=None, *args, **kwargs):
        super(TreeModel, self).__init__(parent)
        super(DataSource, self).__init__(*args, **kwargs)
        self.rootNode = root

        if self.rootNode._parent() is None and self.rootNode.entity is None:
            self.rootNode.setDataSource(self._getDataSource())

        self.numRows = 0
        self.xTotalCount = self.getXtotalCount()

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
            print(bcolors.FAIL + "\t end" + bcolors.ENDC)
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
        return 4

    def setColumnWidth(self, column, width):
        pass

    def data(self, index, role):

        # if role == QtCore.Qt.BackgroundRole:
        # 	print "BackgroundRole %s"%role

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
                elif typeInfo == "assets":
                    return QtGui.QIcon(QtGui.QPixmap(":/Light.jpg"))
                elif typeInfo == "Task":
                    return QtGui.QIcon(QtGui.QPixmap(":/Transform.jpg"))
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
        if index.isValid():
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
