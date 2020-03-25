import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from imagefileclass import imageObject
import pickle
import os
import datetime
class readfilethread(QThread):
    EnddingSingle = QtCore.pyqtSignal()
    ProcessSingle = QtCore.pyqtSignal(float)
    MessageSingle = QtCore.pyqtSignal(str)
    def __init__(self, filepath:str,imageobject:imageObject):
        self.imageobject = imageobject
        self.filepath = filepath
        super(readfilethread, self).__init__()
    def run(self):
        temp=self.imageobject.addfile(self.filepath,self.imageobject)
        print("长度：",len(temp))
        self.EnddingSingle.emit()

class savehistorythread(QThread):
    EnddingSingle = QtCore.pyqtSignal()
    ProcessSingle = QtCore.pyqtSignal(float)
    MessageSingle = QtCore.pyqtSignal(str)
    def __init__(self, achepath:str,imageobject:imageObject,selectindex:int):
        self.imageobject=imageobject
        self.selectindex = selectindex
        self.achepath = achepath
        super(savehistorythread, self).__init__()
    def run(self):
        # 用于缓存的字典
        datalist=dict()
        datalist["pathlist"]=[item["alldir"] for item in self.imageobject.filelist]
        datalist["selectindex"]=self.selectindex
        datalist["exittime"]=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 保存缓存
        if (not os.path.exists(self.achepath)):
            os.makedirs(self.achepath)
        with open(self.achepath+"history.ache", "wb") as file:
            pickle.dump(datalist, file, True)
        self.EnddingSingle.emit()

class readhostorythread(QThread):
    EnddingSingle = QtCore.pyqtSignal(dict)
    ProcessSingle = QtCore.pyqtSignal(float)
    MessageSingle = QtCore.pyqtSignal(str)
    def __init__(self, achepath:str):
        self.achepath = achepath
        self.data=imageObject()
        super(readhostorythread, self).__init__()
    def run(self):
        # 读取缓存
        # datalist 为缓存字典
        f = open(self.achepath, 'rb')
        datalist = pickle.load(f)
        f.close()

        for filepath in datalist["pathlist"]:
            self.data.addfile(filepath,self.data)
        # print(self.data.filelist)

        # 传递给主函数的字典
        data = dict()
        data["data"]=self.data
        data["selectindex"]=datalist["selectindex"]
        data["exittime"]=datalist["exittime"]

        self.EnddingSingle.emit(data)





