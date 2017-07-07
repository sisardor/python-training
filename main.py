import sys
import traceback

from mainController import MainController
# from utils.borderlayout import BorderLayout
from utils.json2obj import json2obj
from models.entity import Entity
from models.tree_model import TreeModel
STANDALONE_MODE=False

try:
    print "Importing PySide."
    from PySide import QtCore, QtGui, QtNetwork
    from PySide import __version__
except ImportError as e:
    print "Importing PySide failed."
    print e

try:
    import maya.mel as mel
    import maya.OpenMaya as OpenMaya
    import maya.OpenMayaUI as mui
    maya=True
except ImportError, e:
    print ("Cannot import Maya python modules.")
    STANDALONE_MODE=True

try:
    import shiboken
except:
    print("Cannot import shiboken.")
    pass

import resources.icons

import sys
sys.path.append("/mnt/x19/mavisdev/mavis_scripts/pydraulx")

from connection import mavis as mavis
from connection import pyside_LoginDialog

def getMayaWindow():
    '''
    Get the maya main window as a QMainWindow instance
    NB* we may not be running this from within Maya.
    '''
    try:
        if not STANDALONE_MODE:
            ptr = mui.MQtUtil.mainWindow()
            if ptr:
                return shiboken.wrapInstance(long(ptr), QtGui.QMainWindow)
            #changed from sip (pyQt) to shiboken (PySide)
            #return sip.wrapinstance(long(ptr), QtCore.QObject)
        else:
            return None
    except Exception, e:
        print e
        return None


class App(QtGui.QWidget):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        print "App"
        # self.conn = self.db_connect()
        self.ui = MainController()
        self.ui.show()

    def db_connect(self):
        '''
        connect to the database. if getMavis return None show login dialog
        '''
        try:
            # conn=mavis.Mavis(username=username, password=password)
            conn = mavis.getMavis()
            retry = False
            # dont like whiles....but
            while not conn:
                try:
                    # show the loging dialog
                    dialog = pyside_LoginDialog.LoginDialog(parent=self, retry=retry)
                    rval = dialog.exec_()
                    if rval == QtGui.QDialog.Rejected:
                        break

                    self.username = dialog.username
                    passwd = dialog.password
                    # print outcome so we know something is happening
                    print("username: %s password %s" % (self.username, passwd))
                    conn = mavis.getMavis(username=self.username, password=passwd)
                    # set user in the UI
                    self.ui.setUser(self.username)
                    retry = True
                    break
                except Exception, e:
                    print "invalid user/passwd"
                    print e
                    retry = True
                    continue
            return conn
        except Exception, e:
            print mavis.__file__
            print e
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
            traceback.print_stack()

def run():
    #get the current (Global) QApplication instance OR
    #create a new one if unavailable (standalone)
    # QtGui.QApplication.setStyle('motif') #"windows", "motif", "cde", "plastique", "windowsxp", or "macintosh".
    STANDALONE_MODE=False
    app = QtGui.QApplication.instance()

    if not app:
        app = QtGui.QApplication(sys.argv)
        STANDALONE_MODE=True
    mainWindowWidget=getMayaWindow()
    topLevelWidgets = QtGui.QApplication.topLevelWidgets()
    if  mainWindowWidget is None and topLevelWidgets:
        mainWindowWidget=[x for x in topLevelWidgets if isinstance(x, QtGui.QWidget) and x.objectName()=="MainWindow"][0]

    win = App(parent=mainWindowWidget)
    if STANDALONE_MODE:
        sys.exit(app.exec_())

if __name__ == "__main__":
    run()
