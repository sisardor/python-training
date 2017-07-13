from PySide import QtGui, QtCore
from entity import Entity
from sources.api_provider import ApiProvider
from sources.constants import LIMIT, HEADER_HEIGHT, ROW_HEIGHT, THUMB_WIDTH, THUMB_HIEGHT, MARGIN
from sources.delegates.grouped_list_delegate import FONT_COLOR
from utils.json2obj import json2obj


class TreeModel(QtCore.QAbstractItemModel, ApiProvider):
    """docstring for TreeModel"""

    def __init__(self, root, parent=None, *args, **kwargs):
        super(TreeModel, self).__init__(parent)
        super(ApiProvider, self).__init__(*args, **kwargs)
        self.rootNode = root
        response = self._find_all(path='CommonFields')
        self.CommonFields = response['data']

        response2 = self._find_all(path='EntityTypes')
        self.EntityTypes = response2['data']
        self.EntityTypesDict = {}

        for item in self.EntityTypes:
            self.EntityTypesDict[item['name']] = item

        # fetch initial data
        self.rootNode._fetch_children(id=self.rootNode.get_id(), skip=0, limit=LIMIT)

        self.numRows = self.rootNode.childCount()
        # self.rootNode.insertChild(0, Node(text='..'))
        pass

    # Overriden public methods
    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == QtCore.Qt.SizeHintRole:
            return QtCore.QSize(100, ROW_HEIGHT)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if node.get_type_info() == 'dir' and index.column() == 0:
                return '..'
            elif node.get_type_info() == 'dir' and index.column() == 1:
                return None
            elif index.column() == 0:
                return node.entity['name']
            elif index.column() == 1:
                return self.EntityTypesDict[node.entity['type']]['label']
                # return node.entity['type']
            elif index.column() == 2:
                return node.entity['fields']['status']
            elif index.column() == 3:
                return node.entity['fields']['priority']
            else:
                return node.get_type_info()


        if role == QtCore.Qt.DecorationRole:
            if node.get_type_info() == 'dir':
                return None
            elif index.column() == 0:
                type_info = node.get_type_info()
                if type_info == "sequence":
                    return QtGui.QPixmap(":/thumbnail-missing.svg")\
                        .scaled(THUMB_WIDTH, ROW_HEIGHT - (MARGIN * 2), QtCore.Qt.KeepAspectRatio)
                elif node.entity['category'] == "groups":
                    image_path = node.get_thumbnail()
                    if image_path:
                        return QtGui.QPixmap(image_path)\
                            .scaled(THUMB_WIDTH, ROW_HEIGHT - (MARGIN * 2), QtCore.Qt.KeepAspectRatio)
                    # return QtGui.QIcon(QtGui.QPixmap(":/thumbnail-missing.svg"))
                elif node.entity['category'] == "tasks":
                    return QtGui.QIcon(QtGui.QPixmap(":/icon-tasks.svg"))
                else:
                    # url = 'http://10.0.0.146:8002/geotest/57ffe93aef8a9100011593ea/582a4918c9831f000149b0e3_sm.jpg'
                    # download_url = QtCore.QUrl(url)
                    # manager = QtNetwork.QNetworkAccessManager()
                    # request = QtNetwork.QNetworkRequest(download_url)
                    # reply = manager.get(request)
                    # print reply


                    # data = urllib.urlopen(url).read()
                    # image = QtGui.QImage()
                    # image.loadFromData(data)
                    # return QtGui.QIcon(QtGui.QPixmap(image))

                    return QtGui.QPixmap(":/thumbnail-missing.svg")\
                        .scaled(THUMB_WIDTH, ROW_HEIGHT - (MARGIN * 2), QtCore.Qt.KeepAspectRatio)

        if role == QtCore.Qt.BackgroundRole:
            if node.parent()._parent:
                return QtGui.QBrush(QtGui.QColor('#1d2022'))
            else:
                return QtGui.QBrush(QtGui.QColor('#2c2f30'))

        if role == QtCore.Qt.ForegroundRole:
            return QtGui.QBrush(QtGui.QColor('#AAAAAA'))

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            if role == QtCore.Qt.EditRole and index.column() == 2:
                node = index.internalPointer()
                result = node.set_field_status(value)
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
            return QtCore.QSize(100, HEADER_HEIGHT)

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

    def columnCount(self, parent):
        return 2

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
        if index.column() == 2 or index.column() == 3:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def fetchMore(self, index):
        node = self._get_node(index)
        if node.parent() is not None:
            # print "expend -> ", node.entity['id']
            node._fetch_children(id=node.entity['id'])
        else:
            remainder_rows = self.rootNode._x_total_count - self.numRows
            rows_to_fetch = min(LIMIT, remainder_rows)

            # print bcolors.OKGREEN + "\t fetching... \t { skip: %s, limit: %s }" % (self.numRows, rows_to_fetch) + bcolors.ENDC
            if rows_to_fetch > 0:
                self.beginInsertRows(QtCore.QModelIndex(), self.numRows, self.numRows + rows_to_fetch - 1)

                data = self.rootNode._fetch(id=self.rootNode.get_id(), skip=self.numRows, limit=rows_to_fetch)

                jj = 0
                for entity in data:
                    tmp_count = self.numRows + jj
                    child_node = Entity(entity=entity)
                    self.rootNode.insertChild(tmp_count, child_node)
                    jj += 1

                self.endInsertRows()
                self.numRows += rows_to_fetch
        return

    def canFetchMore(self, index):
        node = self._get_node(index)
        if node.parent() is not None and self.hasChildren(index):
            if node.childCount() == node.entity['$dependencyCount']:
                return False
            return True
        if self.rootNode._has_more_children():
            return True
        else:
            # print(bcolors.FAIL + "\t end" + bcolors.ENDC)
            return False

    def hasChildren(self, index):
        node = self._get_node(index)
        if node.parent() is None:
            return True
        return node.hasChildren()


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

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self._get_node(parent)

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
        parentNode = self._get_node(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        for row in range(rows):
            success = parentNode.removeChild(position)

        self.endRemoveRows()
        return success

    def _getEntityType(self, field):
        return (item for item in self.CommonFields if item["name"] == field).next()

    def set_task_id(self,id):
        pass



class Node(object):
    def __init__(self, text, parent=None):
        self.text = text
        self._parent = parent
        if parent is not None:
            parent.addChild(self)

    def childCount(self):
        return 0

    def hasChildren(self):
        return self.childCount()

    def get_type_info(self):
        return 'dir'

    def parent(self):
        return self._parent


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
