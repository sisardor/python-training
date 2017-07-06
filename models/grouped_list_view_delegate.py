from PySide import QtGui


class GroupedListViewDelegate(QtGui.QStyledItemDelegate):
    """docstring for GroupedListViewDelegate"""
    def __init__(self, parent=None):
        super(GroupedListViewDelegate, self).__init__(parent)

