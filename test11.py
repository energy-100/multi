import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from PyQt5 import QtCore
from imagefileclass import imageObject
import pickle
import os
import datetime
import math
import threading
import time
import numpy as np

wmax = 1920
hmax = 1080

# imagedata = np.zeros([wmax, hmax])
# class main():
class main(QMainWindow):
    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        par1=10
        par2=10
        par3=0.2

        par21=1
        par22=1000
        par23=10
        w=1920
        h=1920

        imagedata=np.zeros((w+1,h+1,1),dtype=int)
        i=0
        aa=[]
        for x in range(int(-(w/2)),int(w/2)):
            j=0
            for y in range(int(-h/2),int(h/2)):
                # if x==0 and y>0:
                #     color=0
                # elif x==0 and y<0:
                #     color = 0
                # elif x==0 and y==0:
                #     color = 0
                #
                # else:
                    # if(x>0 and y>0):
                    #     # print("1")
                    #     arctanyx=math.atan(y/x)
                    # elif x<0:
                    #     # print("2")
                    #     arctanyx = math.atan(y / x)+math.pi
                    # elif(x>0 and y<0):
                    #     # print("3")
                    #     arctanyx = math.atan(y / x) + math.pi*2
                arctanyx=math.atan2(y,x)
                    # color=(2*math.pi/par2)*x*math.sin(par3)
                # color=par1*arctanyx+(2*math.pi/par2)*x*math.sin(par3)
                color=(2*math.pi/par21)*(x**2+y**2)/(2*par22)
                # print("color1",color)
                color=color%(2*math.pi)
                # print(color/math.pi)
                color=int(round(color/(2*math.pi)*255))
                imagedata[i][j][0]=color
                j +=1
            i +=1
        imagedata=np.swapaxes(imagedata,0,1)
        imagedata=np.tile(imagedata, (1,1,3))
        imagedata = imagedata[0:h, :w, 0:3].copy()
        imagedata = imagedata.astype(np.uint8)
        height, width, bytesPerComponent = imagedata.shape
        bytesPerLine = bytesPerComponent * width  # 表示彩色图像每个像素占用3个（ndarray图像数组的第三维长度）字节的空间
        self.newtempQImg = QImage(imagedata, width, height, bytesPerLine, QImage.Format_RGB888)
        self.newtemppixmap = QPixmap(self.newtempQImg)
        # self.newtemppixmap = QPixmap(self.newtempQImg).scaled(960,960, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label=QLabel()
        self.label.setPixmap(self.newtemppixmap)
        self.label.show()


        # import matplotlib
        # matplotlib.use('TkAgg')
        # plt.plot(aa)
        # plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = main()
    # ui.show()
    sys.exit(app.exec_())
    # import matplotlib
    # matplotlib.use('TkAgg')
    # x=[]
    # for i in range(int(-1920 / 2), int(1920 / 2)):
    #     x.append(i)
    # plt.plot(x)
    # plt.show()



    #
    #
    # if direction == 0:
    #     perordercolorspan = math.floor(256 / self.ordernum)  # 每阶颜色跨度
    #     # copynum = math.ceil(wmax / float(self.line1wide + self.line2wide))
    #     periodunm = math.ceil(wmax / (self.pixelnwide * self.ordernum))  # 向上取整
    #     list12 = []
    #     lineper = []
    #     for order in range(self.ordernum):
    #         self.MessageSingle.emit("正在计算单周期内第" + str(order + 1) + "阶像素点")
    #         color = order * perordercolorspan
    #
    #         # lineper = np.array([])
    #         # for i in range(self.pixelnwide * hmax):
    #         #     self.MessageSingle.emit("正在计算单周期内第" + str(order + 1) + "阶的第"+str(i)+"个像素点")
    #         #     lineper = np.append(lineper, np.array([color,color,color,color]))
    #         # lineper = lineper.reshape(hmax, self.pixelnwide, 4)
    #
    #         # 速度优化版本
    #         if order == 0:
    #             lineper = np.full((hmax, self.pixelnwide, 4), color)
    #             list12 = lineper
    #         else:
    #             lineper = np.full_like(lineper, color)
    #             list12 = np.hstack((list12, lineper))
    #     list12 = list12.astype(np.uint8)
    #     self.MessageSingle.emit("正在进行周期复制")
    #     imagedata = np.tile(list12, (1, periodunm, 1))
    #     imagedata = imagedata[:, 0:1920, 0:3].copy()
    #     print(imagedata.shape)
    # elif direction == 1:
    #     perordercolorspan = math.floor(256 / self.ordernum)  # 每阶颜色跨度
    #     # copynum = math.ceil(wmax / float(self.line1wide + self.line2wide))
    #     periodunm = math.ceil(hmax / (self.pixelnwide * self.ordernum))  # 向上取整
    #     list12 = []
    #     lineper = []
    #     for order in range(self.ordernum):
    #         self.MessageSingle.emit("正在计算单周期内第" + str(order + 1) + "阶像素点")
    #         color = order * perordercolorspan
    #
    #         # lineper = np.array([])
    #         # for i in range(self.pixelnwide * hmax):
    #         #     self.MessageSingle.emit("正在计算单周期内第" + str(order + 1) + "阶的第"+str(i)+"个像素点")
    #         #     lineper = np.append(lineper, np.array([color,color,color,color]))
    #         # lineper = lineper.reshape(hmax, self.pixelnwide, 4)
    #
    #         # 速度优化版本
    #         if order == 0:
    #             lineper = np.full((self.pixelnwide, wmax, 4), color)
    #             list12 = lineper
    #         else:
    #             lineper = np.full_like(lineper, color)
    #             print(list12.shape, lineper.shape)
    #             list12 = np.vstack((list12, lineper))
    #
    #     list12 = list12.astype(np.uint8)
    #     # self.MessageSingle.emit("正在进行周期复制")
    #     imagedata = np.tile(list12, (periodunm, 1, 1))
    #     imagedata = imagedata[0:hmax, 0:wmax, 0:3].copy()
    #
    # print(imagedata.shape)
    # height, width, bytesPerComponent = imagedata.shape
    # bytesPerLine = bytesPerComponent * width  # 表示彩色图像每个像素占用3个（ndarray图像数组的第三维长度）字节的空间
    # newtempQImg = QImage(imagedata, width, height, bytesPerLine, QImage.Format_RGB888)
    # newtemppixmap = QPixmap(newtempQImg)