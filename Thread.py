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

# todo: 系统屏幕数量监听线程
class getwincountthread(QThread):
    wincountSingle = QtCore.pyqtSignal(int)
    def __init__(self):
        super(getwincountthread, self).__init__()

    def run(self):
        self.count=0
        while True:
            countcurrent=QApplication.desktop().screenCount()
            if countcurrent!=self.count:
                self.wincountSingle.emit(countcurrent)
                self.count=countcurrent

# todo:读取文件线程
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
        # print("长度：",len(temp))
        self.EnddingSingle.emit()

# todo:保存历史线程
class savehistorythread(QThread):
    EnddingSingle = QtCore.pyqtSignal()
    ProcessSingle = QtCore.pyqtSignal(float)
    MessageSingle = QtCore.pyqtSignal(str)
    def __init__(self, achepath:str,setting:dict,imageobject:imageObject,selectindex:int):
        self.imageobject=imageobject
        self.selectindex = selectindex
        self.achepath = achepath
        self.setting=setting
        super(savehistorythread, self).__init__()
    def run(self):
        #变换，将文件对象转化为文件路径
        self.setting["filelist"]=[item["alldir"] for item in self.setting["filelist"]]
        self.setting["t7tempimagelist"]=[item["alldir"] for item in self.setting["t7tempimagelist"]]

        # 保存缓存
        if (not os.path.exists(self.achepath)):
            os.makedirs(self.achepath)
        with open(self.achepath+"history.ache", "wb") as file:
            pickle.dump(self.setting, file, True)
        self.EnddingSingle.emit()

# todo:读取历史线程
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

        # 还原变换，将文件路径转化为文件对象
        for filepath in datalist["filelist"]:
            self.data.addfile(filepath,self.data)
        datalist["filelist"]=self.data.filelist
        self.data = imageObject()
        for filepath in datalist["t7tempimagelist"]:
            self.data.addfile(filepath,self.data)
        datalist["t7tempimagelist"]=self.data.filelist
        # 传递给主函数的字典
        # data = dict()
        # data["data"]=self.data
        # data["selectindex"]=datalist["selectindex"]
        # data["exittime"]=datalist["exittime"]

        self.EnddingSingle.emit(datalist)


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

 # todo:彩色生成线程
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

        # if self.direction == "V":
        #     copynum = math.ceil(1080 / float(self.line1wide + self.line2wide))  # 向上取整
        #     print("copynum", copynum)
        #     line1 = np.array([])
        #     for i in range(self.line1wide * wmax):
        #         #     line1 = np.append(line1, np.array(list(self.line1color.getRgb())))
        #         # line1 = line1.reshape(hmax, self.line1wide.value(), 4)
        #         line1 = np.append(line1, self.line1color)
        #     line1 = line1.reshape(hmax, self.line1wide, 4)
        #
        #     line2 = np.array([])
        #     for i in range(self.line2wide * hmax):
        #         #     line2 = np.append(line2, np.array(list(self.line2color.getRgb())))
        #         # line2 = line2.reshape(hmax, self.line2wide.value(), 4)
        #         line2 = np.append(line2, self.line2color)
        #     line2 = line2.reshape(hmax, self.line2wide, 4)
        #
        #     list12 = np.hstack((line1, line2))
        #     list12 = list12.astype(np.uint8)
        #     imagedata = np.tile(list12, (1, copynum, 1))
        #     imagedata = imagedata[:, 0:1920, 0:3].copy()
        #     print(imagedata.shape)
        #     height, width, bytesPerComponent = imagedata.shape
        #     bytesPerLine = bytesPerComponent * width  # 表示彩色图像每个像素占用3个（ndarray图像数组的第三维长度）字节的空间
        #     self.newtempQImg = QImage(imagedata, width, height, bytesPerLine, QImage.Format_RGB888)
        #     self.newtemppixmap = QPixmap(self.newtempQImg)
        # self.EnddingSingle.emit(self.newtempQImg,self.newtemppixmap)
