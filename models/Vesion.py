from models.Entity import Entity
from utils.json2obj import json2obj


class Version(object):
    """docstring for Version"""
    def __init__(self, entity=None, version=None, parent=None):
        self.entity = entity
        self.version = version
        self.parent = parent
        self.children = []

        if parent is not None:
            parent.addChild(self)

        v1 = json2obj(
            '{"version":"v001.000","major":1,"minor":0,"path":"/Users/zeromax/MAVIS_WORKPLACE/projects/rampage/shots/test-0/v001.000","source":"/Users/zeromax/MAVIS_WORKPLACE/projects/rampage/shots/test-0","project":"rampage","isMajorVersion":true,"externalJobStatus":"NO_REQUEST","jobStatus":"NO_REQUEST","createdBy":"cdeng","createdAt":"2017-06-28T18:29:02.499Z","id":"5953f56e79a4ba139b815493","entityId":"5930a4e9eb93bb7b5efb9565","inputIds":[],"proxies":[]}')
        v2 = json2obj(
            '{"version":"v002.000","major":2,"minor":0,"path":"/Users/zeromax/MAVIS_WORKPLACE/projects/rampage/shots/test-0/v002.000","source":"/Users/zeromax/MAVIS_WORKPLACE/projects/rampage/shots/test-0","project":"rampage","isMajorVersion":true,"externalJobStatus":"NO_REQUEST","jobStatus":"NO_REQUEST","createdBy":"cdeng","createdAt":"2017-06-28T18:29:09.718Z","id":"5953f57579a4ba139b815495","entityId":"5930a4e9eb93bb7b5efb9565","inputIds":[],"proxies":[]}')

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

class Output(Version):
    """docstring for Output"""
    def __init__(self, parent=None):
        super(Output, self).__init__(parent)
