import os
import sys
import resources.icons
from models.version_tree_delegate import VersionDelegate
from models.version_tree_model import VersionTreeModel
from models.version import Version
from models.entity import Entity
from models.tree_model import TreeModel
from PySide import QtCore, QtGui

from models.grouped_list_view import GroupedListView
from utils.pyside_dynamic import loadUi
from views.entity_tree_ui import EntityTreeUI
from views.outputs_tree_ui import OutputsTreeUI
from views.treeWidget import TreeWidget
from views.version_tree_widget import VersionTreeWidget

path = os.path.dirname(os.path.abspath(__file__))


class MainController(QtGui.QMainWindow):
    """docstring for MainController"""
    shoppingCart = QtCore.Signal()
    def __init__(self, parent=None):
        super(MainController, self).__init__(parent)
        loadUi(os.path.join(path, 'views/ui/mainwindow.ui'), self)

        self.shoppingCart = GroupedListView()
        self.outputs_tree_ui = OutputsTreeUI(model=self.shoppingCart)
        self.horizontalLayout.addWidget(self.outputs_tree_ui)

        ######################
        self.project_model = Entity(projectName='skyline')
        self.project_tree_model = TreeModel(root=self.project_model)
        self.project_tree_view = EntityTreeUI(model=self.project_tree_model)

        ######################
        self.version_tree_view = VersionTreeWidget(parent=parent)


        self.layoutWest.addWidget(self.project_tree_view)
        self.layoutMiddle.addWidget(self.version_tree_view)

        self.selection_model = QtGui.QItemSelectionModel(self.project_tree_model, self.project_tree_view)
        self.selection_model.selectionChanged.connect(self.row_selected)
        self.project_tree_view.setSelectionModel(self.selection_model)
        QtCore.QObject.connect(self.project_tree_view,
                               QtCore.SIGNAL("clicked(QModelIndex)"),
                               self.row_changed)

    def resizeEvent(self, event):
        self.project_tree_view.resizeEvent(event)
        self.version_tree_view.resizeEvent(event)

    def row_selected(self, selected):
        pass

    def row_changed(self, current):
        node = current.internalPointer()

        version_list_model = VersionTreeModel(root=Version(entity=node.entity),
                                              shoppingCart=self.shoppingCart)
        self.version_tree_view.setModel(version_list_model)
        self.version_tree_view.header().setResizeMode(0, QtGui.QHeaderView.Stretch)

    @QtCore.Slot()
    def mySlot(self, id):
        print "selectionChanged", id
        pass










if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    data = [ "a", "b" ]
    model = QtGui.QStringListModel(data)
    listView = QtGui.QListView()
    listView.show()
    listView.setModel(model)

    loadUi(os.path.join(path, 'views/ui/treeview.ui'), listView)
    sys.exit(app.exec_())