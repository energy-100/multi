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
import time
from PyQt5.QtWebEngineWidgets import *


class rawvortexwidget(QWidget):
    addtolistenddingSignal = QtCore.pyqtSignal()
    massageoutSignal = QtCore.pyqtSignal(str)
    settingchangeSignal = QtCore.pyqtSignal()

    def __init__(self, data: imageObject, settingdict: dict, statusBar,pixmap,progressBar):
        super(rawvortexwidget, self).__init__()
        self.data = data
        self.settingdict = settingdict
        self.statusBar = statusBar
        self.pixmap = []
        self.progressBar = progressBar


        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.lbnewiamge = QLabel()
        self.lbnewiamge.setStyleSheet("background-color:white;border:2px solid red")
        self.lbnewiamge.setFixedSize(192 * 4, 108 * 4)
        self.layout.addWidget(self.lbnewiamge, 0, 0, 1, 7)
        self.par1label = QLabel()
        self.layout.addWidget(self.par1label, 1, 0, 1, 1)
        self.par1Slider = QSlider(Qt.Horizontal)
        self.layout.addWidget(self.par1Slider, 1, 1, 1, 5)
        self.par1Slider.setMinimum(0)  # 最小值
        self.par1Slider.setMaximum(128)  # 最大值
        self.par1Slider.setSingleStep(1)  # 步长
        self.par1Slider.setTickPosition(QSlider.TicksBelow)
        self.par1Slider.setTickInterval((self.par1Slider.maximum()-self.par1Slider.minimum())/10)
        self.par1Slider.valueChanged.connect(self.par1Sliderchanged)
        self.par1Slider.sliderReleased.connect(self.settingchange)
        self.par1Slider.setValue(4)
        self.par1label.setText("参数L:" + str(self.par1Slider.value()))

        self.par2label = QLabel()
        # self.layout.addWidget(self.par2label, 2, 0, 1, 1)
        self.par2Slider = QSlider(Qt.Horizontal)
        # self.layout.addWidget(self.par2Slider, 2, 1, 1, 5)
        self.par2Slider.setMinimum(0)  # 最小值
        self.par2Slider.setMaximum(2000)  # 最大值
        self.par2Slider.setSingleStep(1)  # 步长
        self.par2Slider.setTickInterval((self.par2Slider.maximum() - self.par2Slider.minimum()) / 10)
        self.par2Slider.setTickPosition(QSlider.TicksBelow)
        self.par2Slider.valueChanged.connect(self.par2Sliderchanged)
        self.par2Slider.sliderReleased.connect(self.settingchange)
        self.par2Slider.setValue(2)
        self.par2label.setText("参数2:" + str(self.par2Slider.value()))


        self.displaymodebox = QComboBox()
        self.displaymodebox.addItems(["反显", "正显"])
        self.displaymodebox.setCurrentIndex(0)
        self.displaymodebox.currentIndexChanged.connect(self.settingchange)
        self.layout.addWidget(self.displaymodebox, 1, 6, 1, 1)

        self.eagegrayvalue = QComboBox()
        self.eagegrayvalue.addItems(["边缘灰度最小", "边缘灰度最大"])
        self.eagegrayvalue.setCurrentIndex(0)
        self.eagegrayvalue.currentIndexChanged.connect(self.settingchange)
        self.layout.addWidget(self.eagegrayvalue, 2, 6, 1, 1)

        self.fullshow = QComboBox()
        self.fullshow.addItems(["全屏", "以圆形区域显示"])
        self.fullshow.setCurrentIndex(0)
        self.fullshow.currentIndexChanged.connect(self.settingchange)
        self.layout.addWidget(self.fullshow, 3, 6, 1, 1)


        self.makeimagebutton = QPushButton("生成图片")
        self.makeimagebutton.setIcon(QIcon("生成.png"))
        self.makeimagebutton.clicked.connect(self.makeimagebuttonclicked)
        self.layout.addWidget(self.makeimagebutton, 3, 0, 1, 1)
        self.addtolistbutton = QPushButton("添加到列表")
        self.addtolistbutton.setIcon(QIcon("加.png"))
        self.addtolistbutton.clicked.connect(self.addtolistbuttonclicked)
        self.layout.addWidget(self.addtolistbutton, 3, 1, 1, 1)
        self.addtostorebutton = QPushButton("保存到图片库")
        self.addtostorebutton.setIcon(QIcon("保存.png"))
        self.addtostorebutton.clicked.connect(self.addtostorebuttonclicked)
        self.layout.addWidget(self.addtostorebutton, 3, 2, 1, 1)
        self.setLayout(self.layout)


    # todo: 参数1滑块改变
    def par1Sliderchanged(self, value):
        self.par1label.setText("参数L:" + str(value))

    # todo: 参数2滑块改变
    def par2Sliderchanged(self, value):
        self.par2label.setText("参数2:" + str(value))


    # todo:多阶光栅生成按钮点击事件 **********************
    def makeimagebuttonclicked(self):
        self.rawvorteximageThread = rawvorteximagethread(self.eagegrayvalue.currentIndex(),
                                                   self.displaymodebox.currentIndex(), self.fullshow.currentIndex(),self.par1Slider.value(),
                                                   self.par2Slider.value())
        self.massageoutSignal.emit("正在生成图片...")
        # self.diffimagethread.MessageSingle.connect(self.massageoutSignal.emit)
        self.rawvorteximageThread.MessageSingle.connect(self.statusBar.showMessage)
        self.rawvorteximageThread.EnddingSingle.connect(self.rasterimagethreadend)
        self.rawvorteximageThread.progressBarSingle.connect(self.progressBar.setValue)
        self.rawvorteximageThread.progressvisualBarSingle.connect(self.progressBar.setVisible)
        self.rawvorteximageThread.start()

    # todo:（tab4）加载新生成图片
    def rasterimagethreadend(self, qimage, pixmap, eagegrayvalue,L,displaymode,fullshow):
        self.tempQImg = qimage
        self.pixmap = pixmap
        if eagegrayvalue == 0:
            self.eagegraystr = "MIN"
        else:
            self.eagegraystr = "MAX"
        if fullshow==0:
            self.fullshowstr="全屏"
        else:
            self.fullshowstr = "圆形"

        self.L=L
        self.displaymode=displaymode

        self.massageoutSignal.emit("正在加载图片...")
        pixtemp = self.pixmap.scaled(self.lbnewiamge.width(), self.lbnewiamge.height())
        self.lbnewiamge.setPixmap(pixtemp)
        self.massageoutSignal.emit("图片生成成功！")

    # todo:多级光栅图片添加到图片库
    def addtostorebuttonclicked(self):
        if (self.pixmap == []):
            self.massageoutSignal.emit("请先生成图片")
            return
        if (not os.path.exists(self.settingdict["storedir"])):
            os.makedirs(self.settingdict["storedir"])
        if self.displaymodebox.currentIndex()==0:
            mode="正显"
        else:
            mode="反显"
        filepath = self.settingdict["storedir"] + "/" + "未调制涡旋图_显示区域："+self.fullshowstr+"_显示模式："+mode+"_边缘灰度：" + self.eagegraystr + "_" + "参数L：" + str(self.L) + ".png"
        if os.path.exists(filepath):
            self.massageoutSignal.emit("无需保存，图片库中已包含此图像!(未调制涡旋图_显示区域:"+self.fullshowstr+"_显示模式："+mode+"_边缘灰度：" + self.eagegraystr + "_" + "参数L：" + str(self.L) + ".png)")
            return
        try:

            self.tempQImg.save(filepath)

        except Exception as a:
            print(a)
        # self.reading = True
        # self.data.addfile(filepath)
        # self.reading = False
        # self.readending()
        self.massageoutSignal.emit(
            "已将图片保存到图片库！(未调制涡旋图_显示区域："+self.fullshowstr+"_显示模式："+mode+"_边缘灰度：" + self.eagegraystr + "_" + "参数L：" + str(self.L) + ".png")

    # todo：图片添加到列表
    def addtolistbuttonclicked(self):
        if (self.pixmap == []):
            self.massageoutSignal.emit("请先生成图片")
            return
        if (not os.path.exists(os.getcwd() + "/temp/")):
            os.makedirs(os.getcwd() + "/temp/")
        if self.displaymodebox.currentIndex()==0:
            mode="反显"
        else:
            mode="正显"
        filepath = os.getcwd() + "/temp/" + "未调制涡旋图_显示区域："+self.fullshowstr+"_显示模式："+mode+"_边缘灰度：" + self.eagegraystr + "_" + "参数L：" + str(self.L) + ".png"
        try:
            self.tempQImg.save(filepath)
        except Exception as a:
            print(a)
        self.reading = True
        # print("长度：", len(self.data.filelist))
        # print("内数据id：", self.data)
        self.data.addfile(filepath)
        self.reading = False
        self.addtolistenddingSignal.emit()
        # self.readending()
        self.massageoutSignal.emit("已将图片添加到列表！")


    def settingchange(self):
        self.settingchangeSignal.emit()