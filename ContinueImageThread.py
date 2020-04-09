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
# from time import *
# import wiringpi2 as gpio
import numpy as np

import threading


# todo:读取文件线程
class showcontinuethread(QThread):
    EnddingSingle = QtCore.pyqtSignal()
    ProcessSingle = QtCore.pyqtSignal(float)
    MessageSingle = QtCore.pyqtSignal(str)
    def __init__(self, filelist:list,interval:int,lb:QLabel,lb3:QLabel,imagelist:QTableWidget,namelist:QTableWidget,lblabel:QLabel):
        self.filelist = filelist
        self.interval = interval
        self.lb = lb
        self.lb3 = lb3
        self.lblabel = lblabel
        self.imagelist=imagelist
        self.namelist=namelist
        self.running=True
        self.showimageindex=0
        super(showcontinuethread, self).__init__()
    def run(self):
        # while True:
        #     if not self.running:
        #         break
        #     else:
        #         # global changethread
        #         global timer
        #         # t1 = time.time()
        global t1
        t1=time.time()
        timer=threading.Timer(self.interval*0.001, self.updateimage)
        timer.start()
                # changethread=changeimagethread(self.showimageindex,self.filelist,self.interval,self.lb,self.lb3,self.lblabel,self.imagelist,self.namelist)
                # changethread.start()


                # self.showimageindex += 1
                # if self.showimageindex == len(self.filelist):
                #     self.showimageindex = 0
                # # self.updateimage()
                # time.sleep(self.interval*0.001)
                # t2 = time.time()
                # print(t2-t1)
                # gpio.delayMicroseconds(10)





    def updateimage(self):
        if not self.running:
            # self.lblabel.setText("(连续显示已结束！)当前图片：" + self.filelist[self.showimageindex]["filename"])
            return
        # global timer
        # t1 = time.time()
        timer = threading.Timer(self.interval * 0.001, self.updateimage)
        timer.start()
        # 更新辅屏
        self.lb3.setPixmap(self.filelist[self.showimageindex]["pix"])
        self.lb3.setCursor(Qt.BlankCursor)


        global t1
        temp=t1
        t1=time.time()
        print(t1-temp)

        # 更新预览图
        file = self.filelist[self.showimageindex]
        imageresize = file["pix"].scaled(file["width"] / 1920 * self.lb.width(),file["height"] / 1080 * self.lb.height(), Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.lb.setPixmap(imageresize)
        self.lb.setCursor(Qt.CrossCursor)


        # 更新imagelist
        self.imagelist.selectColumn(self.showimageindex)
        self.namelist.selectRow(self.showimageindex)
        self.MessageSingle.emit("正在显示第" + str(self.showimageindex+1)+"/" +str(len(self.filelist))+ "张图像（时间间隔："+str(self.interval)+"ms)-"+self.filelist[self.showimageindex]["filename"])
        self.lblabel.setText("正在显示第" + str(self.showimageindex+1)+"/" +str(len(self.filelist))+ "张图像（时间间隔："+str(self.interval)+"ms)-"+self.filelist[self.showimageindex]["filename"])
        self.showimageindex += 1
        if self.showimageindex==len(self.filelist):
             self.showimageindex=0
        # self.EnddingSingle.emit()
        # t2=time.time()
        # print(t2-t1)

    def stop(self):
        self.running=False
        self.lblabel.setText("(连续显示已结束！)当前图片："+self.filelist[self.showimageindex]["filename"])


class changeimagethread(QThread):
    EnddingSingle = QtCore.pyqtSignal()
    ProcessSingle = QtCore.pyqtSignal(float)
    MessageSingle = QtCore.pyqtSignal(str)
    def __init__(self, index:int,filelist:list,interval:int,lb:QLabel,lb3:QLabel,lblabel:QLabel,imagelist:QTableWidget,namelist:QTableWidget):
        self.filelist = filelist
        self.interval = interval
        self.lb = lb
        self.lb3 = lb3
        self.lblabel = lblabel
        self.imagelist=imagelist
        self.namelist=namelist
        self.running=True
        self.showimageindex=index
        super(changeimagethread, self).__init__()
    def run(self):
        file = self.filelist[self.showimageindex]
        imageresize = file["pix"].scaled(file["width"] / 1920 * self.lb.width(),
                                         file["height"] / 1080 * self.lb.height(), Qt.KeepAspectRatio,
                                         Qt.SmoothTransformation)
        # 更新预览图
        self.lb.setPixmap(imageresize)
        self.lb.setCursor(Qt.CrossCursor)
        # 更新辅屏
        self.lb3.setPixmap(file["pix"])
        self.lb3.setCursor(Qt.BlankCursor)
        # 更新imagelist
        self.imagelist.selectColumn(self.showimageindex)
        self.namelist.selectRow(self.showimageindex)
        self.MessageSingle.emit(
            "正在显示第" + str(self.showimageindex + 1) + "/" + str(len(self.filelist)) + "张图像（时间间隔：" + str(
                self.interval) + "ms)-" + self.filelist[self.showimageindex]["filename"])
        self.lblabel.setText("正在显示第" + str(self.showimageindex + 1) + "/" + str(len(self.filelist)) + "张图像（时间间隔：" + str(
            self.interval) + "ms)-" + self.filelist[self.showimageindex]["filename"])
        # self.EnddingSingle.emit()

    def stop(self):
        self.running = False
        self.lblabel.setText("(连续显示已结束！)当前图片：" + self.filelist[self.showimageindex]["filename"])