# todo:彩色图生成线程
# class makemultorderimagethread(QThread):
#     EnddingSingle = QtCore.pyqtSignal(QImage, QPixmap,int)
#     ProcessSingle = QtCore.pyqtSignal(float)
#     MessageSingle = QtCore.pyqtSignal(str)
#
#     def __init__(self, direction:int,channel:int, pixelnwide: int, ordernum: int):
#         self.direction = direction
#         self.channel = channel
#         self.pixelnwide = pixelnwide
#         self.ordernum = ordernum
#         super(makemultorderimagethread, self).__init__()
#
#     def run(self):
#         wmax = 1920
#         hmax = 1080
#         # imagedata = np.zeros([wmax, hmax])
#         if self.direction == 0:
#             perordercolorspan=math.floor(256/self.ordernum)  #每阶颜色跨度
#             # copynum = math.ceil(wmax / float(self.line1wide + self.line2wide))
#             periodunm=math.ceil(wmax/(self.pixelnwide * self.ordernum)) # 向上取整
#             list12=[]
#             lineper=[]
#             for order in range(self.ordernum):
#                 self.MessageSingle.emit("正在计算单周期内第"+str(order+1)+"阶像素点")
#                 color=order * perordercolorspan
#
#                 # lineper = np.array([])
#                 # for i in range(self.pixelnwide * hmax):
#                 #     self.MessageSingle.emit("正在计算单周期内第" + str(order + 1) + "阶的第"+str(i)+"个像素点")
#                 #     lineper = np.append(lineper, np.array([color,color,color,color]))
#                 # lineper = lineper.reshape(hmax, self.pixelnwide, 4)
#
#                 # 速度优化版本
#                 if order==0:
#                     lineper = np.full((hmax, self.pixelnwide, 4), color)
#                     list12=lineper
#                 else:
#                     lineper = np.full_like(lineper, color)
#                     list12 = np.hstack((list12, lineper))
#             list12 = list12.astype(np.uint8)
#             self.MessageSingle.emit("正在进行周期复制")
#             imagedata = np.tile(list12, (1, periodunm, 1))
#             imagedata = imagedata[:, 0:1920, 0:3].copy()
#             print(imagedata.shape)
#         elif self.direction == 1:
#             perordercolorspan = math.floor(256 / self.ordernum)  # 每阶颜色跨度
#             # copynum = math.ceil(wmax / float(self.line1wide + self.line2wide))
#             periodunm = math.ceil(hmax / (self.pixelnwide * self.ordernum))  # 向上取整
#             list12 = []
#             lineper = []
#             for order in range(self.ordernum):
#                 self.MessageSingle.emit("正在计算单周期内第" + str(order + 1) + "阶像素点")
#                 color = order * perordercolorspan
#
#                 # lineper = np.array([])
#                 # for i in range(self.pixelnwide * hmax):
#                 #     self.MessageSingle.emit("正在计算单周期内第" + str(order + 1) + "阶的第"+str(i)+"个像素点")
#                 #     lineper = np.append(lineper, np.array([color,color,color,color]))
#                 # lineper = lineper.reshape(hmax, self.pixelnwide, 4)
#
#                 # 速度优化版本
#                 if order == 0:
#                     lineper = np.full((self.pixelnwide, wmax,  4), color)
#                     list12 = lineper
#                 else:
#                     lineper = np.full_like(lineper, color)
#                     print(list12.shape, lineper.shape)
#                     list12 = np.vstack((list12, lineper))
#
#             list12 = list12.astype(np.uint8)
#             self.MessageSingle.emit("正在进行周期复制")
#             imagedata = np.tile(list12, (periodunm,1, 1))
#             imagedata = imagedata[0:hmax, 0:wmax, 0:3].copy()
#
#         print(imagedata.shape)
#         height, width, bytesPerComponent = imagedata.shape
#         bytesPerLine = bytesPerComponent * width  # 表示彩色图像每个像素占用3个（ndarray图像数组的第三维长度）字节的空间
#         self.newtempQImg = QImage(imagedata, width, height, bytesPerLine, QImage.Format_RGB888)
#         self.newtemppixmap = QPixmap(self.newtempQImg)
#
#         self.EnddingSingle.emit(self.newtempQImg, self.newtemppixmap,self.direction)

# todo: 光栅图片生成线程

