from datetime import datetime
import datetime
import numpy as np
import cv2
import math
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QColorDialog
from PyQt5.QtCore import QRect, Qt
import pickle
import os
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
from PyQt5 import QtCore
import os
from PyQt5 import QtGui, QtWidgets
from os import startfile
import sys
from PyQt5.QtWidgets import *
from imagefileclass import imageObject
from PyQt5.QtCore import *
from Thread import *
from MyDemo import Label, editimageLabel, Lineedit, TableWidget
from ContinueImageThread import showcontinuethread
import time
from PyQt5.QtWebEngineWidgets import *


class displayimagelistwidget(QWidget):
    addtolistenddingSignal = QtCore.pyqtSignal()
    massageoutSignal = QtCore.pyqtSignal(str)
    settingchangeSignal = QtCore.pyqtSignal()

    def __init__(self, data: imageObject, settingdict: dict, statusBar,pixmap,list0,lb,lb3,lblabel):
        super(displayimagelistwidget, self).__init__()
        # self.setStyleSheet("background-color:yellow;border:2px solid red")
        # self.setContentsMargins(0, 0, 0, 0)
        # self.setSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum)
        self.showlist=[]
        self.data = data
        self.settingdict = settingdict
        self.statusBar = statusBar
        self.lb=lb
        self.lb3=lb3
        self.lblael=lblabel
        self.list0=list0
        self.showing=False
        # self.pixmap = []
        self.layout = QGridLayout()


        # self.layout = QVBoxLayout()
        # self.layout.setContentsMargins(0,0,0,0)
        # self.layout.setHorizontalSpacing(0)
        # self.layout.setVerticalSpacing(0)
        # self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        # self.layout.setSizeConstraint()
        self.imagelist=QTableWidget()
        self.imagelist.setFixedHeight(250)
        self.imagelist.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.imagelist.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.imagelist.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.imagelist.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.imagelist.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)  # 一行也可以滚动
        self.imagelist.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)  # 一列也可以滚动
        self.imagelist.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.imagelist.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.list0.horizontalHeader().setSectionsMovable(True)
        self.imagelist.clicked.connect(self.imagelistclicked)
        # self.layout.addWidget(self.imagelist)
        self.layout.addWidget(self.imagelist, 0, 0, 1, 8)
        self.namelist=QTableWidget()
        self.namelist.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.namelist.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.namelist.clicked.connect(self.namelistclicked)
        # self.layout.addWidget(self.namelist)
        self.layout.addWidget(self.namelist, 1, 0, 4, 4)

        self.timelabel = QLabel()
        self.layout.addWidget(self.timelabel, 1, 4, 1, 1)
        self.timeSlider = QSlider(Qt.Horizontal)
        self.layout.addWidget(self.timeSlider, 1, 5, 1, 3)
        self.timeSlider.setMinimum(0)  # 最小值
        self.timeSlider.setMaximum(1000)  # 最大值
        self.timeSlider.setSingleStep(1)  # 步长
        # self.timeSlider.setRange(10,20) #等价于上边方法
        self.timeSlider.setTickInterval((self.timeSlider.maximum()-self.timeSlider.minimum())/10)
        self.timeSlider.setTickPosition(QSlider.TicksBelow)
        self.timeSlider.valueChanged.connect(self.timeSliderchanged)
        self.timeSlider.sliderReleased.connect(self.timeSliderReleased)
        self.timeSlider.setValue(500)
        self.timelabel.setText("间隔时间:" + str(self.timeSlider.value())+"ms")

        self.addimagebutton = QPushButton("添加图片")
        self.addimagebutton.clicked.connect(self.addimagebuttonclicked)
        self.layout.addWidget(self.addimagebutton, 2, 4, 1, 1)
        self.setLayout(self.layout)


        self.addimagebutton = QPushButton("删除图片")
        self.addimagebutton.clicked.connect(self.deleteimagebuttonclicked)
        self.layout.addWidget(self.addimagebutton, 2, 5, 1, 1)

        self.clearimagebutton = QPushButton("清空图片")
        self.clearimagebutton.clicked.connect(self.clearimagebuttonclicked)
        self.layout.addWidget(self.clearimagebutton, 2, 6, 1, 1)

        self.stratbutton = QPushButton("开始播放图片")
        # self.stratbutton.setStyleSheet("color:green;font-family:Microsoft YaHei;font-size:12pt")
        self.stratbutton.clicked.connect(self.startbuttonclicked)
        self.layout.addWidget(self.stratbutton, 3, 4, 1, 1)

        self.stopbutton = QPushButton("停止")
        # self.stopbutton.setFont(QFont("Microsoft YaHei", 12))
        self.stopbutton.clicked.connect(self.stopshow)
        self.layout.addWidget(self.stopbutton, 3, 5, 1, 1)
        self.setLayout(self.layout)


    def addimagebuttonclicked(self):
        if self.list0.currentIndex().column() == -1:
            self.massageoutSignal.emit("请先选择要添加的图片！")
            return

        index = self.list0.currentIndex().column()
        self.showlist.append(self.data.filelist[index])
        self.update()
        self.massageoutSignal.emit("已添加图片-"+self.data.filelist[index]["filename"])
        self.settingchangeSignal.emit()

    def deleteimagebuttonclicked(self):
        index=self.imagelist.currentIndex().column()
        if index == -1:
            self.massageoutSignal.emit("请先选择要删除的图片！")
            return

        data=self.showlist.pop(index)
        self.update()
        self.massageoutSignal.emit("已删除图片-"+data["filename"])
        self.settingchangeSignal.emit()

    def clearimagebuttonclicked(self):
        self.showlist=[]
        self.update()
        self.massageoutSignal.emit("已清空所有图片")
        self.settingchangeSignal.emit()

    def update(self):
        self.namelist.clear()
        self.namelist.setColumnCount(1)
        self.namelist.setRowCount(len(self.showlist))
        for index, datapar in enumerate(self.showlist):
            self.namelist.setItem(index, 0, QTableWidgetItem(str(datapar["filename"])))


        self.imagelist.clear()
        self.imagelist.setColumnCount(len(self.showlist))
        self.imagelist.setRowCount(1)
        for i in range(len(self.showlist)):
            imagepix = Label()
            image = self.showlist[i]
            imagepix.setPixmap(image["pix"].scaled(image["width"] / image["height"] * 200, 200, Qt.KeepAspectRatio,
                                                   Qt.SmoothTransformation))
            # imagepix.resize(image["width"]/image["height"]*20,20)

            # print("比例：",self.data.filelist[i]["height"]/self.data.filelist[i]["width"])
            # imagepix.setCursor(Qt.CrossCursor)
            imagepix.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            # imagelist.append(imagepix)
            # imagepix.FilepathSignal.connect(self.filepathdrop)
            self.imagelist.setCellWidget(0, i, imagepix)
        self.imagelist.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.imagelist.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    def startbuttonclicked(self):
        # if self.showing:
        self.stopbutton.click()
        # self.showing=True
        self.showimagethread=showcontinuethread(self.showlist,self.timeSlider.value(),self.lb,self.lb3,self.imagelist,self.namelist,self.lblael)
        self.massageoutSignal.emit("正在启动...")
        self.showimagethread.MessageSingle.connect(self.statusBar.showMessage)
        self.stopbutton.clicked.connect(self.showimagethread.stop)
        self.showimagethread.start()

    def stopshow(self):
        self.massageoutSignal.emit("已停止！")






    # def stopbuttonclicked(self):

    def imagelistclicked(self):
        index = self.imagelist.currentIndex().column()
        if  index == -1:
            return
        self.namelist.selectRow(index)


    def namelistclicked(self):
        index = self.namelist.currentIndex().row()
        if  index == -1:
            return
        self.imagelist.selectColumn(index)



    # todo: 间隔时间滑块改变
    def timeSliderchanged(self, value):
        self.timelabel.setText("间隔时间:" + str(value)+"ms")

    # todo: 间隔时间滑块释放
    def timeSliderReleased(self):
        self.settingchangeSignal.emit()
