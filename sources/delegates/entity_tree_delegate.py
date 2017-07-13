from PySide import QtGui, QtCore
from PySide.QtGui import QColor, QPalette, QBrush, QStyledItemDelegate

from sources.constants import MARGIN, THUMB_WIDTH, THUMB_HIEGHT, BORDER_COLOR_FOR_DELEGATE
from sources.delegates.grouped_list_delegate import FONT_COLOR
from sources.entity import Entity


class EntityTreeDelegate(QtGui.QStyledItemDelegate):
    """docstring for EntityTreeDelate"""
    def __init__(self, view, parent=None):
        super(EntityTreeDelegate, self).__init__(parent)
        self.view = view

    def paint(self, painter, option, index):
        item = index.internalPointer()
        model = index.model()
        if isinstance(item, Entity):
            painter.save()

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

            # Draw background
            self.drawBackground(painter, option, bg_color, index.column() == 0)


            # Draw branch
            if item.hasChildren() and index.column() == 0:
                self.drawBrachIndicator(painter, option)

            # Draw thumbnail
            if index.column() == 0:
                thumbnail = index.data(QtCore.Qt.DecorationRole)
                x_point = self.drawThumbnail(painter, option, thumbnail)
            else:
                x_point = option.rect.x()

            # Draw text
            text = model.data(index, QtCore.Qt.DisplayRole)
            self.drawText(painter, option, pen_color, x_point, text)

            self.draw_border(painter, option, index)
            painter.restore()
        else:
            QStyledItemDelegate.paint(self, painter, option, index)

    def draw_border(self, painter, option, index):
        # paint borders right, bottom
        painter.setPen(QtGui.QPen(QtGui.QColor(BORDER_COLOR_FOR_DELEGATE), 1))
        if index.column() != 0:
            painter.drawLine(option.rect.topLeft(), option.rect.bottomLeft())
        painter.drawLine(QtCore.QPoint(0, option.rect.bottom()), option.rect.bottomRight())
        pass

    def drawThumbnail(self, painter, option, thumbnail):
        if type(thumbnail) is QtGui.QPixmap:
            r = QtCore.QRect(option.rect.left(),
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

    def drawBrachIndicator(self, painter, option):
        branch_option = QtGui.QStyleOption()
        if option.state & QtGui.QStyle.State_Open:
            icon = QtGui.QPixmap(':/icon-chevrondown.svg')
        else:
            icon = QtGui.QPixmap(':/icon-chevronright.svg')
        i = 17
        branch_option.rect = QtCore.QRect(option.rect.left() - 18,
                                          option.rect.top() + (option.rect.height() - i) / 2,
                                          i, i)
        branch_option.palette = option.palette
        branch_option.palette.setColor(QPalette.Highlight, QColor('#9ED764'))
        branch_option.state = QtGui.QStyle.State_Children
        painter.drawPixmap(branch_option.rect, icon)

    def drawText(self, painter, option, pen_color, x_point, text):
        painter.setPen(pen_color)
        textrect = QtCore.QRect(x_point + MARGIN,
                                option.rect.top(),
                                option.rect.width(),
                                option.rect.height())
        painter.drawText(textrect, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft, text)

    def drawBackground(self, painter, option, bg_color, is_first_column):
        width = option.rect.width()
        left_p = option.rect.left()
        if is_first_column:
            left_p = 0
            width = option.rect.width() + option.rect.left()

        r2 = QtCore.QRect(left_p,
                          option.rect.top(),
                          width,
                          option.rect.height())

        painter.fillRect(r2, QBrush(bg_color))


