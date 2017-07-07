from PySide import QtGui, QtCore
from PySide.QtGui import QColor, QStyle

from utils.detect_color import detectColor

BORDER_COLOR_FOR_DELEGATE = "#3e4041"


class ComboboxDelegate(QtGui.QStyledItemDelegate):
    """
    A delegate that places a fully functioning QComboBox in every
    cell of the column to which it's applied
    """
    def __init__(self, parent=None):
        super(ComboboxDelegate, self).__init__(parent)

    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        editor.setCurrentIndex(editor.findData(value))

    def createEditor(self, parent, option, index):
        field = index.model()._getEntityType('status')
        options = field['options']
        combo = QtGui.QComboBox(parent)
        for o in options:
            combo.addItem(o['name'], o['label'])

        return combo

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def paint(self, painter, option, index):
        painter.save()
        value = index.data(QtCore.Qt.DisplayRole)

        # set background color
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        field = index.model()._getEntityType('status')
        options = field['options']
        o = (item for item in options if item["name"] == value or item["name"] == value).next()
        background = o['color']
        if option.state & QStyle.State_Selected:
            painter.setBrush(QtGui.QBrush(QtCore.Qt.white))
            painter.setBrush(QtGui.QBrush(QColor(background)))
        else:
            painter.setBrush(QtGui.QBrush(QColor(background)))
        painter.drawRect(option.rect)

        # set borders
        painter.setPen(QtGui.QPen(QColor(BORDER_COLOR_FOR_DELEGATE), 1))
        painter.drawLine(option.rect.topRight(), option.rect.bottomRight())
        painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())

        # set text color
        text_color = detectColor(background)
        painter.setPen(QtGui.QPen(QColor(text_color)))
        painter.drawText(option.rect, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter, value)
        painter.restore()