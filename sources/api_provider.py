import sys

sys.path.append("/mnt/x19/mavisdev/mavis_scripts/pydraulx")
from connection import mavis as mavis

class ApiProvider(object):
    conn = mavis.getMavis(accessToken='xyEKnvVCUE3AqUlhbPqOGp8ZqWdxCLWm5GSKn6MnxyU7O5jUTc7I2l4vXgh8JrZQ')

    def _find_all(self, path=None, **filter):
        query = {'filter': filter}
        try:
            response = self.conn.get(path, **query)
            return response
        except Exception as e:
            print '======= Exception ======='
            print e
            return False

    def _patch(self, path=None, data=None):
        return self.conn.patch(path, data)

    def _find_by_id(self):
        pass








# if __name__ == '__main__':
#     class Version(ApiProvider):
#         def __init__(self, parent=None, *args, **kwargs):
#             super(Version, self).__init__(*args, **kwargs)
#
#     a = ApiProvider()
#     b = ApiProvider()
#
#     vv = Version()
#     vv2 = Version()
#
#     print id(a), id(a.conn), a.conn
#     print id(b), id(b.conn), b.conn
#     vv.fetch()
#     vv2.fetch()