import sys
import traceback

from mainController import MainController
# from utils.borderlayout import BorderLayout
from utils.json2obj import json2obj
from sources.entity import Entity
from sources.tree_model import TreeModel
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
FONT_PATH = '/mnt/x19/mavisdev/mavis_scripts/pydraulx/static/Open_Sans/OpenSans-Regular.ttf'

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

        font_id = QtGui.QFontDatabase.addApplicationFont(FONT_PATH)
        if font_id is not -1:
            font_db = QtGui.QFontDatabase()
            self.font_styles = font_db.styles('Open Sans')
            self.font_families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
            for font_family in self.font_families:
                self.font = font_db.font(font_family, self.font_styles[0], 12)

        # QtGui.QApplication.setFont(self.font)

        self.ui = MainController()
        self.ui.show()

def run():

    # family = QtGui.QFontDatabase.applicationFontFamilies(id).at(0)
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
