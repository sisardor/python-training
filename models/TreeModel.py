from PySide import QtGui, QtCore, QtNetwork
import resources.icons
from Node import Node
import urllib

class TreeModel(QtCore.QAbstractItemModel):
	"""docstring for TreeModel"""
	def __init__(self, root, parent=None):
		super(TreeModel, self).__init__(parent)
		self.rootNode = root


	def rowCount(self, parent):
		if not parent.isValid():
			parentNode = self.rootNode
		else:
			parentNode = parent.internalPointer()

		return parentNode.childCount()

	def columnCount(self, parent):
		return 4

	def setColumnWidth(self, column, width):
		pass


	def data(self, index, role):

		# if role == QtCore.Qt.BackgroundRole:
		# 	print "BackgroundRole %s"%role

		if not index.isValid():
			return None
		node = index.internalPointer()


		if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
			if index.column() == 0:
				return node.entity.name
			elif index.column() == 1:
				return node.entity.type
			elif index.column() == 2:
				return node.entity.fields.status
			elif index.column() == 3:
				return node.entity.fields.priority
			else:
				return node.typeInfo()



		if role == QtCore.Qt.DecorationRole:
			if index.column() == 0:
				typeInfo = node.typeInfo()
				if typeInfo == "sequence":
				 	# url = 'http://10.0.0.146:8002/geotest/57d861566fef3a0001c879b1/580fdded7ad29f000132c694_med.jpg'
					# data = urllib.urlopen(url).read()
					# image = QtGui.QImage()
					# image.loadFromData(data)
					# return QtGui.QIcon(QtGui.QPixmap(image))
					return QtGui.QIcon(QtGui.QPixmap(":/thumbnail-missing.svg"))
				elif typeInfo == "assets":
					return QtGui.QIcon(QtGui.QPixmap(":/Light.jpg"))
				elif typeInfo == "Task":
					return QtGui.QIcon(QtGui.QPixmap(":/Transform.jpg"))
				elif typeInfo == "Camera":
					return QtGui.QIcon(QtGui.QPixmap(":/Camera.jpg"))
				else:
					url = 'http://10.0.0.146:8002/geotest/57ffe93aef8a9100011593ea/582a4918c9831f000149b0e3_sm.jpg'
					# download_url = QtCore.QUrl(url)
					# manager = QtNetwork.QNetworkAccessManager()
					# request = QtNetwork.QNetworkRequest(download_url)
					# reply = manager.get(request)
					# print reply


					# data = urllib.urlopen(url).read()
					# image = QtGui.QImage()
					# image.loadFromData(data)
					# return QtGui.QIcon(QtGui.QPixmap(image))
					return QtGui.QIcon(QtGui.QPixmap(":/thumbnail-missing.svg"))




	def getNode(self, index):
		if index.isValid():
			node = index.internalPointer()
			if node:
				return node
		return self.rootNode

	def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
		parentNode = self.getNode(parent)

		self.beginInsertRows(parent, position, position + rows -1)
		for row in range(rows):
			childCount = parentNode.childCount()
			childNode = Node("untitled" + str(childCount))
			success = parentNode.insertChild(position,childNode)
		self.endInsertRows()

		return success

	def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
		parentNode = self.getNode(parent)
		self.beginRemoveRows(parent, position, position + rows -1)
		for row in range(rows):
			success = parentNode.removeChild(position)

		self.endRemoveRows()
		return success

	def setData(self, index, value, role=QtCore.Qt.EditRole):
		if index.isValid():
			if role == QtCore.Qt.EditRole:
				node = index.internalPointer()
				node.setName(value)
				self.dataChanged.emit(index, index)
				return True
		return False

	def headerData(self, section, orientation, role):
		# if role == QtCore.Qt.DecorationRole:
		# 	print "QtCore.Qt.DecorationRole %s"%role

		if role == QtCore.Qt.SizeHintRole:
			if section == 0:
				return QtCore.QSize(350,25)
			else:
				return QtCore.QSize(100,25)

		if role == QtCore.Qt.DisplayRole:
			if section == 0:
				return "Name"
			elif section == 1:
				return "Type"
			elif section == 2:
				return "Status"
			elif section == 3:
				return "Priority"
			elif section == 4:
				return "Assignees"
			else:
				return "Type"

	def flags(self, index):
		return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

	def parent(self, index):
		node = self.getNode(index)
		parentNode = node.parentX()

		if parentNode == self.rootNode:
			return QtCore.QModelIndex()
		return self.createIndex(parentNode.row(), 0, parentNode)

	def index(self, row, column, parent):
		parentNode = self.getNode(parent)

		childItem = parentNode.child(row)

		if childItem:
			return self.createIndex(row, column, childItem)
		else:
			return QtCore.QModelIndex()
