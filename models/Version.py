from models.api_provider import ApiProvider


class Version(ApiProvider):
    """docstring for Version"""
    def __init__(self, entity=None, version=None, parent=None, *args, **kwargs):
        super(Version, self).__init__()
        self.entity = entity
        self.version = version
        self._parent = parent
        self.children = []
        self.checked = False

        if self._parent is not None:
            self._parent.addChild(self)

        if self.entity is not None:
            self._getVersions(self.entity['id'])

    def hasOutputs(self):
        if self.version and self.version['outputs']:
            return True
        return False

    def isLatestVersion(self):
        if self._parent and self._parent.entity:
            return self._parent.entity['latest'] == self.version['id']
        else:
            return False

    def getThumbnail(self):
        if self.version['proxies'] or hasattr(self.version, 'proxies'):
            image = (item for item in self.version['proxies'] if item["mediaType"] == 'thumb_small' or item["mediaType"] == 'thumb_big').next()
            return image['path']
        return False

    def get_display_name(self):
        return self.version['version']

    def getType(self):
        return 'version'

    def _getVersions(self, entityId=None):
        if entityId is None:
            return

        filter = { 'include': {'outputs': 'proxies'}, 'order': 'version DESC'}
        # filter = {'include': 'outputs', 'order': 'version DESC'}
        response = self._find_all(path='Entities/%s/versions'%(entityId), **filter)
        versions = response['data']
        for i, version in enumerate(versions):
            v_node = Version(version=version)
            if version['outputs']:
                print 'Found output'
                for j, output in enumerate(version['outputs']):
                    Output(output=output, parent=v_node)



            self.insertChild(i, v_node)

    def addChild(self, child):
        self.children.append(child)
        child._parent = self

    def parent(self):
        return self._parent

    def child(self, row):
        if row - 1 == len(self.children):
            return None
        else:
            return self.children[row]


    def childCount(self):
        return len(self.children)

    def row(self):
        if self._parent is not None:
            return self._parent.children.index(self)

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

    def isChecked(self):
        result = []
        for child in self.children:
            if child.isChecked():
                result.append(child.isChecked())
        if self.childCount() and self.childCount() == len(result):
            return 2 # QtCore.Qt.Checked
        elif len(result) == 0:
            return 0 # QtCore.Qt.Unchecked
        else:
            return 1 # QtCore.Qt.PartiallyChecked



    def setChecked(self, set):
        if self.childCount():
            for child in self.children:
                child.setChecked(set)
        self.checked = set

    def isEqual(self, item):
        return self.version['id'] == item.version['id']

    def log(self, tabLevel=-1):
        if self.version:
            return '{name: %s}'%self.version['version']
        return 'xxx'

    def __repr__(self):
        return self.log()

class Output(Version):
    """docstring for Output"""
    def __init__(self, output, parent=None):
        super(Output, self).__init__(version=output, parent=parent)

    def getType(self):
        return 'output'

    def isChecked(self):
        return self.checked

    def setChecked(self, set):
        self.checked = set

    def get_display_name(self):
        return self.version['type']

    def log(self, tabLevel=-1):
        return '{name: %s}'%self.version['type']

    def __repr__(self):
        return self.log()
