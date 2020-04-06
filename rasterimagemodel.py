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
from MyDemo import Label, editimageLabel,Lineedit,TableWidget
import time
from PyQt5.QtWebEngineWidgets import *



class rasterwidget(QWidget):
    addtolistenddingSignal = QtCore.pyqtSignal()
    massageoutSignal = QtCore.pyqtSignal(str)
    settingchangeSignal = QtCore.pyqtSignal()

    def __init__(self, data:imageObject,settingdict:dict,statusBar,pixmap):
        super(rasterwidget, self).__init__()
        self.data=data
        self.settingdict=settingdict
        self.statusBar=statusBar
        self.pixmap=pixmap

        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.lbshownewimage = QLabel()
        self.lbshownewimage.setStyleSheet("background-color:white;border:2px solid red")
        self.lbshownewimage.setFixedSize(192 * 4, 108 * 4)
        self.layout.addWidget(self.lbshownewimage, 0, 0, 1, 7)
        self.Multorderlabel = QLabel()
        self.layout.addWidget(self.Multorderlabel, 1, 0, 1, 1)
        self.MultorderSlider = QSlider(Qt.Horizontal)
        self.layout.addWidget(self.MultorderSlider, 1, 1, 1, 5)
        self.MultorderSlider.setMinimum(2)  # 最小值
        self.MultorderSlider.setMaximum(256)  # 最大值
        self.MultorderSlider.setSingleStep(1)  # 步长
        self.MultorderSlider.setTickPosition(QSlider.TicksBelow)
        self.MultorderSlider.valueChanged.connect(self.MultorderSliderchanged)
        self.MultorderSlider.sliderReleased.connect(self.settingchange)
        self.MultorderSlider.setValue(8)
        self.Multorderlabel.setText("光栅阶数:" + str(self.MultorderSlider.value()))

        self.pixelnwidelabel = QLabel()
        self.layout.addWidget(self.pixelnwidelabel, 2, 0, 1, 1)
        self.pixelnwideSlider = QSlider(Qt.Horizontal)
        self.layout.addWidget(self.pixelnwideSlider, 2, 1, 1, 5)
        self.pixelnwideSlider.setMinimum(1)  # 最小值
        self.pixelnwideSlider.setMaximum(100)  # 最大值
        self.pixelnwideSlider.setSingleStep(1)  # 步长
        self.pixelnwideSlider.setTickPosition(QSlider.TicksBelow)
        self.pixelnwideSlider.valueChanged.connect(self.pixelnwideSliderchanged)
        self.pixelnwideSlider.sliderReleased.connect(self.settingchange)
        self.pixelnwideSlider.setValue(2)
        self.pixelnwidelabel.setText("像素宽度:" + str(self.pixelnwideSlider.value()))

        self.imagechannelbox = QComboBox()
        self.imagechannelbox.addItems(["四通道", "三通道"])
        self.imagechannelbox.currentIndexChanged.connect(self.settingchange)
        self.imagechannelbox.setCurrentIndex(0)
        self.layout.addWidget(self.imagechannelbox, 1, 6, 1, 1)

        self.directionbox = QComboBox()
        self.directionbox.addItems(["横向(H)", "纵向(V)"])
        self.directionbox.setCurrentIndex(0)
        self.directionbox.currentIndexChanged.connect(self.settingchange)
        self.layout.addWidget(self.directionbox, 2, 6, 1, 1)

        self.makeimagebutton = QPushButton("生成图片")
        self.makeimagebutton.clicked.connect(self.makeimagebuttonclicked)
        self.layout.addWidget(self.makeimagebutton, 3, 0, 1, 1)
        self.addmultordertolistbutton = QPushButton("添加到列表")
        self.addmultordertolistbutton.clicked.connect(self.addmultordertolistbuttonclicked)
        self.layout.addWidget(self.addmultordertolistbutton, 3, 1, 1, 1)
        self.addtostorebutton = QPushButton("保存到图片库")
        self.addtostorebutton.clicked.connect(self.addtostoretabbuttonclicked)
        self.layout.addWidget(self.addtostorebutton, 3, 2, 1, 1)
        self.setLayout(self.layout)



    # todo: 光栅阶数滑块改变
    def MultorderSliderchanged(self, value):
        self.Multorderlabel.setText("光栅阶数:" + str(value))

    # todo: 像素宽度滑块改变
    def pixelnwideSliderchanged(self, value):
        self.pixelnwidelabel.setText("像素宽度:" + str(value))

    # todo:多阶光栅生成按钮点击事件 **********************
    def makeimagebuttonclicked(self):
        self.rasterimagethread = rasterimagethread(self.directionbox.currentIndex(),
                                                   self.imagechannelbox.currentIndex(), self.pixelnwideSlider.value(),
                                                   self.MultorderSlider.value())
        self.massageoutSignal.emit("正在生成图片...")
        self.rasterimagethread.MessageSingle.connect(self.statusBar.showMessage)
        self.rasterimagethread.EnddingSingle.connect(self.rasterimagethreadend)
        self.rasterimagethread.start()
        
        
    # todo:（tab4）加载新生成图片
    def rasterimagethreadend(self, qimage, pixmap,direction):
        self.newtempQImg2 = qimage
        self.newtemppixmap2 = pixmap
        if direction==0:
            self.direction2 = "H"
        else:
            self.direction2 = "V"
        self.massageoutSignal.emit("正在加载图片...")
        pixtemp = self.newtemppixmap2.scaled(self.lbshownewimage.width(), self.lbshownewimage.height())
        self.lbshownewimage.setPixmap(pixtemp)
        self.massageoutSignal.emit("图片生成成功！")

    # todo:多级光栅图片添加到图片库
    def addtostoretabbuttonclicked(self):
        if (self.newtemppixmap2 == []):
            self.massageoutSignal.emit("请先生成图片")
            return
        if (not os.path.exists(self.settingdict["storedir"])):
            os.makedirs(self.settingdict["storedir"])
        print(self.settingdict["storedir"] + "/" + "光栅图_方向：" + self.direction2 + "_" + "像素宽度：" + str(
            self.pixelnwideSlider.value()) + "_阶数：" + str(self.MultorderSlider.value()) + ".png")
        filepath = self.settingdict["storedir"] + "/" + "光栅图_方向：" + self.direction2 + "_" + "像素宽度：" + str(
            self.pixelnwideSlider.value()) + "_阶数：" + str(self.MultorderSlider.value()) + ".png"
        if os.path.exists(filepath):
            self.massageoutSignal.emit("无需保存，图片库中已包含此图像!(光栅图_方向：" + self.direction2 + "  像素宽度：" + str(
                self.pixelnwideSlider.value()) + "  阶数：" + str(self.MultorderSlider.value()) + ")")
            return
        try:

            self.newtempQImg2.save(filepath)

        except Exception as a:
            print(a)
        # self.reading = True
        # self.data.addfile(filepath)
        # self.reading = False
        # self.readending()
        self.massageoutSignal.emit(
            "已将图片保存到图片库！(光栅图_方向：" + self.direction2 + "  像素宽度：" + str(self.pixelnwideSlider.value()) + "  阶数：" + str(
                self.MultorderSlider.value()) + ")")


    # todo：图片添加到列表
    def addmultordertolistbuttonclicked(self):
        if (self.newtemppixmap2 == []):
            self.massageoutSignal.emit("请先生成图片")
            return
        if (not os.path.exists(os.getcwd() + "/temp/")):
            os.makedirs(os.getcwd() + "/temp/")
        print(os.getcwd() + "/temp/" + "光栅图_方向："+ self.direction2 + "_" + "像素宽度："+str(self.pixelnwideSlider.value())+"_阶数："+str(self.MultorderSlider.value()) + ".png")
        filepath = os.getcwd() + "/temp/" + "光栅图_方向："+ self.direction2 + "_" + "像素宽度："+str(self.pixelnwideSlider.value())+"_阶数："+str(self.MultorderSlider.value()) + ".png"
        try:
            self.newtempQImg2.save(filepath)
        except Exception as a:
            print(a)
        self.reading = True
        print("长度：",len(self.data.filelist))
        print("内数据id：",self.data)
        self.data.addfile(filepath)
        self.reading = False
        self.addtolistenddingSignal.emit()
        # self.readending()
        self.massageoutSignal.emit("已将图片添加到列表！")

    def settingchange(self):
        self.settingchangeSignal.emit()