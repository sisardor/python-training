from models.api_provider import ApiProvider


class Version(ApiProvider):
    """docstring for Version"""
    def __init__(self, entity=None, version=None, parent=None, *args, **kwargs):
        super(Version, self).__init__()
        self.entity = entity
        self.version = version
        self.parent = parent
        self.children = []

        if parent is not None:
            parent.addChild(self)

        if self.entity is not None:
            self._getVersions(self.entity['id'])

    def hasOutputs(self):
        if self.version and self.version['outputs']:
            return True
        return False

    def getThumbnail(self):
        if self.version['proxies'] or hasattr(self.version, 'proxies'):
            image = (item for item in self.version['proxies'] if item["mediaType"] == 'thumb_small' or item["mediaType"] == 'thumb_big').next()
            return image['path']
        return False

    def getType(self):
        return 'version'

    def _getVersions(self, entityId=None):
        if entityId is None:
            return

        filter = { 'include': 'outputs'}
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
        child.parent = self

    def _parent(self):
        return self.parent

    def child(self, row):
        return self.children[row]

    def childCount(self):
        return len(self.children)

    def row(self):
        if self.parent is not None:
            return self.parent.children.index(self)

    def insertChild(self, position, child):
        if position < 0 or position > len(self.children):
            return False

        self.children.insert(position, child)
        child.parent = self
        return True


class Output(Version):
    """docstring for Output"""
    def __init__(self, output, parent):
        super(Output, self).__init__(version=output, parent=parent)


    def getType(self):
        return 'output'
