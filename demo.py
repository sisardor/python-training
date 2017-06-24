import sys
from PyQt4 import QtGui, QtCore
import numpy

class LazyTableModel(QtCore.QAbstractTableModel):
    
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.numRows=0    
        self.numColumns=0
        self._data=data    
    #__init__
    
    def rowCount(self, parent):
        """
        parent=QModelIndex
        """
        return self.numRows
    #rowCount    
    
    def columnCount(self, parent):
        """
        parent=QModelIndex
        """
        return self.numColumns
    #columnCount    
    
    def data(self, index, role=QtCore.Qt.DisplayRole):
        """
        index=QModelIndex
        """
        if not index.isValid():
            return QtCore.QVariant()
        
        if index.row()>=self.numRows or index.row()<0 or index.column()>=self.numColumns or index.column()<0:
            return QtCore.QVariant()
        
        if role==QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self._data[index.row(), index.column()])
        elif role==QtCore.Qt.BackgroundRole:
            return QtCore.QVariant(QtGui.qApp.palette().base())
            
        return QtCore.QVariant()
    #data
    
    def canFetchMore(self, index):
        """
        index=QModelIndex
        """
        if self.numRows<self._data.shape[0] or self.numColumns<self._data.shape[1]:
            return True
        else:
            return False
    #canFetchMore
    
    def fetchMore(self, index):
        """
        Index=QModelIndex
        """
        maxFetch=10     #maximum number of rows/columns to grab at a time.
        remainderRows=self._data.shape[0]-self.numRows
        rowsToFetch=min(maxFetch, remainderRows)

        print "numRows: %s \t rowsToFetch: %s\tremainderRows: %s"%(self.numRows, rowsToFetch, remainderRows)
        if rowsToFetch>0:
            self.beginInsertRows(QtCore.QModelIndex(), self.numRows, self.numRows+rowsToFetch-1)
            self.endInsertRows()
            self.numRows+=rowsToFetch
        
        remainderColumns=self._data.shape[1]-self.numColumns
        columnsToFetch=min(maxFetch, remainderColumns)
        if columnsToFetch>0:
            self.beginInsertColumns(QtCore.QModelIndex(), self.numColumns, self.numColumns+columnsToFetch-1)
            self.endInsertColumns()
            self.numColumns+=columnsToFetch

        self.emit(QtCore.SIGNAL("numberPopulated"), rowsToFetch, columnsToFetch)
    #fetchMore
#LazyTableModel

class Window(QtGui.QWidget):
    
    def __init__(self, data, parent=None):
        """
        Data is any 2-d numpy array
        """
        QtGui.QWidget.__init__(self, parent)
        
        self.model = LazyTableModel(data, parent=self)
        
        view=QtGui.QTableView()
        view.setModel(self.model)
        
        self.logViewer=QtGui.QTextBrowser()
        self.logViewer.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred))
        
        self.connect(self.model, QtCore.SIGNAL("numberPopulated"), self.updateLog)
        
        layout=QtGui.QGridLayout()
        layout.addWidget(view, 0, 0, 1, 2)
        layout.addWidget(self.logViewer, 1, 0, 1, 2)
        
        self.setLayout(layout)
        
        self.setWindowTitle(self.tr("Fetch More Example - Table Edition"))
        self.resize(400, 600)
    #__init__
    
    def updateLog(self, rows, columns):
        self.logViewer.append(self.tr("%1 rows added.  %2 columns added").arg(rows).arg(columns))
    #updateLog
#Window

if __name__=='__main__':
    qApp=QtGui.QApplication(sys.argv)
    data=numpy.random.normal(size=(100, 1))
    fetchMoreWindow=Window(data)
    fetchMoreWindow.show()
    qApp.exec_()
