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
        self._parent = parent
        self._x_total_count = -1

        if self._parent is not None:
            self._parent.addChild(self)

    # ========================================================================
    # Public methods

    def parent(self):
        return self._parent

    def get_project_name(self):
        return self.projectName

    def child(self, row):
        return self.children[row]

    def hasChildren(self):
        return self.entity['$dependencyCount'] > 0

    def childCount(self):
        return len(self.children)

    def set_field_status(self, value, ds):
        entity = copy.deepcopy(self.entity)
        entity['fields']['status'] = value
        result = ds.save(entity)
        if result:
            self.entity = result
        else:
            print bcolors.FAIL + 'Error' + bcolors.ENDC
            raise

    def row(self):
        if self._parent is not None:
            return self._parent.children.index(self)

    def get_thumbnail(self):
        if self.entity['media'] or hasattr(self.entity, 'media'):
            image = (item for item in self.entity['media']
                     if item["mediaType"] == 'thumb_small'
                     or item["mediaType"] == 'thumb_big').next()
            return image['path']
        return False

    def get_type_info(self):
        return self.entity['type']

    def get_x_total_count(self):
        headers = self.ds.getHeaders()
        if headers['x-total-count']:
            return int(headers['x-total-count'])
        else:
            raise

    # ========================================================================
    # Internal class methods
    def addChild(self, child):
        self.children.append(child)
        child._parent = self


    def insertChild(self, position, child):
        if position < 0 or position > len(self.children):
            return False

        self.children.insert(position, child)
        child._parent = self
        return True

    def removeChild(self, position):
        if position < 0 or position > len(self.children):
            return False

        child = self.children.pop(position)
        child._parent = None
        return True

    # ========================================================================
    # Private methods

    def _has_more_children(self):
        return self.childCount() < self._x_total_count

    def _fetch(self, id, **filter):
        filter['$dependencyCount'] = True
        filter['order'] = 'orderNum ASC'
        filter['include'] = ['media']
        response = self._find_all(path='Entities/%s/children' % id, **filter)

        remainder_rows = self._x_total_count - self.childCount()
        rows_to_fetch = min(25, remainder_rows)

        return response['data']

    def _fetch_children(self, id, **filter):
        filter['$dependencyCount'] = True
        filter['order'] = 'orderNum ASC'
        filter['include'] = ['media']

        response = self._find_all(path='Entities/%s/children' % id, **filter)
        entities = response['data']
        if self._parent is None:
            self._x_total_count = int(response['headers']['x-total-count'])

        child_count = self.childCount()
        for index, entity in enumerate(entities):
            # print child_count + index, entity
            self.insertChild(index, Entity("untitled", entity))












    def log(self):
        return '{name: %s}'%self.entity['name']

    def __repr__(self):
        return self.log()
