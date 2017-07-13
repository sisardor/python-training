from PySide import QtGui, QtCore

from sources.delegates.grouped_list_delegate import GroupedListDelegate


class OutputsTreeUI(QtGui.QTreeView):
    def __init__(self, model=None, parent=None):
        QtGui.QTreeView.__init__(self, parent)

        self.header().setStretchLastSection(True)
        self.setMinimumSize(QtCore.QSize(200, 0))
        self.setAnimated(True)
        self.setItemsExpandable(False)
        self.setItemDelegate(GroupedListDelegate())
        self.setRootIsDecorated(False)
        self.setModel(model)
        self.header().hide()
        self.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)

        QtCore.QObject.connect(model,
                               QtCore.SIGNAL("rowsInserted(QModelIndex, int, int)"),
                               self.row_inserted)

        self.setStyleSheet("""
            QTreeView QHeaderView::section,
            QTreeView {
                font-size:12px
                
            }
            QTreeView
            {
                selection-background-color: transparent;
            }

            QTreeView::branch {
                background-color: rgba(64, 64, 64, 0)!important;
            }
            QTreeView::branch:selected {
                background: none;
            }
            QTreeView {
                border: none;
            }

        """)

    def row_inserted(self, parent, start, end):
        self.expandAll()



