import os

import sys
from PySide import QtGui

from utils.pyside_dynamic import loadUi

path = os.path.dirname(os.path.abspath(__file__))
class TreeWidget(QtGui.QTreeView):
    """docstring for TreeWidget"""
    def __init__(self, *args, **kwds):
        super(TreeWidget, self).__init__(*args, **kwds)
        # loadUi(os.path.join(path, 'ui/ui_tree.ui'), self)
        self.setStyleSheet("QTreeView {\n"
            "    background: #2c2f30;\n"
            "    color: #AAAAAA;\n"
            "}")
        self.resize(758, 595)
        print self







if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    treeWidget = TreeWidget()
    treeWidget.show()

    sys.exit(app.exec_())