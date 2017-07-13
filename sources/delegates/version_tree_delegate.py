from PySide import QtGui, QtCore
from sources.constants import BORDER_COLOR_FOR_DELEGATE, THUMB_WIDTH, CHECKBOX_WIDTH, MARGIN, THUMB_HIEGHT, \
    LATEST_VERSION, ROW_HEIGHT

BACKGROUND_COLOR = QtGui.QColor('#2c2f30')
BACKGROUND_COLOR_SELECT = QtGui.QColor('#575858')
CHILD_NODE_BG_COLOR = QtGui.QColor('#1d2022')
FONT_COLOR = QtGui.QPen(QtGui.QColor('#AAAAAA'), 0.5, QtCore.Qt.SolidLine)
font = QtGui.QFont()
font.setFamily(font.defaultFamily())
fm = QtGui.QFontMetrics(font)


class VersionDelegate(QtGui.QStyledItemDelegate):
    BG_DEFAULT = QtGui.QBrush(BACKGROUND_COLOR)
    BG_SELECTED = QtGui.QBrush(BACKGROUND_COLOR_SELECT)
    CHILD_BG_SELECTED = QtGui.QBrush(CHILD_NODE_BG_COLOR)

    """docstring for VersionDelegate"""
    def __init__(self, parent=None):
        super(VersionDelegate, self).__init__(parent)

    def drawBackground(self, painter, option, index, selected):
        if selected:
            baseColor = self.BG_SELECTED
            childColor = self.BG_SELECTED
        else:
            baseColor = self.BG_DEFAULT
            childColor = self.CHILD_BG_SELECTED

        painter.save()
        # painter.fillRect(option.rect, baseColor)

        # paint borders right, bottom
        painter.setPen(QtGui.QPen(QtGui.QColor(BORDER_COLOR_FOR_DELEGATE), 1))
        if index.column() != 0:
            painter.drawLine(option.rect.topLeft(), option.rect.bottomLeft())
        painter.drawLine(QtCore.QPoint(0, option.rect.bottom()), option.rect.bottomRight())
        painter.restore()

    def drawThumbnail(self, painter, option, index, thumbnail):
        thumbnail_image = QtGui.QPixmap(thumbnail).scaled(THUMB_WIDTH, THUMB_HIEGHT)
        r = QtCore.QRect(option.rect.left() + MARGIN + CHECKBOX_WIDTH,
                         option.rect.top() + MARGIN,
                         THUMB_WIDTH, THUMB_HIEGHT)
        painter.drawPixmap(r, thumbnail_image)

    def drawTextWithThumb(self, painter, rect, text):
        painter.save()
        painter.setPen(FONT_COLOR)
        r = QtCore.QRect(rect.left() + THUMB_WIDTH + MARGIN + MARGIN + CHECKBOX_WIDTH,
                         rect.top(),
                         rect.width() - THUMB_WIDTH - MARGIN,
                         rect.height())
        painter.drawText(r, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft, text)
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

    def drawBadge(self, painter, option, is_latest_version):
        if not is_latest_version: return

        star_badge = QtGui.QPixmap(':/star-badge.svg')
        r = QtCore.QRect(option.rect.right() - MARGIN - star_badge.width(),
                         option.rect.top() + (star_badge.height()/2),
                         20,
                         20)
        painter.drawPixmap(r, star_badge)
        pass

    def paint(self, painter, option, index):
        selected = False
        if option.state & QtGui.QStyle.State_MouseOver:
            # print 'mouse over'
            pass

        if option.state & QtGui.QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
            selected = True

        thumbnail = index.data(QtCore.Qt.UserRole)
        text = index.data(QtCore.Qt.DisplayRole)
        is_latest_version = index.data(LATEST_VERSION)

        self.drawBackground(painter, option, index, selected)
        if index.column() == 0:
            self.drawBadge(painter, option, is_latest_version)
            self.drawThumbnail(painter, option, index, thumbnail)
            self.drawTextWithThumb(painter, option.rect, text)
        else:
            self.drawText(painter, option.rect, text)

        # paint checkbox
        if index.column() == 0:
            painter.save()
            checkbox_state = index.data(QtCore.Qt.CheckStateRole)
            checkboxstyle = QtGui.QStyleOptionButton()
            options = QtGui.QStyleOptionViewItemV4(option)

            self.initStyleOption(options, index)
            style = QtGui.QApplication.style() if options.widget is None else options.widget.style()
            middle = (option.rect.height()/2) - 10
            checkboxstyle.rect = QtCore.QRect(option.rect.x() + 2, option.rect.y() + middle, 20, 20)

            if checkbox_state == QtCore.Qt.Checked:
                checkboxstyle.state = QtGui.QStyle.State_On | QtGui.QStyle.State_Active | QtGui.QStyle.State_Enabled
            elif checkbox_state == QtCore.Qt.PartiallyChecked:
                checkboxstyle.state = QtGui.QStyle.State_NoChange | QtGui.QStyle.State_Active | QtGui.QStyle.State_Enabled
            else:
                checkboxstyle.state = QtGui.QStyle.State_Off | QtGui.QStyle.State_Enabled

            checkboxstyle.palette = QtGui.QPalette(QtCore.Qt.white)
            style.drawControl(QtGui.QStyle.CE_CheckBox, checkboxstyle, painter)

            painter.restore()

    def sizeHint(self, option, index):
        value = index.data(QtCore.Qt.SizeHintRole)

        if value and value.isValid():
            return QtCore.QSize(value)
        else:
            return QtCore.QSize(190, ROW_HEIGHT)

