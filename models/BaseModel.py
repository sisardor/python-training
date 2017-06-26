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
        self.conn = mavis.getMavis(accessToken='xyEKnvVCUE3AqUlhbPqOGp8ZqWdxCLWm5GSKn6MnxyU7O5jUTc7I2l4vXgh8JrZQ')

    def name(self):
        return self.modelName

    def getHeaders(self):
        return self.headers

    def getXtotalCount(self):
        # return 300
        try:
            return int(self.headers['x-total-count'])
        except:
            return 300

    def fetch(self, path='Entities', **filter):
        default_filter = {'include': 'activities'}
        default_filter.update(filter)

        query = {'filter': default_filter}
        response = self.conn.get(path, **query)
        self.entities = response['data']
        self.headers = response['headers']
        # print('fetching...', query)
        return self.entities

    def _findById(self, id):
        response = self.conn.get('Entities/%s'%(id))
        return response

    def __str__(self):
        return "Model name: " + self.modelName


class DataSource(BaseModel):
    """docstring for Entity"""
    def __init__(self, parent=None, *args, **kwargs):
        BaseModel.__init__(self, *args, **kwargs)

    def getDataSource(self):
        return self

    # def fetch(self,*args, **filter):
    #     filter['$dependencyCount'] = True
    #     return super(DataSource, self).fetch(*args,**filter)



if __name__ == '__main__':
    entity = DataSource(modelName='Entity', apiPath='Entities')
    print DataSource.__mro__
    res = entity.fetch(skip=0, limit=12)
    print len(res)
    print entity.getXtotalCount()