from PySide import QtGui, QtCore
from sources.delegates.combobox_delegate import ComboboxDelegate
from sources.delegates.entity_tree_delegate import EntityTreeDelegate


class EntityTreeUI(QtGui.QTreeView):
    """docstring for EntityTreeUI"""
    def __init__(self, model, parent=None):
        QtGui.QTreeView.__init__(self, parent)
        self.header().setStretchLastSection(True)
        self.setItemDelegateForColumn(2, ComboboxDelegate(self))
        self.setAnimated(True)
        self.setMinimumSize(QtCore.QSize(302, 0))
        self.setMaximumSize(QtCore.QSize(302, 1500))

        self.setItemDelegate(EntityTreeDelegate(self))

        self.setModel(model)
        self.setStyleSheet("""
            QTreeView QHeaderView::section,
            QTreeView {

                font-size:12px
            }
             # QTreeView::branch:has-children:!has-siblings:closed,
             # QTreeView::branch:closed:has-children:has-siblings {
             #         border-image: none;
             #         image: url(:/icon-chevronright.svg);
             # }
             # QTreeView::branch:open:has-children:!has-siblings,
             # QTreeView::branch:open:has-children:has-siblings  {
             #         border-image: none;
             #         image: url(:/icon-chevrondown.svg);
             # }
             QTreeView::item{border-color:#FFFF00;}
        """)

    def resizeEvent(self, event):
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 100)
        pass
