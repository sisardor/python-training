import os
import sys
import resources.icons
from sources.version_tree_model import VersionTreeModel
from sources.version import Version
from sources.entity import Entity
from sources.tree_model import TreeModel
from PySide import QtCore, QtGui
from sources.grouped_list_model import GroupedListView
from utils.pyside_dynamic import loadUi
from views.entity_tree_ui import EntityTreeUI
from views.outputs_tree_ui import OutputsTreeUI

from views.version_tree_widget import VersionTreeWidget

path = os.path.dirname(os.path.abspath(__file__))


class MainController(QtGui.QMainWindow):
    """docstring for MainController"""
    # shoppingCart = QtCore.Signal()
    def __init__(self, parent=None):
        super(MainController, self).__init__(parent)
        loadUi(os.path.join(path, 'views/ui/mainwindow.ui'), self)

        self.task_id_input.textChanged.connect(self.inputChange)

        self.shoppingCart = GroupedListView()
        self.outputs_tree_ui = OutputsTreeUI(model=self.shoppingCart)

        self.horizontalLayout.addWidget(self.outputs_tree_ui)

        ######################
        self.current_dir.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.current_dir.setContentsMargins(0, 0, 0, 0)
        self.current_dir.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        self.project_model = Entity(id='580799dede2171292a05a0d6')
        self.current_dir.setText(self.project_model.get_display_name())
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
        QtCore.QObject.connect(self.project_tree_view,
                               QtCore.SIGNAL("doubleClicked(QModelIndex)"),
                               self.doubleClick)


    def doubleClick(self, index):
        print index
        pass

    def inputChange(self, text):
        # print text
        project_model = Entity(current_loaded_entity_id=text)
        self.current_dir.setText(project_model.get_display_name())
        project_tree_model = TreeModel(root=project_model)
        self.project_tree_view.setModel(project_tree_model)


    def resizeEvent(self, event):
        self.project_tree_view.resizeEvent(event)
        self.version_tree_view.resizeEvent(event)

    def row_selected(self, selected):
        pass

    def row_changed(self, current):
        node = current.internalPointer()
        if node.get_type_info() == 'dir':
            return
        version_list_model = VersionTreeModel(root=Version(entity=node.entity),
                                              shoppingCart=self.shoppingCart)
        self.version_tree_view.setModel(version_list_model)
        # self.version_tree_view.header().setResizeMode(0, QtGui.QHeaderView.Stretch)
        self.version_tree_view.header().resizeSection(0, 370)






if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    data = [ "a", "b" ]
    model = QtGui.QStringListModel(data)
    listView = QtGui.QListView()
    listView.show()
    listView.setModel(model)

    loadUi(os.path.join(path, 'views/ui/treeview.ui'), listView)
    sys.exit(app.exec_())