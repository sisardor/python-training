import os
import sys

from PySide.QtGui import QItemSelectionModel

import resources.icons
from models.VersionTreeModel import VersionDelegate, VersionTreeModel
from models.Vesion import Version
from utils.json2obj import json2obj
from models.Entity import Entity
from models.TreeModel import TreeModel, StarDelegate
from PySide import QtCore, QtGui
from utils.pyside_dynamic import loadUi
from views.treeWidget import TreeWidget
from views.version_tree_widget import VersionTreeWidget

path = os.path.dirname(os.path.abspath(__file__))


class MainController(QtGui.QMainWindow):
    """docstring for MainController"""
    def __init__(self, parent=None):
        super(MainController, self).__init__(parent)
        loadUi(os.path.join(path, 'views/ui/mainwindow.ui'), self)
        ######################
        self.project_model = Entity(projectName='skyline')
        self.project_tree_model = TreeModel(root=self.project_model)
        self.project_tree_view = TreeWidget(parent)
        self.project_tree_view.uiTree.setModel(self.project_tree_model)

        self.selection_model = QtGui.QItemSelectionModel(self.project_tree_model, self.project_tree_view.uiTree)
        self.project_tree_view.uiTree.setSelectionModel(self.selection_model)
        self.selection_model.selectionChanged.connect(self.row_selected)
        QtCore.QObject.connect(self.project_tree_view.uiTree,\
                               QtCore.SIGNAL("clicked(QModelIndex)"),\
                               self.row_changed)
        self.current = None



        ######################
        # v1 = json2obj(
        #     '{"version":"v001.000","major":1,"minor":0,"path":"/Users/zeromax/MAVIS_WORKPLACE/projects/rampage/shots/test-0/v001.000","source":"/Users/zeromax/MAVIS_WORKPLACE/projects/rampage/shots/test-0","project":"rampage","isMajorVersion":true,"externalJobStatus":"NO_REQUEST","jobStatus":"NO_REQUEST","createdBy":"cdeng","createdAt":"2017-06-28T18:29:02.499Z","id":"5953f56e79a4ba139b815493","entityId":"5930a4e9eb93bb7b5efb9565","inputIds":[],"proxies":[]}')
        # v2 = json2obj(
        #     '{"version":"v002.000","major":2,"minor":0,"path":"/Users/zeromax/MAVIS_WORKPLACE/projects/rampage/shots/test-0/v002.000","source":"/Users/zeromax/MAVIS_WORKPLACE/projects/rampage/shots/test-0","project":"rampage","isMajorVersion":true,"externalJobStatus":"NO_REQUEST","jobStatus":"NO_REQUEST","createdBy":"cdeng","createdAt":"2017-06-28T18:29:09.718Z","id":"5953f57579a4ba139b815495","entityId":"5930a4e9eb93bb7b5efb9565","inputIds":[],"proxies":[]}')
        #
        # self.entity_version_model = Version(entity = self.project_model.entity)
        # Version(version=v1, parent=self.entity_version_model)

        # self.version_list_model = VersionTreeModel(root=self.entity_version_model)
        self.version_tree_view = VersionTreeWidget(parent)
        self.version_tree_view.uiTree.setItemDelegate(VersionDelegate())
        # self.version_tree_view.uiTree.setModel(self.version_list_model)





        self.layoutWest.addWidget(self.project_tree_view.uiTree)
        self.layoutMiddle.addWidget(self.version_tree_view.uiTree)

    def resizeEvent(self, event):
        self.project_tree_view.resizeEvent(event)
        pass

    def row_selected(self, selected):
        # print selected.indexes()
        # item = selected.
        pass

    def row_changed(self, current):
        self.current = current
        node = current.internalPointer()
        entity_version_model = Version(entity=node)
        v1 = json2obj(
            '{"version":"v001.000","major":1,"minor":0,"path":"/Users/zeromax/MAVIS_WORKPLACE/projects/rampage/shots/test-0/v001.000","source":"/Users/zeromax/MAVIS_WORKPLACE/projects/rampage/shots/test-0","project":"rampage","isMajorVersion":true,"externalJobStatus":"NO_REQUEST","jobStatus":"NO_REQUEST","createdBy":"cdeng","createdAt":"2017-06-28T18:29:02.499Z","id":"5953f56e79a4ba139b815493","entityId":"5930a4e9eb93bb7b5efb9565","inputIds":[],"proxies":[]}')

        Version(version=v1, parent=entity_version_model)
        version_list_model = VersionTreeModel(root=entity_version_model)
        self.version_tree_view.uiTree.setModel(version_list_model)

        print 'row_changed', node

    @QtCore.Slot()
    def mySlot(self, id):
        print "selectionChanged", id
        pass

    def current_row_changed(self, current_idx, prev_idx):

        # print 'current: %s \t prev: %s'%(current_idx, prev_idx)
        if prev_idx == None:
            return
        print "currentRowChanged\n"
        item = current_idx.internalPointer()

        v1 = json2obj(
            '{"version":"v006.000","major":1,"minor":0,"path":"/Users/zeromax/MAVIS_WORKPLACE/projects/rampage/shots/test-0/v001.000","source":"/Users/zeromax/MAVIS_WORKPLACE/projects/rampage/shots/test-0","project":"rampage","isMajorVersion":true,"externalJobStatus":"NO_REQUEST","jobStatus":"NO_REQUEST","createdBy":"cdeng","createdAt":"2017-06-28T18:29:02.499Z","id":"5953f56e79a4ba139b815493","entityId":"5930a4e9eb93bb7b5efb9565","inputIds":[],"proxies":[]}')
        v2 = json2obj(
            '{"version":"v005.000","major":2,"minor":0,"path":"/Users/zeromax/MAVIS_WORKPLACE/projects/rampage/shots/test-0/v002.000","source":"/Users/zeromax/MAVIS_WORKPLACE/projects/rampage/shots/test-0","project":"rampage","isMajorVersion":true,"externalJobStatus":"NO_REQUEST","jobStatus":"NO_REQUEST","createdBy":"cdeng","createdAt":"2017-06-28T18:29:09.718Z","id":"5953f57579a4ba139b815495","entityId":"5930a4e9eb93bb7b5efb9565","inputIds":[],"proxies":[]}')

        versions = Version(entity=item.entity)
        Version(version=v1, parent=versions)
        Version(version=v2, parent=versions)

        versionsTree = VersionTreeModel(root=versions)
        self.versionTree.uiTree.setModel(versionsTree)

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