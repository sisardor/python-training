import os

import sys
from PySide import QtGui

from utils.pyside_dynamic import loadUi

path = os.path.dirname(os.path.abspath(__file__))
class TreeWidget(QtGui.QTreeView):
    """docstring for TreeWidget"""
    def __init__(self,  parent = None, *args):
        super(TreeWidget, self).__init__(parent)
        loadUi(os.path.join(path, 'ui/ui_tree.ui'), self)




if __name__ == '__main__':
    from utils.json2obj import json2obj
    from models.Node import Node
    from models.TreeModel import TreeModel
    app = QtGui.QApplication(sys.argv)

    treeWidget = TreeWidget()

    entity = json2obj(
        '{"category":"groups","path":"/mnt/x19/mavisdev/projects/geotest/sequence/afg_0025","name":"afg_0025","description":"AFG_0025 sequence","fileImportPath":"","isGlobal":false,"project":"geotest","fields":{"priority":"medium","status":"idle"},"createdBy":"trevor","createdAt":"2016-09-13T20:28:04.745Z","updatedAt":"2017-05-31T21:38:19.935Z","id":"57d861546fef3a0001c87954","type":"sequence","mediaIds":[],"isTest":false}')
    entity1 = json2obj(
        '{"category":"assets","path":"/mnt/x19/mavisdev/projects/geotest/globals/assets/wood_log","name":"wood_log","description":"a log that is wooden","fileImportPath":"","isGlobal":false,"project":"geotest","fields":{"priority":"medium","status":"review","grouping":"char","comp_status":"Ready","prod_status":"HIGH"},"createdBy":"dexplorer","createdAt":"2017-06-12T20:07:21.739Z","updatedAt":"2017-06-12T20:07:21.798Z","id":"593ef47973d9f40001cf898b","type":"assets","mediaIds":[],"isTest":false}')
    entity2 = json2obj(
        '{"category":"assets","path":"/mnt/x19/mavisdev/projects/geotest/sequence/afg_0025/shots/afg_0025_0020/plates/plate_afg-0025__0020","name":"plate_afg-0025__0020","description":"plate asse for afg_0025_0020","latest":"583dc9eebc843d0001905bde","fileImportPath":"/mnt/x1/mavisdev/client_imports/geotest/afg_0025_0020/AFG_0025_0020_bg01_v001_LIN.exr","isGlobal":true,"project":"geotest","fields":{"priority":"low","status":"approved","startFrame":10,"endFrame":100,"pxAspect":1,"colorspace":"linear","fileType":"exr","width":1920,"height":1080,"lut":"","ccc":"","head":8,"tail":8,"handle":8},"createdBy":"trevor","createdAt":"2016-11-29T18:31:59.429Z","updatedAt":"2017-05-23T21:17:43.390Z","id":"583dc99fbc843d0001905bd9","type":"plates","mediaIds":[],"parentId":"57d861546fef3a0001c87960","isTest":false}')
    entity3 = json2obj(
        '{"category":"tasks","path":"/mnt/x19/mavisdev/projects/geotest/globals/assets/wood_log/texture/tex_log","name":"tex_log","description":"texture the wood log","latest":"5941b18073d9f40001cf8a6c","fileImportPath":"","isGlobal":false,"project":"geotest","fields":{"priority":"urgent","status":"revised","grouping":"mtpg","comp_status":"In-Progress","prod_status":"HIGH"},"createdBy":"dexplorer","createdAt":"2017-06-12T20:08:10.814Z","updatedAt":"2017-06-14T21:58:24.772Z","id":"593ef4aa73d9f40001cf8992","type":"texture","mediaIds":[],"isTest":false}')
    entity4 = json2obj(
        '{"category":"tasks","path":"/mnt/x19/mavisdev/projects/geotest/sequence/mdm_0202/shots/mdm_0202_0100/assets/tuktuka/model/tuktuk_model","name":"tuktuk_model","description":"published plate 6310","latest":"58c6ffe6e925cc00016a6b58","fileImportPath":"","isGlobal":false,"project":"geotest","fields":{"priority":"high","status":"revised","grouping":"vehi","comp_status":"Waiting","prod_status":"MEDIUM"},"createdBy":"trevor","createdAt":"2017-04-13T22:08:33.983Z","updatedAt":"2017-04-18T20:35:28.557Z","id":"589b4f9dc599d10001375de9","type":"model","mediaIds":[],"parentId":"589b4f10c599d10001375de2","isTest":false}')

    rootNode = Node('Hips')
    childNode0 = Node('LeftPirateleg', entity, rootNode)
    childNode1 = Node('RightLeg', entity1, rootNode)
    childNode2 = Node('RightFoot', entity2, childNode1)
    childNode3 = Node('Xxxree', entity3, childNode2)
    childNode4 = Node('kldjskfds', entity4, childNode1)
    treeModel = TreeModel(rootNode)
    print treeModel
    print treeWidget
    treeWidget.show()

    treeWidget.uiTree.setModel(treeModel)

    sys.exit(app.exec_())