import os
import sys
import resources.icons
from models.VersionTreeModel import VersionDelegate, VersionTreeModel
from models.Version import Version
from models.Entity import Entity
from models.TreeModel import TreeModel
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
        QtCore.QObject.connect(self.project_tree_view.uiTree,
                               QtCore.SIGNAL("clicked(QModelIndex)"),
                               self.row_changed)
        self.current = None



        ######################
        self.version_tree_view = VersionTreeWidget(parent)
        self.version_tree_view.uiTree.setItemDelegate(VersionDelegate())


        self.layoutWest.addWidget(self.project_tree_view.uiTree)
        self.layoutMiddle.addWidget(self.version_tree_view.uiTree)

    def resizeEvent(self, event):
        self.project_tree_view.resizeEvent(event)
        self.version_tree_view.resizeEvent(event)
        pass

    def row_selected(self, selected):
        pass

    def row_changed(self, current):
        self.current = current
        node = current.internalPointer()

        entity_version_model = Version(entity=node.entity)
        version_list_model = VersionTreeModel(root=entity_version_model)
        self.version_tree_view.uiTree.setModel(version_list_model)

        self.version_tree_view.uiTree.header().setResizeMode(0, QtGui.QHeaderView.Stretch)

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