class rasterimagethread(QThread):
    EnddingSingle = QtCore.pyqtSignal(QImage, QPixmap,int)
    ProcessSingle = QtCore.pyqtSignal(float)
    MessageSingle = QtCore.pyqtSignal(str)
    progressBarSingle = QtCore.pyqtSignal(int)
    progressvisualBarSingle = QtCore.pyqtSignal(bool)

    def __init__(self, direction:int,channel:int, pixelnwide: int, ordernum: int):
        self.direction = direction
        self.channel = channel
        self.pixelnwide = pixelnwide
        self.ordernum = ordernum
        super(rasterimagethread, self).__init__()

    def run(self):
        self.progressvisualBarSingle.emit(True)
        wmax = 1920
        hmax = 1080
        # imagedata = np.zeros([wmax, hmax])
        if self.direction == 0:
            perordercolorspan=math.floor(256/self.ordernum)  #每阶颜色跨度
            # copynum = math.ceil(wmax / float(self.line1wide + self.line2wide))
            periodunm=math.ceil(wmax/(self.pixelnwide * self.ordernum)) # 向上取整
            list12=[]
            lineper=[]
            for order in range(self.ordernum):
                self.MessageSingle.emit("正在计算单周期内第"+str(order+1)+"阶像素点")
                color=order * perordercolorspan

                # lineper = np.array([])
                # for i in range(self.pixelnwide * hmax):
                #     self.MessageSingle.emit("正在计算单周期内第" + str(order + 1) + "阶的第"+str(i)+"个像素点")
                #     lineper = np.append(lineper, np.array([color,color,color,color]))
                # lineper = lineper.reshape(hmax, self.pixelnwide, 4)

                # 速度优化版本
                if order==0:
                    lineper = np.full((hmax, self.pixelnwide, 4), color)
                    list12=lineper
                else:
                    lineper = np.full_like(lineper, color)
                    list12 = np.hstack((list12, lineper))
            list12 = list12.astype(np.uint8)
            self.MessageSingle.emit("正在进行周期复制")
            imagedata = np.tile(list12, (1, periodunm, 1))
            imagedata = imagedata[:, 0:1920, 0:3].copy()
            print(imagedata.shape)
        elif self.direction == 1:
            perordercolorspan = math.floor(256 / self.ordernum)  # 每阶颜色跨度
            # copynum = math.ceil(wmax / float(self.line1wide + self.line2wide))
            periodunm = math.ceil(hmax / (self.pixelnwide * self.ordernum))  # 向上取整
            list12 = []
            lineper = []
            for order in range(self.ordernum):
                self.MessageSingle.emit("正在计算单周期内第" + str(order + 1) + "阶像素点")
                self.progressvisualBarSingle.emit(True)
                self.progressBarSingle.emit(int((order + 1) / self.ordernum*100))
                color = order * perordercolorspan

                # lineper = np.array([])
                # for i in range(self.pixelnwide * hmax):
                #     self.MessageSingle.emit("正在计算单周期内第" + str(order + 1) + "阶的第"+str(i)+"个像素点")
                #     lineper = np.append(lineper, np.array([color,color,color,color]))
                # lineper = lineper.reshape(hmax, self.pixelnwide, 4)

                # 速度优化版本
                if order == 0:
                    lineper = np.full((self.pixelnwide, wmax,  4), color)
                    list12 = lineper
                else:
                    lineper = np.full_like(lineper, color)
                    print(list12.shape, lineper.shape)
                    list12 = np.vstack((list12, lineper))

            list12 = list12.astype(np.uint8)
            self.MessageSingle.emit("正在进行周期复制")
            imagedata = np.tile(list12, (periodunm,1, 1))
            imagedata = imagedata[0:hmax, 0:wmax, 0:3].copy()

        print(imagedata.shape)
        height, width, bytesPerComponent = imagedata.shape
        bytesPerLine = bytesPerComponent * width  # 表示彩色图像每个像素占用3个（ndarray图像数组的第三维长度）字节的空间
        self.newtempQImg = QImage(imagedata, width, height, bytesPerLine, QImage.Format_RGB888)
        self.newtemppixmap = QPixmap(self.newtempQImg)
        self.EnddingSingle.emit(self.newtempQImg, self.newtemppixmap,self.direction)
        self.progressvisualBarSingle.emit(False)


class vorteximagethread(QThread):
    EnddingSingle = QtCore.pyqtSignal(QImage, QPixmap,int)
    ProcessSingle = QtCore.pyqtSignal(float)
    MessageSingle = QtCore.pyqtSignal(str)
    progressBarSingle = QtCore.pyqtSignal(int)
    progressvisualBarSingle = QtCore.pyqtSignal(bool)

    def __init__(self, direction:int,displaymode:int, par1: int, par2: int,par3:float):
        self.direction = direction
        self.displaymode = displaymode
        self.par1 = par1
        self.par2 = par2
        self.par3 = par3
        # self.par1 = 500
        # self.par2 = 1000
        # self.par3 = 0.2
        super(vorteximagethread, self).__init__()

    def run(self):
        self.progressvisualBarSingle.emit(True)
        w=1920
        h=1080
        if self.direction == 0:
            imagedata=np.zeros((w+1,h+1,1),dtype=int)
            i=0
            for x in range(int(-w/2),int(w/2)):
                j=0
                for y in range(int(-h/2),int(h/2)):
                    arctanyx=math.atan2(y,x)
                    color=self.par1*arctanyx+(2*math.pi/self.par2)*(x)*math.sin(self.par3)
                    color=color%(2*math.pi)
                    if self.displaymode == 0:
                        color = int(round(color / (2 * math.pi) * 255))
                    else:
                        color = int(255 - round(color / (2 * math.pi) * 255))
                    imagedata[i][j][0]=color
                    j +=1
                i +=1
                self.MessageSingle.emit("已完成"+str(i)+"/"+str(w)+"列")
                self.progressvisualBarSingle.emit(True)
                self.progressBarSingle.emit(int(i / w*100))
        else:
            imagedata = np.zeros((w + 1, h + 1, 1), dtype=int)
            i = 0
            for x in range(int(-w / 2), int(w / 2)):
                j = 0
                for y in range(int(-h / 2), int(h / 2)):
                    arctanyx = math.atan2(x, y)
                    color = self.par1 * arctanyx + (2 * math.pi / self.par2) * y * math.sin(self.par3)
                    color = color % (2 * math.pi)
                    if self.displaymode == 0:
                        color = int(round(color / (2 * math.pi) * 255))
                    else:
                        color = int(255 - round(color / (2 * math.pi) * 255))
                    imagedata[i][j][0] = color
                    j += 1
                i += 1
                self.MessageSingle.emit("已完成" + str(i) + "/" + str(w) + "列")
                self.progressvisualBarSingle.emit(True)
                self.progressBarSingle.emit(int(i / w*100))



        imagedata=np.swapaxes(imagedata,0,1)
        imagedata=np.tile(imagedata, (1,1,4))
        imagedata = imagedata[0:h, 0:w, 0:3].copy()
        imagedata = imagedata.astype(np.uint8)
        height, width, bytesPerComponent = imagedata.shape
        bytesPerLine = bytesPerComponent * width  # 表示彩色图像每个像素占用3个（ndarray图像数组的第三维长度）字节的空间
        self.newtempQImg = QImage(imagedata, width, height, bytesPerLine, QImage.Format_RGB888)
        self.newtemppixmap = QPixmap(self.newtempQImg)
        self.EnddingSingle.emit(self.newtempQImg, self.newtemppixmap,self.direction)
        self.progressvisualBarSingle.emit(False)


