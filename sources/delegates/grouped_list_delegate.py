from PySide import QtGui, QtCore

from sources.constants import GROUP_HEADER

MARGIN = 5
BG_SELECTED = QtGui.QBrush(QtGui.QColor('#575858'))
BG_SELECTED2 = QtGui.QBrush(QtGui.QColor('#D1ECB6'))
FONT_COLOR = QtGui.QPen(QtGui.QColor('#AAAAAA'), 0.5, QtCore.Qt.SolidLine)

ROW_MARGIN = 5

class GroupedListDelegate(QtGui.QStyledItemDelegate):
    """docstring for GroupedListDelegate"""
    def __init__(self, parent=None):
        super(GroupedListDelegate, self).__init__(parent)

    def editorEvent(self, event, model, option, index):
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            clickX = event.x()
            clickY = event.y()

            r = option.rect
            x = option.rect.left() + option.rect.width() - 27
            y = option.rect.top() + 5
            w = 15
            h = 15

            if clickX > x and clickX < x + w:
                if clickY > y and clickY < y + h:
                    # node = index.internalPointer()
                    # index.model().removeOuput(node.parent().version, node.version)
                    index.model().removeIndex(index)

        return False

    def paint(self, painter, option, index):
        # QtGui.QStyledItemDelegate.paint(self, painter, option, index)
        # return
        group_header = index.data(GROUP_HEADER)
        text = index.data(QtCore.Qt.DisplayRole)

        selected = False
        if option.state & QtGui.QStyle.State_Selected:
            selected = True

        if group_header:
            self.drawBackgroundWithMargin(painter, option, index, False)
            self.drawTextWithMargin(painter, option.rect, text)
            return
        else:
            self.drawBackground(painter, option, index, selected)
            self.drawText(painter, option.rect, text)


        # button:

        buttonstyle = QtGui.QStyleOptionButton()
        options = QtGui.QStyleOptionViewItemV4(option)

        self.initStyleOption(options, index)
        style = QtGui.QApplication.style() if options.widget is None else options.widget.style()
        x = option.rect.left() + option.rect.width() - 27
        y = option.rect.top() + 5
        w = 15
        h = 15

        buttonstyle.rect = QtCore.QRect(x,y,w,h)
        buttonstyle.text = 'x'
        buttonstyle.state = QtGui.QStyle.State_Enabled | QtGui.QStyle.State_Raised
        # buttonstyle.palette = QtGui.QPalette(QtCore.Qt.white)
        style.drawControl(QtGui.QStyle.CE_PushButton, buttonstyle, painter)



    def sizeHint(self, option, index):
        group_header = index.data(GROUP_HEADER)
        if group_header and index.row() != 0:
            return QtCore.QSize(100, 30)
        else:
            return QtCore.QSize(100, 25)

    def drawBackground(self, painter, option, index, selected):
        painter.save()
        if selected:
            base = QtGui.QBrush(QtGui.QColor('#9ED764'))
        else:
            base = QtGui.QBrush(QtGui.QColor('#D1ECB6'))

        r = QtCore.QRect(ROW_MARGIN,
                         option.rect.top(),
                         option.rect.width() + ROW_MARGIN + ROW_MARGIN,
                         option.rect.height())
        painter.fillRect(r, base)
        painter.restore()

    def drawBackgroundWithMargin(self, painter, option, index, selected):
        painter.save()
        r = QtCore.QRect(ROW_MARGIN,
                         option.rect.top() + ROW_MARGIN,
                         option.rect.width() - (ROW_MARGIN * 2),
                         option.rect.height() - ROW_MARGIN)

        painter.fillRect(r, BG_SELECTED)
        painter.restore()

    def drawText(self, painter, rect, text):
        painter.save()
        painter.setPen(FONT_COLOR)
        r = QtCore.QRect(rect.left() + MARGIN,
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
