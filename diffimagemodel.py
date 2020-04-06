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


class diffwidget(QWidget):
    addtolistenddingSignal = QtCore.pyqtSignal()
    massageoutSignal = QtCore.pyqtSignal(str)
    settingchangeSignal = QtCore.pyqtSignal()

    def __init__(self, data: imageObject, settingdict: dict, statusBar,pixmap):
        super(diffwidget, self).__init__()
        self.data = data
        self.settingdict = settingdict
        self.statusBar = statusBar
        self.pixmap = []
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
        self.par1Slider.setMaximum(2000)  # 最大值
        self.par1Slider.setSingleStep(1)  # 步长
        self.par1Slider.setTickPosition(QSlider.TicksBelow)
        self.par1Slider.setTickInterval((self.par1Slider.maximum()-self.par1Slider.minimum())/10)
        self.par1Slider.valueChanged.connect(self.par1Sliderchanged)
        self.par1Slider.sliderReleased.connect(self.settingchange)
        self.par1Slider.setValue(8)
        self.par1label.setText("参数1:" + str(self.par1Slider.value()))

        self.par2label = QLabel()
        self.layout.addWidget(self.par2label, 2, 0, 1, 1)
        self.par2Slider = QSlider(Qt.Horizontal)
        self.layout.addWidget(self.par2Slider, 2, 1, 1, 5)
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
        self.displaymodebox.addItems(["正显", "反显"])
        self.displaymodebox.setCurrentIndex(0)
        self.displaymodebox.currentIndexChanged.connect(self.settingchange)
        self.layout.addWidget(self.displaymodebox, 1, 6, 1, 1)

        self.directionbox = QComboBox()
        self.directionbox.addItems(["横向(H)", "纵向(V)"])
        self.directionbox.setCurrentIndex(0)
        self.directionbox.currentIndexChanged.connect(self.settingchange)
        self.layout.addWidget(self.directionbox, 2, 6, 1, 1)

        self.makepar1imagebutton = QPushButton("生成图片")
        self.makepar1imagebutton.clicked.connect(self.makepar1imagebuttonclicked)
        self.layout.addWidget(self.makepar1imagebutton, 3, 0, 1, 1)
        self.addpar1tolistbutton = QPushButton("添加到列表")
        self.addpar1tolistbutton.clicked.connect(self.addtolistbuttonclicked)
        self.layout.addWidget(self.addpar1tolistbutton, 3, 1, 1, 1)
        self.addtostoretab4button = QPushButton("保存到图片库")
        self.addtostoretab4button.clicked.connect(self.addtostorebuttonclicked)
        self.layout.addWidget(self.addtostoretab4button, 3, 2, 1, 1)
        self.setLayout(self.layout)


    # todo: 参数1滑块改变
    def par1Sliderchanged(self, value):
        self.par1label.setText("参数1:" + str(value))

    # todo: 参数2滑块改变
    def par2Sliderchanged(self, value):
        self.par2label.setText("参数2:" + str(value))


    # todo:多阶光栅生成按钮点击事件 **********************
    def makepar1imagebuttonclicked(self):
        self.diffimagethread = diffimagethread(self.directionbox.currentIndex(),
                                                   self.displaymodebox.currentIndex(), self.par1Slider.value(),
                                                   self.par2Slider.value())
        self.massageoutSignal.emit("正在生成图片...")
        # self.diffimagethread.MessageSingle.connect(self.massageoutSignal.emit)
        self.diffimagethread.MessageSingle.connect(self.statusBar.showMessage)
        self.diffimagethread.EnddingSingle.connect(self.rasterimagethreadend)
        self.diffimagethread.start()

    # todo:（tab4）加载新生成图片
    def rasterimagethreadend(self, qimage, pixmap, direction):
        self.tempQImg = qimage
        self.pixmap = pixmap
        if direction == 0:
            self.direction2 = "H"
        else:
            self.direction2 = "V"
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
        filepath = self.settingdict["storedir"] + "/" + "衍射光"+mode+"_方向：" + self.direction2 + "_" + "参数1：" + str(self.par1Slider.value()) + "_参数2：" + str(self.par2Slider.value()) + ".png"
        if os.path.exists(filepath):
            self.massageoutSignal.emit("无需保存，图片库中已包含此图像!(衍射光"+mode+"_方向：" + self.direction2 + "_" + "参数1：" + str(self.par1Slider.value()) + "_参数2：" + str(self.par2Slider.value())+ ".png)")
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
            "已将图片保存到图片库！(衍射光"+mode+"_方向：" + self.direction2 + "_" + "参数1：" + str(self.par1Slider.value()) + "_参数2：" + str(self.par2Slider.value()) + ".png)")

    # todo：图片添加到列表
    def addtolistbuttonclicked(self):
        if (self.pixmap == []):
            self.massageoutSignal.emit("请先生成图片")
            return
        if (not os.path.exists(os.getcwd() + "/temp/")):
            os.makedirs(os.getcwd() + "/temp/")
        if self.displaymodebox.currentIndex()==0:
            mode="正显"
        else:
            mode="反显"
        filepath = os.getcwd() + "/temp/" + "衍射光"+mode+"_方向：" + self.direction2 + "_" + "参数1：" + str(self.par1Slider.value()) + "_参数2：" + str(self.par2Slider.value()) + ".png"
        try:
            self.tempQImg.save(filepath)
        except Exception as a:
            print(a)
        self.reading = True
        print("长度：", len(self.data.filelist))
        print("内数据id：", self.data)
        self.data.addfile(filepath)
        self.reading = False
        self.addtolistenddingSignal.emit()
        # self.readending()
        self.massageoutSignal.emit("已将图片添加到列表！")


    def settingchange(self):
        self.settingchangeSignal.emit()