from PySide import QtGui, QtCore

BACKGROUND_COLOR = QtGui.QColor('#2c2f30')
BACKGROUND_COLOR_SELECT = QtGui.QColor('#575858')
CHILD_NODE_BG_COLOR = QtGui.QColor('#1d2022')
BORDER_COLOR_FOR_DELEGATE = "#3e4041"
THUMB_WIDTH = 70
THUMB_HIEGHT = 40
MARGIN = 5
CHECKBOX_WIDTH = 25
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
        painter.drawLine(option.rect.topRight(), option.rect.bottomRight())
        painter.drawLine(QtCore.QPoint(0, option.rect.bottom()), option.rect.bottomRight())
        painter.restore()

    def drawThumbnail(self, painter, option, index, thumbnail):
        thumbnail_image = QtGui.QPixmap(thumbnail).scaled(THUMB_WIDTH, THUMB_HIEGHT)
        r = QtCore.QRect(option.rect.left() + MARGIN + CHECKBOX_WIDTH,
                         option.rect.top() + MARGIN,
                         THUMB_WIDTH, THUMB_HIEGHT)
        painter.drawPixmap(r, thumbnail_image)

    def drawText(self, painter, rect, index, text):
        painter.save()
        painter.setPen(FONT_COLOR)
        r = QtCore.QRect(rect.left() + THUMB_WIDTH + MARGIN + MARGIN + CHECKBOX_WIDTH,
                         rect.top(),
                         rect.width() - THUMB_WIDTH - MARGIN,
                         rect.height())
        painter.drawText(r, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft, text)
        node = index.internalPointer()
        if node.is_latest_version():
            self.drawBadge(painter, rect, text, r)

        painter.restore()

    def drawTextWithoutThumnail(self, painter, rect, text):
        painter.save()
        painter.setPen(FONT_COLOR)
        r = QtCore.QRect(rect.left() + MARGIN,
                         rect.top(),
                         rect.width() - MARGIN,
                         rect.height())
        painter.drawText(r, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft, text)
        painter.restore()

    def drawBadge(self, painter, rect, text, r):
        star_badge = QtGui.QPixmap(':/star-badge.svg')
        r = QtCore.QRect(r.x() + fm.width(text) + MARGIN + MARGIN,
                         rect.top() + (star_badge.height()/2),
                         20,
                         20)
        painter.drawPixmap(r, star_badge)
        pass

    def paint(self, painter, option, index):
        selected = False
        if option.state & QtGui.QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        if option.state & QtGui.QStyle.State_Selected:
            selected = True

        thumbnail = index.data(QtCore.Qt.UserRole)
        text = index.data(QtCore.Qt.DisplayRole)

        self.drawBackground(painter, option, index, selected)
        if index.column() == 0:
            self.drawThumbnail(painter, option, index, thumbnail)
            self.drawText(painter, option.rect, index, text)
        else:
            self.drawTextWithoutThumnail(painter, option.rect, text)

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
