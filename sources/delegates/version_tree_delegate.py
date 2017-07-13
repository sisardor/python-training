from PySide import QtGui, QtCore
from PySide.QtGui import QColor, QPalette

from sources.constants import BORDER_COLOR_FOR_DELEGATE, THUMB_WIDTH, CHECKBOX_WIDTH, MARGIN, THUMB_HIEGHT, \
    LATEST_VERSION, ROW_HEIGHT, ROW_HEIGHT_VERSION

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

        # painter.save()
        # # painter.fillRect(option.rect, baseColor)
        #
        # # paint borders right, bottom
        #
        # painter.setPen(QtGui.QPen(QtGui.QColor(BORDER_COLOR_FOR_DELEGATE), 1))
        # if index.column() != 0:
        #     painter.drawLine(option.rect.topLeft(), option.rect.bottomLeft())
        # painter.drawLine(QtCore.QPoint(0, option.rect.bottom()), option.rect.bottomRight())
        # painter.restore()

    def draw_border(self, painter, option, index, item):
        # paint borders right, bottom
        painter.setPen(QtGui.QPen(QtGui.QColor(BORDER_COLOR_FOR_DELEGATE), 1))
        if index.column() != 0:
            painter.drawLine(option.rect.topLeft(), option.rect.bottomLeft())
        painter.drawLine(QtCore.QPoint(0, option.rect.bottom()), option.rect.bottomRight())

    def drawThumbnail(self, painter, option, thumbnail):
        if type(thumbnail) is QtGui.QPixmap:
            r = QtCore.QRect(option.rect.left() + CHECKBOX_WIDTH,
                             option.rect.top() + MARGIN,
                             thumbnail.width(), thumbnail.height())
            painter.drawPixmap(r, thumbnail)
            return r.right()
        elif type(thumbnail) is QtGui.QIcon:
            size = thumbnail.actualSize(QtCore.QSize(20, 20))
            r = QtCore.QRect(option.rect.left(),
                             option.rect.top() + (option.rect.height() - size.height())/2,
                             size.width(), size.height())
            thumbnail.paint(painter,r, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter )
            return r.right()
        return option.rect.x()

    def drawText(self, painter, option, pen_color, x_point, text):
        painter.setPen(pen_color)
        textrect = QtCore.QRect(x_point + MARGIN,
                                option.rect.top(),
                                option.rect.width(),
                                option.rect.height())
        painter.drawText(textrect, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft, text)

    def drawBadge(self, painter, option, is_latest_version):
        if not is_latest_version: return

        star_badge = QtGui.QPixmap(':/star-badge.svg')\
            .scaled(20, ROW_HEIGHT_VERSION - (MARGIN * 2), QtCore.Qt.KeepAspectRatio)
        r = QtCore.QRect(option.rect.right() - MARGIN - star_badge.width(),
                         option.rect.top() + (option.rect.height() - star_badge.height()) / 2,
                         20,
                         20)
        painter.drawPixmap(r, star_badge)
        pass

    def paint(self, painter, option, index):
        item = index.internalPointer()
        model = index.model()
        selected = False
        if option.state & QtGui.QStyle.State_MouseOver:
            # print 'mouse over'
            pass

        if option.state & QtGui.QStyle.State_Selected:
            pen_color = QColor('white')
            bg_color = option.palette.color(QPalette.Active, QPalette.Highlight)
        else:
            pen_color = model.data(index, QtCore.Qt.ForegroundRole).color()
            bg_color = model.data(index, QtCore.Qt.BackgroundRole)

        if (option.state & QtGui.QStyle.State_Selected) > 0 \
                and (option.state & QtGui.QStyle.State_Active) == 0:
            pen_color = QColor('black')
            bg_color = QtCore.Qt.lightGray

        if option.state & QtGui.QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
            selected = True

        thumbnail = index.data(QtCore.Qt.DecorationRole)
        text = index.data(QtCore.Qt.DisplayRole)
        is_latest_version = index.data(LATEST_VERSION)

        self.drawBackground(painter, option, index, selected)
        if index.column() == 0:
            self.drawBadge(painter, option, is_latest_version)
            x_point = self.drawThumbnail(painter, option, thumbnail)
            self.drawText(painter, option, pen_color, x_point, text)
        else:
            self.drawText(painter, option, pen_color, option.rect.x(), text)

        self.draw_border(painter, option, index, item)
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
            return QtCore.QSize(190, ROW_HEIGHT_VERSION)

