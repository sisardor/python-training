from PySide import QtGui, QtCore
from PySide.QtGui import QColor, QPalette, QBrush, QStyledItemDelegate

from sources.constants import MARGIN
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
        if isinstance(item, Entity) and index.column() == 0:
            painter.save()
            options = QtGui.QStyleOptionViewItemV4(option)
            style = QtGui.QApplication.style() if options.widget is None else options.widget.style()
            # Draw background
            if option.state & QtGui.QStyle.State_Selected:
                bg_color = option.palette.color(QPalette.Active, QPalette.Highlight)
            else:
                bg_color = QColor('#2c2f30')#model.data(index, QtCore.Qt.BackgroundRole)
            r2 = QtCore.QRect(0,
                             option.rect.top(),
                             option.rect.width() + option.rect.left(),
                             option.rect.height())
            painter.fillRect(r2, QBrush(bg_color))

            i = 25  # hardcoded in qcommonstyle.cpp
            r = option.rect
            if item.hasChildren():
                # Draw branch
                branch_option = QtGui.QStyleOption()

                branch_option.rect = QtCore.QRect(r.left() - 20, r.top() + (r.height() - i) / 2, i, i)
                branch_option.palette = option.palette
                branch_option.palette.setColor(QPalette.Highlight, QColor('#9ED764'))
                branch_option.state = QtGui.QStyle.State_Children

                if option.state & QtGui.QStyle.State_Open:#self.view.isExpanded(index):
                    # branch_option.state |= QtGui.QStyle.State_Open
                    thumbnail_image = QtGui.QPixmap(':/icon-chevrondown.svg')
                else:
                    thumbnail_image = QtGui.QPixmap(':/icon-chevronright.svg')
                # style.drawPrimitive(QtGui.QStyle.PE_IndicatorBranch, branch_option, painter, self.view)
                # print branch_option
                painter.drawPixmap(branch_option.rect, thumbnail_image)

            # textrect = QtCore.QRect(r.left() + MARGIN, r.top()-10, r.width() - ((5 * i) / 2), r.height())
            text = model.data(index, QtCore.Qt.DisplayRole)#self.elidedText(option.fontMetrics, textrect.width(), QtCore.Qt.ElideMiddle,
                                  # model.data(index, QtCore.Qt.DisplayRole).toString())
            # painter.setFont(model.data(index, QtCore.Qt.FontRole))
            # painter.setPen(QtGui.QPen(model.data(index, QtCore.Qt.ForegroundRole)))
            # style.drawItemText(painter, textrect, QtCore.Qt.AlignLeft,
            #                    option.palette, self.view.isEnabled(), text)

            self.drawText(painter, option.rect, text)
            painter.restore()
        else:
            QStyledItemDelegate.paint(self, painter, option, index)

    def drawText(self, painter, rect, text):
        painter.save()
        painter.setPen(FONT_COLOR)
        r = QtCore.QRect(rect.left() + MARGIN,
                         rect.top(),
                         rect.width() - MARGIN,
                         rect.height())
        painter.drawText(r, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft, text)
        painter.restore()

    def paintX(self, painter, option, index):
        options = QtGui.QStyleOptionViewItemV4(option)
        style = QtGui.QApplication.style() if options.widget is None else options.widget.style()
        # view = QtGui.QTreeView(options.widget(option))



        if option.state & QtGui.QStyle.State_Selected:
            # QRect
            # branchRect(0, option.rect.top(), option.rect.left(), option.rect.height());
            # painter->setCompositionMode(QPainter::CompositionMode_Multiply);
            # painter->fillRect(branchRect, index.data(Qt::BackgroundColorRole).value < QColor > ());
            # painter->setCompositionMode(QPainter::CompositionMode_SourceOver);
            # self.drawBackground(painter,option,index, True)

            painter.save()
            r = QtCore.QRect(0,
                             option.rect.top(),
                             option.rect.left(),
                             option.rect.height())
            bk = QtGui.QBrush(QColor('#9ED764') , QtCore.Qt.SolidPattern )

            painter.fillRect(r, bk)
            painter.restore()


        print option.state &  QtGui.QStyle.State_Sibling
        if option.state & QtGui.QStyle.State_Children & QtGui.QStyle.State_Sibling & QtGui.QStyle.State_Item & QtGui.QStyle.State_Open :
            painter.save()
            branchOption = QtGui.QStyleOption()
            i = 9
            r = option.rect
            branchOption.rect = QtCore.QRect(r.left() + i/2, r.top() + (r.height() - i)/2, i,i)
            branchOption.palette = option.palette
            branchOption.state = QtGui.QStyle.State_Children
            if option.state & QtGui.QStyle.State_Open:
                branchOption.state |= QtGui.QStyle.State_Open

            style.drawPrimitive(QtGui.QStyle.PE_IndicatorBranch, branchOption, painter)
            painter.restore()
        # QtGui.QStyledItemDelegate.paint(self, painter, option, index)
        # pass

    def drawBackground(self, painter, option, index, selected):
        painter.save()
        if selected:
            base = QtGui.QBrush(QtGui.QColor('#9ED764'))
        else:
            base = QtGui.QBrush(QtGui.QColor('#D1ECB6'))
        r = QtCore.QRect(0,
                         option.rect.top(),
                         option.rect.width(),
                         option.rect.height())
        painter.fillRect(r, base)
        painter.restore()

