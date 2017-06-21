import os, sys
from utils.pyside_dynamic import loadUi
from PySide import QtGui, QtCore

#from views.mainWindow import Ui_MainWindow

try:
    from PySide.QtUiTools import QUiLoader
except Exception as e:
    print e

path = os.path.dirname(os.path.abspath(__file__))
print path

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
         image: url(resources/icon-chevronright.svg);
 }
 QTreeView::branch:open:has-children:!has-siblings,
 QTreeView::branch:open:has-children:has-siblings  {
         border-image: none;
         image: url(resources/icon-chevrondown.svg);
 }
 QTreeView::branch:open

"""

class MainUI(QtGui.QMainWindow):
    """docstring for MainUI"""
    def __init__(self, parent = None):
        super(MainUI, self).__init__(parent)
        loadUi(os.path.join(path, 'ui/main.ui'), self)
        # self.setupUi(self)
        self.uiTree.setIconSize(QtCore.QSize(37, 23))
        self.filelHeader = self.uiTree.header()
        self.filelHeader.setDefaultSectionSize(175)
        self.uiTree.setStyleSheet(style)

    @QtCore.Slot()
    def mySlot(self):
        print "Hello"
        self.pushButton.setText("Click me again")

    def closeEvent(self, event):
        print "closeEvent"
        event.accept()
        # pass





# import os
# try:
#     from PySide import QtGui, QtCore
#     from PySide.QtUiTools import QUiLoader
# except Exception as e:
#     from PyQt4 import QtGui, QtCore
#     from PyQt4 import uic
#
# path = os.path.dirname(os.path.abspath(__file__))
#
# def loadUiWidget(uifilename, parent=None):
#     loader = QUiLoader()
#     uifile = QtCore.QFile(uifilename)
#     uifile.open(QtCore.QFile.ReadOnly)
#     ui = loader.load(uifile, parent)
#     uifile.close()
#     return ui
#
# try:
#     base, form = uic.loadUiType(os.path.join(path, 'ui/main.ui'))
# except:
#     print "Using QUiLoader"
#     base = QUiLoader().load(os.path.join(path, 'ui/main.ui'))