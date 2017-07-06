import os
import sys
import resources.icons
from models.VersionTreeModel import VersionDelegate, VersionTreeModel
from models.Version import Version
from models.Entity import Entity
from models.TreeModel import TreeModel
from PySide import QtCore, QtGui

from models.grouped_list_view import GroupedListView
from utils.pyside_dynamic import loadUi
from views.treeWidget import TreeWidget
from views.version_tree_widget import VersionTreeWidget

path = os.path.dirname(os.path.abspath(__file__))


# class ShoppingCart(object):
#     """docstring for ShoppingCart"""
#     def __init__(self):
#         super(ShoppingCart, self).__init__()
#         self.list = []
#
#     def addItem(self, node):
#         result =  [index for index, item in enumerate(self.list) if item.isEqual(node) ]
#         print result
#         if not result:
#             self.list.append(node)
#         print '\n================='
#         for item in self.list:
#             print item
#
#     def removeItem(self, node):
#         indices = [ index for index, item in enumerate(self.list) if item.isEqual(node) ]
#
#         for index in indices:
#             del self.list[index]
#
#
#         pass


class ShoppingCart(QtCore.QAbstractListModel):
    def __init__(self, datain, parent=None, *args):
        """ datain: a list where each item is a row
        """
        super(ShoppingCart, self).__init__(parent, *args)
        self.listdata = datain

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.listdata)

    def data(self, index, role):

        if index.isValid() and role == QtCore.Qt.DisplayRole:

            return self.listdata[index.row()].version['type']

    def addItem(self, node):
        result =  [index for index, item in enumerate(self.listdata) if item.isEqual(node) ]
        # print result
        if not result:
            self.listdata.append(node)
        # print '\n================='
        # for item in self.listdata:
        #     print item
        self.dataChanged.emit(0, 0)

    def removeItem(self, node):
        indices = [ index for index, item in enumerate(self.listdata) if item.isEqual(node) ]

        for index in indices:
            del self.listdata[index]
        self.dataChanged.emit(0, 0)


class MainController(QtGui.QMainWindow):
    """docstring for MainController"""
    shoppingCart = QtCore.Signal()
    def __init__(self, parent=None):
        super(MainController, self).__init__(parent)
        loadUi(os.path.join(path, 'views/ui/mainwindow.ui'), self)
        tempV = Version()
        # Version(parent=tempV)
        self.shoppingCart = GroupedListView(tempV)
        self.shoppingTree.setModel(self.shoppingCart)

        print  self.shoppingTree

        ######################
        self.project_model = Entity(projectName='skyline')
        self.project_tree_model = TreeModel(root=self.project_model)
        self.project_tree_view = TreeWidget(parent)
        self.project_tree_view.uiTree.setModel(self.project_tree_model)

        ######################
        self.version_tree_view = VersionTreeWidget(parent=parent)
        self.version_tree_view.uiTree.setItemDelegate(VersionDelegate())


        self.layoutWest.addWidget(self.project_tree_view.uiTree)
        self.layoutMiddle.addWidget(self.version_tree_view.uiTree)

        # self.version_tree_view.setShoppingCart(self.shoppingCart)


        self.selection_model = QtGui.QItemSelectionModel(self.project_tree_model, self.project_tree_view.uiTree)
        self.selection_model.selectionChanged.connect(self.row_selected)
        self.project_tree_view.uiTree.setSelectionModel(self.selection_model)
        QtCore.QObject.connect(self.project_tree_view.uiTree,
                               QtCore.SIGNAL("clicked(QModelIndex)"),
                               self.row_changed)


    def resizeEvent(self, event):
        self.project_tree_view.resizeEvent(event)
        self.version_tree_view.resizeEvent(event)
        pass

    def row_selected(self, selected):
        pass

    def row_changed(self, current):
        node = current.internalPointer()

        entity_version_model = Version(entity=node.entity)
        version_list_model = VersionTreeModel(root=entity_version_model, shoppingCart=self.shoppingCart)
        self.version_tree_view.uiTree.setModel(version_list_model)

        self.version_tree_view.uiTree.header().setResizeMode(0, QtGui.QHeaderView.Stretch)

        self.shoppingTree.expandAll()
        self.shoppingTree.setItemsExpandable(False)

    @QtCore.Slot()
    def mySlot(self, id):
        print "selectionChanged", id
        pass

    def closeEvent(self, event):
        print "closeEvent"









if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    data = [ "a", "b" ]
    model = QtGui.QStringListModel(data)
    listView = QtGui.QListView()
    listView.show()
    listView.setModel(model)

    loadUi(os.path.join(path, 'views/ui/treeview.ui'), listView)
    sys.exit(app.exec_())