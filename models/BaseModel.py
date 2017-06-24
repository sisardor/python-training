import time
from PySide import QtCore
import sys
import pprint

sys.path.append("/mnt/x19/mavisdev/mavis_scripts/pydraulx")
from connection import mavis as mavis

class BaseModel(object):
    """docstring for BaseModel"""
    def __init__(self, modelName=None, *args, **kwargs):
        # for name, value in kwargs.items():
        #     print('{0} = {1}'.format(name, value))
        self.modelName = modelName
        self.entities = []
        self.headers = {}
        self.conn = mavis.getMavis(accessToken='eU0wYfeZTlf8NsbMnvT960X6EzXYxuwwHCimGJiXuFZY0HJCh4RiDt339vK0a9Ei')

    def name(self):
        return self.modelName

    def getHeaders(self):
        return self.headers

    def getXtotalCount(self):
        return 300
        # return self.headers['x-total-count']

    def fetch(self, **filter):
        default_filter = {'include': 'activities'}
        default_filter.update(filter)

        query = {'filter': default_filter}
        response = self.conn.get('Entities', **query)
        self.entities = response['data']
        self.headers = response['headers']
        print('fetching...')
        return self.entities

    def __str__(self):
        return "Model name: " + self.modelName


class Entity(QtCore.QAbstractItemModel, BaseModel):
    """docstring for Entity"""
    def __init__(self, parent=None, *args, **kwargs):
        # super(Entity, self).__init__(parent)
        QtCore.QAbstractItemModel.__init__(self, parent)
        BaseModel.__init__(self, *args, **kwargs)


if __name__ == '__main__':
    entity = Entity(modelName='Entity', apiPath='Entities')
    print Entity.__mro__
    res = entity.fetch(skip=0, limit=12)
    print len(res)
    print entity.getXtotalCount()