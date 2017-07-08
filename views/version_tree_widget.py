import os, sys
from PySide import QtGui, QtCore
from models.version_tree_delegate import VersionDelegate


class VersionTreeWidget(QtGui.QTreeView):
    def __init__(self, parent=None):
        QtGui.QTreeView.__init__(self, parent)
        self.header().setStretchLastSection(True)
        self.setMinimumSize(QtCore.QSize(700, 0))
        self.setAnimated(True)
        self.setItemDelegate(VersionDelegate())

        self.setStyleSheet("""
            QTreeView QHeaderView::section,
            QTreeView {
                font-family: Open Sans;
            }
        """)


if __name__ == '__main__':
    from utils.json2obj import json2obj
    from models.entity import Entity

    app = QtGui.QApplication(sys.argv)

    listWidget = VersionTreeWidget()

    entity = json2obj('{"version":"v001.000","major":1,"minor":0,"path":"/Users/zeromax/MAVIS_WORKPLACE/projects/rampage/shots/test-0/v001.000","source":"/Users/zeromax/MAVIS_WORKPLACE/projects/rampage/shots/test-0","project":"rampage","isMajorVersion":true,"externalJobStatus":"NO_REQUEST","jobStatus":"NO_REQUEST","createdBy":"cdeng","createdAt":"2017-06-28T18:29:02.499Z","id":"5953f56e79a4ba139b815493","entityId":"5930a4e9eb93bb7b5efb9565","inputIds":[],"proxies":[]}')
    entity1 = json2obj('{"version":"v002.000","major":2,"minor":0,"path":"/Users/zeromax/MAVIS_WORKPLACE/projects/rampage/shots/test-0/v002.000","source":"/Users/zeromax/MAVIS_WORKPLACE/projects/rampage/shots/test-0","project":"rampage","isMajorVersion":true,"externalJobStatus":"NO_REQUEST","jobStatus":"NO_REQUEST","createdBy":"cdeng","createdAt":"2017-06-28T18:29:09.718Z","id":"5953f57579a4ba139b815495","entityId":"5930a4e9eb93bb7b5efb9565","inputIds":[],"proxies":[]}')

    rootNode = Entity('Hips')
    childNode0 = Entity('LeftPirateleg', entity, rootNode)
    listWidget.show()

    sys.exit(app.exec_())