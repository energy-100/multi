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
import math
import threading
import time
import numpy as np
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


class DownThread:

    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, n):
        while self._running and n > 0:
            print('T-minus', n)
            n -= 1
            time.sleep(1)

class makeimage(QThread):
    EnddingSingle = QtCore.pyqtSignal(QImage,QPixmap)
    ProcessSingle = QtCore.pyqtSignal(float)
    MessageSingle = QtCore.pyqtSignal(str)
    def __init__(self,direction:str, line1wide: int,line2wide: int,line1color:np.ndarray,line2color:np.ndarray):
        self.direction = direction
        self.line1wide = line1wide
        self.line2wide = line2wide
        self.line1color = line1color
        self.line2color = line2color
        super(makeimage, self).__init__()

    def run(self):
        wmax = 1920
        hmax = 1080
        # imagedata = np.zeros([wmax, hmax])
        if self.direction == "H":
            copynum = math.ceil(1920 / float(self.line1wide + self.line2wide))  # 向上取整
            print("copynum", copynum)
            line1 = np.array([])
            for i in range(self.line1wide * hmax):
                #     line1 = np.append(line1, np.array(list(self.line1color.getRgb())))
                # line1 = line1.reshape(hmax, self.line1wide.value(), 4)
                line1 = np.append(line1, self.line1color)
            line1 = line1.reshape(hmax, self.line1wide, 4)

            line2 = np.array([])
            for i in range(self.line2wide * hmax):
                #     line2 = np.append(line2, np.array(list(self.line2color.getRgb())))
                # line2 = line2.reshape(hmax, self.line2wide.value(), 4)
                line2 = np.append(line2, self.line2color)
            line2 = line2.reshape(hmax, self.line2wide, 4)

            list12 = np.hstack((line1, line2))
            list12 = list12.astype(np.uint8)
            imagedata = np.tile(list12, (1, copynum, 1))
            imagedata = imagedata[:, 0:1920, 0:3].copy()
            print(imagedata.shape)
            height, width, bytesPerComponent = imagedata.shape
            bytesPerLine = bytesPerComponent * width  # 表示彩色图像每个像素占用3个（ndarray图像数组的第三维长度）字节的空间
            self.newtempQImg = QImage(imagedata, width, height, bytesPerLine, QImage.Format_RGB888)
            self.newtemppixmap = QPixmap(self.newtempQImg)

        self.EnddingSingle.emit(self.newtempQImg,self.newtemppixmap)

class makemultorderimagethread(QThread):
    EnddingSingle = QtCore.pyqtSignal(QImage, QPixmap)
    ProcessSingle = QtCore.pyqtSignal(float)
    MessageSingle = QtCore.pyqtSignal(str)

    def __init__(self, direction: str, pixelnwide: int, ordernum: int):
        self.direction = direction
        self.pixelnwide = pixelnwide
        self.ordernum = ordernum
        super(makemultorderimagethread, self).__init__()

    def run(self):
        wmax = 1920
        hmax = 1080
        # imagedata = np.zeros([wmax, hmax])
        if self.direction == "H":
            perordercolorspan=math.floor(256/self.ordernum)  #每阶颜色跨度
            # copynum = math.ceil(wmax / float(self.line1wide + self.line2wide))
            periodunm=math.ceil(wmax/(self.pixelnwide * self.ordernum)) # 向上取整
            list12=[]

            for order in range(self.ordernum):
                self.MessageSingle.emit("正在计算单周期内第"+str(order+1)+"阶像素点")
                color=order * perordercolorspan
                lineper = np.array([])
                for i in range(self.pixelnwide * hmax):
                    lineper = np.append(lineper, np.array([color,color,color,color]))
                lineper = lineper.reshape(hmax, self.pixelnwide, 4)
                if order==0:
                    list12=lineper
                else:
                    list12 = np.hstack((list12, lineper))
            list12 = list12.astype(np.uint8)
            self.MessageSingle.emit("正在进行周期复制")
            imagedata = np.tile(list12, (1, periodunm, 1))
            imagedata = imagedata[:, 0:1920, 0:3].copy()
            print(imagedata.shape)
            height, width, bytesPerComponent = imagedata.shape
            bytesPerLine = bytesPerComponent * width  # 表示彩色图像每个像素占用3个（ndarray图像数组的第三维长度）字节的空间
            self.newtempQImg = QImage(imagedata, width, height, bytesPerLine, QImage.Format_RGB888)
            self.newtemppixmap = QPixmap(self.newtempQImg)

        self.EnddingSingle.emit(self.newtempQImg, self.newtemppixmap)