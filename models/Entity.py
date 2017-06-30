import copy
from models.api_provider import ApiProvider
from utils.bcolors import bcolors


class Entity(ApiProvider):
    """docstring for Node"""
    def __init__(self, projectName=None, entity=None, parent=None):
        super(Entity, self).__init__()
        self.projectName = projectName
        self.entity = entity
        self.children = []
        self.parent = parent
        self.xTotalCount = -1

        if parent is not None:
            parent.addChild(self)

        if self.parent is None and self.projectName is not None:
            pass
            # self._fetchChildren(id=self.projectName)

    def _hasMoreChildren(self):
        return self.childCount() < self.xTotalCount

    def _fetch(self, id, **filter):
        filter['$dependencyCount'] = True
        filter['order'] = 'orderNum ASC'
        filter['include'] = ['media']
        response = self._find_all(path='Entities/%s/children' % id, **filter)

        remainder_rows = self.xTotalCount - self.childCount()
        rows_to_fetch = min(25, remainder_rows)

        return response['data']

    def _fetchChildren(self, id, **filter):
        filter['$dependencyCount'] = True
        filter['order'] = 'orderNum ASC'
        filter['include'] = ['media']

        response = self._find_all(path='Entities/%s/children' % id, **filter)
        entities = response['data']
        if self.parent is None:
            self.xTotalCount = int(response['headers']['x-total-count'])

        child_count = self.childCount()
        for index, entity in enumerate(entities):
            # print child_count + index, entity
            self.insertChild(index, Entity("untitled", entity))



    def setDataSource(self, dataSourece):
        self.ds = dataSourece
        response = self.ds._findById(self.projectName)
        self.entity = response['data']
        # print 'setDataSource ' , self.entity

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
        child.parent = self


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

    def setFieldStatus(self, value, ds):
        entity = copy.deepcopy(self.entity)
        entity['fields']['status'] = value
        result = ds.save(entity)
        if result:
            self.entity = result
        else:
            print bcolors.FAIL + 'Error' + bcolors.ENDC
            raise

        # pprint.pprint(self.entity)

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

    def getThumbnail(self):
        if self.entity['media'] or hasattr(self.entity, 'media'):
            image = (item for item in self.entity['media'] if item["mediaType"] == 'thumb_small' or item["mediaType"] == 'thumb_big').next()
            return image['path']
        return False

    def log(self, tabLevel=-1):
        return '{name: %s}'%self.entity['name']

        # output = ""
        # tabLevel += 1
        # for i in range(tabLevel):
        #     output += '\t'
        #
        # output += "|------" + self.entity['name'] + '\n'
        #
        # for child in self.children:
        #     output += child.log(tabLevel)
        #
        # tabLevel -= 1
        # output += '\n'
        # return output

    def __repr__(self):
        return self.log()
