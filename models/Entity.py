from BaseModel import DataSource


class Entity(object):
    """docstring for Node"""
    def __init__(self, projectName=None, entity=None, parent=None):
        super(Entity, self).__init__()
        self.projectName = projectName
        self.entity = entity
        self.children = []
        self.parent = parent
        self._xTotalCount = 0

        if parent is not None:
            parent.addChild(self)

    def setDataSource(self, dataSourece):
        self.ds = dataSourece
        response = self.ds._findById(self.projectName)
        self.entity = response['data']
        # print 'setDataSource ' , self.entity

    def fetchChildren(self, **filter):
        filter['$dependencyCount'] = True
        return self.ds.fetch(path='Entities/%s/children'%(self.projectName), **filter)

    def fetchChildrenX(self, id, **filter):
        filter['$dependencyCount'] = True
        return self.ds.fetch(path='Entities/%s/children'%(id), **filter)

    def getXTotalCount(self):
        headers = self.ds.getHeaders()
        if headers['x-total-count']:
            return int(headers['x-total-count'])
        else:
            raise

    def setMetaData(self, response):
        self.entity = response['data']
        pass

    def typeInfo(self):
        return self.entity['type']

    def addChild(self, child):
        self.children.append(child)

    def insertChild(self, position, child):
        if position < 0 or position > len(self.children):
            return False

        self.children.insert(position, child)
        child.parent = self
        return True

    def removeChild(self, position):
        if position < 0 or position > len(self.children):
            return False

        child = self.children.pop(position)
        child.parent = None
        return True

    def setProjectName(self, projectName):
        self.projectName = projectName

    def getProjectName(self):
        return self.projectName

    def child(self, row):
        return self.children[row]

    def hasChildren(self):
        return self.entity['$dependencyCount'] > 0

    def childCount(self):
        return len(self.children)

    def _parent(self):
        return self.parent

    def row(self):
        if self.parent is not None:
            return self.parent.children.index(self)

    def log(self, tabLevel=-1):
        output = ""
        tabLevel += 1
        for i in range(tabLevel):
            output += '\t'

        output += "|------" + self.projectName + '\n'

        for child in self.children:
            output += child.log(tabLevel)

        tabLevel -= 1
        output += '\n'
        return output

    def __repr__(self):
        return self.log()
