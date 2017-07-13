# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.12
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setEnabled(True)
        MainWindow.resize(1252, 671)
        MainWindow.setMinimumSize(QtCore.QSize(1250, 0))
        MainWindow.setMaximumSize(QtCore.QSize(2000, 16777215))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setStyleSheet(_fromUtf8(""))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.task_id_input = QtGui.QLineEdit(self.centralwidget)
        self.task_id_input.setGeometry(QtCore.QRect(20, 10, 261, 21))
        self.task_id_input.setObjectName(_fromUtf8("task_id_input"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(12, 42, 311, 571))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.layoutWest = QtGui.QHBoxLayout(self.widget)
        self.layoutWest.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.layoutWest.setMargin(0)
        self.layoutWest.setObjectName(_fromUtf8("layoutWest"))
        self.widget1 = QtGui.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(335, 12, 621, 601))
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.layoutMiddle = QtGui.QHBoxLayout(self.widget1)
        self.layoutMiddle.setMargin(0)
        self.layoutMiddle.setObjectName(_fromUtf8("layoutMiddle"))
        self.widget2 = QtGui.QWidget(self.centralwidget)
        self.widget2.setGeometry(QtCore.QRect(967, 12, 271, 601))
        self.widget2.setObjectName(_fromUtf8("widget2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget2)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1252, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))

