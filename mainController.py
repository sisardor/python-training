import os
import sys
import resources.icons
from PySide import QtCore, QtGui
from utils.pyside_dynamic import loadUi
from views.treeWidget import TreeWidget
path = os.path.dirname(os.path.abspath(__file__))
class MainController(QtGui.QMainWindow):
    """docstring for MainController"""
    def __init__(self, parent=None):
        super(MainController, self).__init__(parent)
        loadUi(os.path.join(path, 'views/ui/mainwindow.ui'), self)
        self.uiTree = TreeWidget(self)



    @QtCore.Slot()
    def mySlot(self):
        print "Hello"
        self.pushButton.setText("Click me again")

    def closeEvent(self, event):
        print "closeEvent"
        # event.accept()
        pass



























style = """


QTreeView QHeaderView::section {
     background-color: #2c2f30;
     color: #AAAAAA;
     padding-left: 10px;
     border: 1px solid #3e4041;
     border-left: 0px;
     border-right: 0px;
     font-weight: 700;
 }
QTreeView {
    background: #2c2f30;
    color: #AAAAAA;
}

 QTreeView::branch {
    border-bottom: 1px solid #3e4041;
 }
 QTreeView::branch:selected {
    background-color: #575858 !important;
    color: #fff !important;
    fill: white;
 }
 QTreeView::item:selected {
    background-color: #575858 !important;
    color: #fff !important;
 }
 QTreeView::item {
    height: 35px;
    width: 250px;
    border-bottom: 1px solid #3e4041;
 }
 QTreeView::branch {
    width: 175px;
 }

 QTreeView::branch:has-children:!has-siblings:closed,
 QTreeView::branch:closed:has-children:has-siblings {
         border-image: none;
         image: url(:/icon-chevronright.svg)!important;
 }
 QTreeView::branch:open:has-children:!has-siblings,
 QTreeView::branch:open:has-children:has-siblings  {
         border-image: none;
         image: url(:/icon-chevrondown.svg)!important;
 }

"""


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    data = [ "a", "b" ]
    model = QtGui.QStringListModel(data)
    listView = QtGui.QListView()
    listView.show()
    listView.setModel(model)

    loadUi(os.path.join(path, 'views/ui/treeview.ui'), listView)
    sys.exit(app.exec_())