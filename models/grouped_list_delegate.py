from PySide import QtGui, QtCore

GROUP_HEADER = QtCore.Qt.UserRole + 1
MARGIN = 5
BG_SELECTED = QtGui.QBrush(QtGui.QColor('#575858'))
FONT_COLOR = QtGui.QPen(QtGui.QColor('#AAAAAA'), 0.5, QtCore.Qt.SolidLine)

ROW_MARGIN = 5

class GroupedListDelegate(QtGui.QStyledItemDelegate):
    """docstring for GroupedListDelegate"""
    def __init__(self, parent=None):
        super(GroupedListDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        group_header = index.data(GROUP_HEADER)
        text = index.data(QtCore.Qt.DisplayRole)
        if group_header:
            # painter.drawText(option.rect, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft, group_header)

            if index.row() != 0:
                self.drawBackgroundWithMargin(painter, option, index, False)
                self.drawTextWithMargin(painter, option.rect, text)
            else:
                self.drawBackground(painter, option, index, False)
                self.drawText(painter, option.rect, text)


        else:
            QtGui.QStyledItemDelegate.paint(self, painter, option, index)


    def sizeHint(self, option, index):
        group_header = index.data(GROUP_HEADER)
        if group_header and index.row() != 0:
            return QtCore.QSize(100, 30)
        else:
            return QtCore.QSize(100, 25)

    def drawBackground(self, painter, option, index, selected):
        r = QtCore.QRect(ROW_MARGIN,
                         option.rect.top(),
                         option.rect.width() - ROW_MARGIN - ROW_MARGIN,
                         option.rect.height())
        painter.fillRect(r, BG_SELECTED)

    def drawBackgroundWithMargin(self, painter, option, index, selected):
        painter.save()
        r = QtCore.QRect(ROW_MARGIN,
                         option.rect.top() + 5,
                         option.rect.width() - ROW_MARGIN - ROW_MARGIN,
                         option.rect.height() - 5)

        painter.fillRect(r, BG_SELECTED)
        painter.restore()

    def drawText(self, painter, rect, text):
        painter.save()
        painter.setPen(FONT_COLOR)
        r = QtCore.QRect(ROW_MARGIN + MARGIN,
                         rect.top(),
                         rect.width() - MARGIN,
                         rect.height())
        painter.drawText(r, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft, text)
        painter.restore()

    def drawTextWithMargin(self, painter, rect, text):
        painter.save()
        painter.setPen(FONT_COLOR)
        r = QtCore.QRect(ROW_MARGIN + MARGIN,
                         rect.top() + 5,
                         rect.width() - MARGIN,
                         rect.height())
        painter.drawText(r, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft, text)
        painter.restore()