class diffimagethread(QThread):
    EnddingSingle = QtCore.pyqtSignal(QImage, QPixmap,int)
    ProcessSingle = QtCore.pyqtSignal(float)
    MessageSingle = QtCore.pyqtSignal(str)
    progressBarSingle = QtCore.pyqtSignal(int)
    progressvisualBarSingle = QtCore.pyqtSignal(bool)

    def __init__(self, direction:int,displaymode:int, par1: int, par2: int):
        self.direction = direction
        self.displaymode = displaymode
        self.par1 = par1
        self.par2 = par2
        super(diffimagethread, self).__init__()

    def run(self):
        self.progressvisualBarSingle.emit(True)
        w=1920
        h=1080
        if self.direction == 0:
            imagedata=np.zeros((w+1,h+1,1),dtype=int)
            i=0
            for x in range(int(-w/2),int(w/2)):
                j=0
                for y in range(int(-h/2),int(h/2)):
                    color=(2*math.pi/self.par1)*(x**2+y**2)/(2*self.par2)
                    color=color%(2*math.pi)
                    if self.displaymode == 0:
                        color = int(round(color / (2 * math.pi) * 255))
                    else:
                        color = int(255 - round(color / (2 * math.pi) * 255))
                    imagedata[i][j][0]=color
                    j +=1
                i +=1
                self.MessageSingle.emit("已完成"+str(i)+"/"+str(w)+"列")
                self.progressvisualBarSingle.emit(True)
                self.progressBarSingle.emit(int(i/w*100))
        else:
            imagedata = np.zeros((w + 1, h + 1, 1), dtype=int)
            i = 0
            for x in range(int(-w / 2), int(w / 2)):
                j = 0
                for y in range(int(-h / 2), int(h / 2)):
                    color=(2*math.pi/self.par1)*(x**2+y**2)/(2*self.par2)
                    color = color % (2 * math.pi)
                    if self.displaymode==0:
                        color = int(round(color / (2 * math.pi) * 255))
                    else:
                        color = int(255-round(color / (2 * math.pi) * 255))
                    imagedata[i][j][0] = color
                    j += 1
                i += 1
                self.MessageSingle.emit("已完成" + str(i) + "/" + str(w) + "列")
                self.progressvisualBarSingle.emit(True)
                self.progressBarSingle.emit(int(i / w*100))




        imagedata=np.swapaxes(imagedata,0,1)
        imagedata=np.tile(imagedata, (1,1,4))
        imagedata = imagedata[0:h, 0:w, 0:3].copy()
        imagedata = imagedata.astype(np.uint8)
        height, width, bytesPerComponent = imagedata.shape
        bytesPerLine = bytesPerComponent * width  # 表示彩色图像每个像素占用3个（ndarray图像数组的第三维长度）字节的空间
        self.newtempQImg = QImage(imagedata, width, height, bytesPerLine, QImage.Format_RGB888)
        self.newtemppixmap = QPixmap(self.newtempQImg)
        self.EnddingSingle.emit(self.newtempQImg, self.newtemppixmap,self.direction)
        self.progressvisualBarSingle.emit(False)