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
import sys
from PyQt5.QtWidgets import *
from imagefileclass import imageObject
from PyQt5.QtCore import *
from Thread import *
from MyLabel import Label, editimageLabel
import time


# 主对话框
class main(QMainWindow):
    # 图片改变信号
    imagechangedSignal = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        # todo:软件配置
        self.setFont(QFont("Microsoft YaHei", 12))
        self.setWindowTitle('辅屏图像控制软件')
        self.setWindowIcon(QIcon('xyjk.png'))
        self.move(20, 10)

        # todo:全局变量
        self.filelist = []
        self.reading = False
        self.timestart = -1
        self.line1color = QColor(0, 0, 0)
        self.line2color = QColor(255, 255, 255)
        self.data = imageObject()
        self.newtemppixmap = []
        self.newtemppixmap2 = []
        self.direction = "H"
        if (os.path.exists(os.getcwd() + "/ache/storepath")):
            f = open(os.getcwd() + "/ache/storepath.ache", 'rb')
            path = pickle.load(f)
            f.close()
            self.storedir = path
        else:
            self.storedir = os.getcwd() + "/store/"

        # todo:获取屏幕信息
        desktop = QApplication.desktop()
        self.screen_count = desktop.screenCount()  # 屏幕数量
        print(self.screen_count)
        self.win1 = desktop.screenGeometry(0)  # 参数为显示屏索引，如果安装了两个显示屏，主显示屏索引为0，辅显示屏索引为1
        self.win2 = desktop.screenGeometry(1)  # 参数为显示屏索引，如果安装了两个显示屏，主显示屏索引为0，辅显示屏索引为1
        # available_rect = desktop.availableGeometry(0)  # 参数为显示屏索引，如果安装了两个显示屏，主显示屏索引为0，辅显示屏索引为1

        # todo:屏幕1Wigget
        self.widget = QWidget()
        self.widget.setGeometry(self.win1)

        # todo:主屏幕布局
        self.grid = QGridLayout()

        # todo:预览辅屏
        # self.lb = QWidget("请选择图片，或将图片文件拖拽至此！")
        # self.lb = Label("请选择图片，或将图片文件拖拽至此！")
        self.lb = Label()
        # self.lb.resize(192*5, 108*5)
        self.lb.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.lb.setStyleSheet("background-color:white;border:1px solid black")
        self.lb.MessageSignal.connect(self.statusBar().showMessage)
        self.lb.FilepathSignal.connect(self.filepathdrop)
        self.lb.setAcceptDrops(True)
        self.lb.setFixedSize(192 * 5, 108 * 5)

        # todo:预览图片
        # self.lb2 = Label("请选择图片，或将图片文件拖拽至此！")
        self.lb2 = editimageLabel()
        # self.lb.resize(192*5, 108*5)
        # self.lb2.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.lb2.setStyleSheet("background-color:white;border:1px solid black")
        self.lb2.MessageSignal.connect(self.statusBar().showMessage)
        self.lb2.FilepathSignal.connect(self.filepathdrop)
        self.lb2.setAcceptDrops(True)
        self.lb2.setFixedSize(192 * 5, 108 * 5)

        # self.grid.addWidget(self.lb,0,0,1,4)

        # todo:设置辅屏对象
        self.lb3 = Label()
        self.lb3.setWindowIcon(QIcon('display.png'))
        self.lb3.setWindowTitle('辅屏窗口')
        self.lb3.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.lb3.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus | Qt.WindowStaysOnTopHint)
        self.lb3.setCursor(Qt.BlankCursor)  # 设置鼠标隐藏
        if self.screen_count > 1:
            self.lb3.setGeometry(self.win2)
            self.lb3.show()
        # todo:说明文档
        self.instructions = QLabel("操作提示:\
                                 \n1.辅屏请设置为扩展模式\
                                 \n2.在图片编辑功能下，鼠标滚轮缩放，按住左键移动，单击右键还原\
                                 \n3.当图像尺寸小于窗口尺寸时，辅屏将居中显示图片\
                                 \n4.在图片编辑功能下，默认将图片填充至整个窗口（包括右键还原的图片），\
                                 \n   若要以原尺寸输出图片请再次在图片列表中点击图片")
        # self.instructions.adjustSize()
        self.instructions.setScaledContents(True)
        print("self.instructions.minimumSize()", self.instructions.size().width(), self.instructions.size().height())
        self.instructions.setFixedSize(900, 400)

        # self.instructions.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        # todo:图片绘制模块
        # ****************************************************
        self.tab3layout = QGridLayout()
        self.lbnewiamge = QLabel()
        self.lbnewiamge.setStyleSheet("background-color:white;border:1px solid red")
        self.lbnewiamge.setFixedSize(192 * 4, 108 * 4)
        self.tab3layout.addWidget(self.lbnewiamge, 0, 0, 1, 10)
        self.line1widelabel = QLabel()
        self.line1widelabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tab3layout.addWidget(self.line1widelabel, 1, 0, 1, 1)
        self.line1wide = QSlider(Qt.Horizontal)
        self.line1wide.setMinimum(1)  # 最小值
        self.line1wide.setMaximum(200)  # 最大值
        self.line1wide.setSingleStep(1)  # 步长
        self.line1wide.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.line1wide.setValue(5)
        self.line1widelabel.setText("线一宽:" + str(self.line1wide.value()))
        self.line1wide.valueChanged.connect(self.line1widechanged)
        self.tab3layout.addWidget(self.line1wide, 1, 1, 1, 4)
        self.line1colorfrm = QLabel("线一颜色")
        self.line1colorfrm.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # self.line1colorfrm.setStyleSheet("QWidget { background-color : %s}" % self.line1color.name())
        self.tab3layout.addWidget(self.line1colorfrm, 1, 5, 1, 1)
        self.line1colorbotton = QPushButton()
        self.line1colorbotton.setStyleSheet(
            "QWidget {border:2px solid black; background-color : %s}" % self.line1color.name())
        self.line1colorbotton.clicked.connect(self.line1colorbottonclicked)
        self.tab3layout.addWidget(self.line1colorbotton, 1, 6, 1, 1)

        self.line2widelabel = QLabel()
        self.line2widelabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tab3layout.addWidget(self.line2widelabel, 2, 0, 1, 1)
        self.line2wide = QSlider(Qt.Horizontal)
        self.line2wide.setMinimum(1)  # 最小值
        self.line2wide.setMaximum(200)  # 最大值
        self.line2wide.setSingleStep(1)  # 步长
        self.line2wide.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方

        self.line2wide.setValue(5)
        self.line2widelabel.setText("线二宽:" + str(self.line2wide.value()))
        self.line2wide.valueChanged.connect(self.line2widechanged)
        self.tab3layout.addWidget(self.line2wide, 2, 1, 1, 4)
        self.line2colorfrm = QLabel("线二颜色")
        self.line2colorfrm.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # self.line2colorfrm.setStyleSheet("QWidget { background-color : %s}" % self.line2color.name())
        self.tab3layout.addWidget(self.line2colorfrm, 2, 5, 1, 1)
        self.line2colorbotton = QPushButton()
        self.line2colorbotton.setStyleSheet(
            "QWidget { border:2px solid black;background-color : %s}" % self.line2color.name())
        self.line2colorbotton.clicked.connect(self.line2colorbottonclicked)
        self.tab3layout.addWidget(self.line2colorbotton, 2, 6, 1, 1)

        self.makeimagebutton = QPushButton("生成图片")
        self.makeimagebutton.clicked.connect(self.makeimagebottonclicked)
        self.tab3layout.addWidget(self.makeimagebutton, 1, 7, 2, 1)
        self.addtolistbutton = QPushButton("添加到列表")
        self.addtolistbutton.clicked.connect(self.addtolistbuttonclicked)
        self.tab3layout.addWidget(self.addtolistbutton, 3, 0, 1, 1)
        self.addtolistandoutbutton = QPushButton("添加到列表并输出")
        self.addtolistandoutbutton.clicked.connect(self.addtolistandoutbuttonclicked)
        self.tab3layout.addWidget(self.addtolistandoutbutton, 3, 1, 1, 1)
        self.savetostorebutton = QPushButton("保存到生成库")
        self.savetostorebutton.clicked.connect(self.savetostorebuttonclicked)
        self.tab3layout.addWidget(self.savetostorebutton, 3, 2, 1, 1)
        self.changestoredirbutton = QPushButton("修改库目录")
        self.changestoredirbutton.clicked.connect(self.changestoredirbuttonclick)
        self.tab3layout.addWidget(self.changestoredirbutton, 3, 3, 1, 1)
        self.changestoredirLine = QLineEdit()
        self.changestoredirLine.setText(self.storedir)
        self.changestoredirLine.setReadOnly(True)
        self.tab3layout.addWidget(self.changestoredirLine, 3, 4, 1, 3)
        # ****************************************************

        # *****************************************************
        # todo:多阶光栅
        self.tab4layout = QGridLayout()
        self.lbnewiamge2 = QLabel()
        self.lbnewiamge2.setStyleSheet("background-color:white;border:1px solid red")
        self.lbnewiamge2.setFixedSize(192 * 4, 108 * 4)
        self.tab4layout.addWidget(self.lbnewiamge2, 0, 0, 1, 10)
        self.Multorderlabel = QLabel()
        self.tab4layout.addWidget(self.Multorderlabel, 1, 0, 1, 1)
        self.MultorderSlider = QSlider(Qt.Horizontal)
        self.tab4layout.addWidget(self.MultorderSlider, 1, 1, 1, 5)
        self.MultorderSlider.setMinimum(2)  # 最小值
        self.MultorderSlider.setMaximum(256)  # 最大值
        self.MultorderSlider.setSingleStep(1)  # 步长
        self.MultorderSlider.setTickPosition(QSlider.TicksBelow)
        self.MultorderSlider.valueChanged.connect(self.MultorderSliderchanged)
        self.MultorderSlider.setValue(8)
        self.Multorderlabel.setText("光栅阶数:" + str(self.MultorderSlider.value()))

        self.pixelnwidelabel = QLabel()
        self.tab4layout.addWidget(self.pixelnwidelabel, 2, 0, 1, 1)
        self.pixelnwideSlider = QSlider(Qt.Horizontal)
        self.tab4layout.addWidget(self.pixelnwideSlider, 2, 1, 1, 5)
        self.pixelnwideSlider.setMinimum(1)  # 最小值
        self.pixelnwideSlider.setMaximum(100)  # 最大值
        self.pixelnwideSlider.setSingleStep(1)  # 步长
        self.pixelnwideSlider.setTickPosition(QSlider.TicksBelow)
        self.pixelnwideSlider.valueChanged.connect(self.pixelnwideSliderchanged)
        self.pixelnwideSlider.setValue(2)
        self.pixelnwidelabel.setText("像素宽度:" + str(self.pixelnwideSlider.value()))

        self.makemultorderimagebutton = QPushButton("生成图片")
        self.makemultorderimagebutton.clicked.connect(self.makemultorderimagebuttonclicked)
        self.tab4layout.addWidget(self.makemultorderimagebutton, 3, 0, 1, 1)
        self.addmultordertolistbutton = QPushButton("添加到列表")
        self.addmultordertolistbutton.clicked.connect(self.addmultordertolistbuttonclicked)
        self.tab4layout.addWidget(self.addmultordertolistbutton, 3, 1, 1, 1)


        self.changestoredirbuttontab4 = QPushButton("修改库目录")
        self.changestoredirbuttontab4.clicked.connect(self.changestoredirbuttonclick)
        self.tab4layout.addWidget(self.changestoredirbuttontab4, 3, 3, 1, 1)
        self.changestoredirLinetab4 = QLineEdit()
        self.changestoredirLinetab4.setText(self.storedir)
        self.changestoredirLinetab4.setReadOnly(True)
        self.tab4layout.addWidget(self.changestoredirLine, 3, 4, 1, 3)

        # self.line1wide.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        # self.line1wide.setValue(5)
        # self.tab3layout.addWidget(self.changestoredirbutton, 3, 3, 1, 1)
        # self.changestoredirLine = QLineEdit()
        # self.changestoredirLine.setText(self.storedir)
        # self.changestoredirLine.setReadOnly(True)
        # self.tab3layout.addWidget(self.changestoredirLine, 3, 4, 1, 3)
        # *****************************************************

        # todo:预览图片选项卡
        self.imagetab = QTabWidget()
        self.imagetab.setFont(QFont("Microsoft YaHei", 12))
        # self.imagetab.setStyleSheet("background-color:red")
        self.tab1layout = QHBoxLayout()
        self.tab2layout = QHBoxLayout()
        self.tabinflayout = QHBoxLayout()
        self.tab1widget = QWidget()
        self.tab2widget = QWidget()
        self.tab3widget = QWidget()
        self.tab4widget = QWidget()
        self.tabinfwidget = QWidget()

        self.tab1layout.addWidget(self.lb)
        self.tab2layout.addWidget(self.lb2)
        self.tabinflayout.addWidget(self.instructions)

        self.tab1widget.setLayout(self.tab1layout)
        self.tab2widget.setLayout(self.tab2layout)
        self.tab3widget.setLayout(self.tab3layout)
        self.tab4widget.setLayout(self.tab4layout)
        self.tabinfwidget.setLayout(self.tabinflayout)

        self.tab1 = self.imagetab.addTab(self.tab1widget, "辅屏画面预览")
        self.tab2 = self.imagetab.addTab(self.tab2widget, "图片编辑")
        self.tab3 = self.imagetab.addTab(self.tab3widget, "图片生成")
        self.tab4 = self.imagetab.addTab(self.tab4widget, "多阶光栅图片生成")
        self.tabinf = self.imagetab.addTab(self.tabinfwidget, "说明文档")
        # self.tab1=self.imagetab.addTab(self.lb, "辅屏画面预览")
        # self.tab2=self.imagetab.addTab(self.lb2, "图片编辑")
        # # self.tab1.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        # # self.tab2.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.imagetab.setTabIcon(self.tab1, QtGui.QIcon('display.png'))
        self.imagetab.setTabIcon(self.tab2, QtGui.QIcon('picture.png'))
        self.imagetab.setTabIcon(self.tabinf, QtGui.QIcon('ins.png'))
        self.grid.addWidget(self.imagetab, 0, 0, 1, 8)

        # todo:读取文件按钮
        self.outeditimagebutton = QPushButton("将编辑的图片输出到辅屏")
        self.outeditimagebutton.clicked.connect(lambda: self.outeditimage())
        self.grid.addWidget(self.outeditimagebutton, 1, 0, 1, 1)

        # todo:辅屏检测
        self.inflabel = QLabel("当前屏幕数:"+str(self.screen_count))


        self.grid.addWidget(self.inflabel, 1, 2, 1, 2)
        self.checkwinbutton = QPushButton("辅屏检测")
        self.checkwinbutton.clicked.connect(self.checkwinclicked)
        self.grid.addWidget(self.checkwinbutton, 1, 1, 1, 1)

        # todo:文件路径显示框
        self.filepathline = QLineEdit()
        self.filepathline.setPlaceholderText('请点击右侧按钮选择图片→')
        self.filepathline.setReadOnly(True)
        self.grid.addWidget(self.filepathline, 2, 0, 1, 6)

        # todo:读取文件按钮
        self.readfilebutton = QPushButton("添加图片文件")
        self.readfilebutton.clicked.connect(lambda: self.readfile())
        self.grid.addWidget(self.readfilebutton, 2, 6, 1, 1)

        # todo:读取文件夹按钮
        self.readfolderbutton = QPushButton("添加图片文件夹")
        self.readfolderbutton.clicked.connect(lambda: self.readfolder())
        self.grid.addWidget(self.readfolderbutton, 2, 7, 1, 1)

        # todo:删除文件按钮
        self.deletefilebutton = QPushButton("移除图片")
        self.deletefilebutton.clicked.connect(lambda: self.deletefile())
        self.grid.addWidget(self.deletefilebutton, 2, 8, 1, 1)

        # todo:清空文件按钮
        self.deletefilebutton = QPushButton("清空图片")
        self.deletefilebutton.clicked.connect(lambda: self.clearfile())
        self.grid.addWidget(self.deletefilebutton, 2, 9, 1, 1)

        # todo:图片预览列表
        self.list0 = QTableWidget()
        self.list0.setRowCount(1)
        self.list0.setColumnCount(1)
        self.list0.setSelectionBehavior(QAbstractItemView.SelectColumns)
        self.list0.clicked.connect(self.list0Rowindexchanged)
        # self.list0.setWindowFlags(Qt.FramelessWindowHint)
        self.list0.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list0.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)  # 一行也可以滚动
        self.list0.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)  # 一列也可以滚动
        self.list0.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.list0.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.list0.setFixedSize(1250,250)
        self.list0.setFixedHeight(250)
        self.grid.addWidget(self.list0, 3, 0, 1, 10)

        # todo:文件列表框
        self.list1 = QTableWidget()
        self.list1.setColumnCount(1)
        self.list1.setRowCount(6)
        self.list1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list1.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list1.setVerticalHeaderLabels(["文件名", "类型", "父路径", "宽度", "高度", "色深"])
        self.list1.setHorizontalHeaderLabels(["图片属性"])
        self.grid.addWidget(self.list1, 0, 8, 2, 2)
        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)
        self.statusBar().showMessage("请添加图片文件")
        self.loadache()
        # self.resize(1200,870)
        # self.setMinimumHeight(870)
        # self.setMaximumHeight(870)
        # self.setMaximumWidth(1250)
        # self.setMinimumWidth(1250)
        # self.resize(192 * 10, 108 * 10)

    # todo:重写窗口关闭事件
    def closeEvent(self, event):
        self.savehistory()
        self.lb3.close()
    # todo:屏幕检测事件
    def checkwinclicked(self):
        if self.screen_count > 1:
            self.lb3.setGeometry(self.win2)
            self.lb3.show()



    # todo:读取文件按钮事件
    def readfile(self):
        if self.reading == True:
            self.statusBar().showMessage("正在读取，请稍后重试！")
        else:
            self.reading == True
            path = QFileDialog.getOpenFileName(self, '请选择图片文件', '', 'Image Files (*.jpg *.png *.jpeg)')
            self.runreadfileThread(path)

    # todo:读取文件夹按钮事件
    def readfolder(self):
        if self.reading == True:
            self.statusBar().showMessage("正在读取，请稍后重试！")
        else:
            self.reading == True
            path = QFileDialog.getExistingDirectory(self, "请选择图片文件目录")
            self.runreadfileThread(path)

    # todo:拖拽路径进入软件事件
    def filepathdrop(self, path):
        if self.reading == True:
            self.statusBar().showMessage("正在读取，请稍后重试！")
        else:
            self.runreadfileThread(path)

    # todo:移除图片事件
    def deletefile(self):
        if self.list0.currentIndex().column() < 0:
            self.statusBar().showMessage("请选择要移除图片")
        else:
            tempindex = self.list0.currentIndex().column()
            file = self.data.filelist.pop(self.list0.currentIndex().column())
            self.savehistory()
            self.readending()
            if tempindex == len(self.data.filelist):
                self.list0.selectColumn(len(self.data.filelist) - 1)
            else:
                self.list0.selectColumn(tempindex)
            self.statusBar().showMessage("已移除图片‘" + file["allfilename"] + "’")
            self.list1.clearContents()  # 清空数据 保留表头
            self.list0Rowindexchanged()

    # todo:清空图片事件
    def clearfile(self):
        self.data.filelist = []
        self.list0.clearContents()
        self.list1.clearContents()
        self.list0.setColumnCount(0)
        self.list0.setRowCount(0)
        self.lb.clear()
        # self.lb2.clear()
        self.lb3.clear()
        self.statusBar().showMessage("已清空图片列表")

    # todo:将编辑图片输出到辅屏事件
    def outeditimage(self):
        print(self.lb2.singleOffset.x(), self.lb2.singleOffset.y())
        pix = self.lb2.scaledImg.copy(-self.lb2.singleOffset.x(), -self.lb2.singleOffset.y(), self.lb2.width(),
                                      self.lb2.height())
        print("*******************")
        print("原图", self.lb2.scaledImg.width(), self.lb2.scaledImg.height())
        print("裁剪图", pix.width(), pix.height())
        print("*******************")
        lb2x = self.lb2.singleOffset.x()
        lb2y = self.lb2.singleOffset.y()
        lbx = lb2x
        lby = lb2y
        lb3x = lb2x / self.lb2.width() * self.lb3.width()
        lb3y = lb2y / self.lb2.height() * self.lb3.height()
        self.lb.setPixmap(pix)
        self.lb3.setPixmap(pix.scaled(self.lb3.width() / self.lb2.width() * pix.width(),
                                      self.lb3.height() / self.lb2.height() * pix.height()))
        self.statusBar().showMessage("已将编辑的图片输出到辅屏！")

    # todo:启动读取图片线程
    def runreadfileThread(self, path):
        self.reading == True
        self.thraedreadfile = readfilethread(path, self.data)
        self.thraedreadfile.EnddingSingle.connect(self.readending)
        self.thraedreadfile.MessageSingle.connect(self.statusBar().showMessage)
        self.thraedreadfile.start()
        self.filepathline.setText(path)

    # 读todo:取数据，更新图像列表
    def readending(self):
        self.reading == False
        print(self.data)
        imagelist = []
        self.list0.clear()
        self.list0.setColumnCount(len(self.data.filelist))
        self.list0.setRowCount(1)
        for i in range(len(self.data.filelist)):
            imagepix = QLabel()
            image = self.data.filelist[i]
            imagepix.setPixmap(image["pix"].scaled(image["width"] / image["height"] * 200, 200, Qt.KeepAspectRatio,
                                                   Qt.SmoothTransformation))
            # imagepix.resize(image["width"]/image["height"]*20,20)

            # print("比例：",self.data.filelist[i]["height"]/self.data.filelist[i]["width"])
            # imagepix.setCursor(Qt.CrossCursor)
            imagepix.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            imagelist.append(imagepix)
            self.list0.setCellWidget(0, i, imagepix)
        # todo:更新自适应宽高尺寸
        self.list0.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.list0.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # todo:保存状态
        self.savehistory()

    # todo:点击图像列表事件
    def list0Rowindexchanged(self):
        if self.list0.currentIndex().column() == -1:
            self.lb.clear()
            # self.lb2.clear()
            self.lb3.clear()
            return

        print("self.fileindex:", self.list0.currentIndex().column())
        self.list1.setItem(0, 0,
                           QTableWidgetItem(str(self.data.filelist[self.list0.currentIndex().column()]["filename"])))
        self.list1.setItem(1, 0, QTableWidgetItem(
            str(self.data.filelist[self.list0.currentIndex().column()]["fileextension"])))
        self.list1.setItem(2, 0,
                           QTableWidgetItem(str(self.data.filelist[self.list0.currentIndex().column()]["parentdir"])))
        self.list1.setItem(3, 0, QTableWidgetItem(
            str(self.data.filelist[self.list0.currentIndex().column()]["width"]) + "px"))
        self.list1.setItem(4, 0, QTableWidgetItem(
            str(self.data.filelist[self.list0.currentIndex().column()]["height"]) + "px"))
        self.list1.setItem(5, 0,
                           QTableWidgetItem(str(self.data.filelist[self.list0.currentIndex().column()]["depth"]) + "位"))

        # 更新铺屏预览图
        image = self.data.filelist[self.list0.currentIndex().column()]
        # 根据辅屏比例修改预览图中图片比例
        imageresize = image["pix"].scaled(image["width"] / 1920 * self.lb.width(),
                                          image["height"] / 1080 * self.lb.height(), Qt.KeepAspectRatio,
                                          Qt.SmoothTransformation)
        self.lb.setPixmap(imageresize)
        self.lb.setCursor(Qt.CrossCursor)

        # 更新图片预览图
        self.lb2.setPixmap(
            image["pix"].scaled(self.lb.width(), self.lb.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.lb2.setCursor(Qt.CrossCursor)

        # 更新辅屏
        self.lb3.setPixmap(self.data.filelist[self.list0.currentIndex().column()]["pix"])
        # self.lb3.setCursor(Qt.CrossCursor)
        self.timestart = time.time()
        self.statusBar().showMessage("辅屏图片已更新！")

    # todo:保存状态函数
    def savehistory(self):
        achepath = os.getcwd() + "/ache/"
        print("缓存：", self.list0.currentIndex().column())
        self.thraedhistory = savehistorythread(achepath, self.data, self.list0.currentIndex().column())
        self.thraedhistory.MessageSingle.connect(self.statusBar().showMessage)
        self.thraedhistory.start()

    # todo:读取缓存
    def loadache(self):
        achepath = os.getcwd() + "/ache/history.ache"
        print(os.path.exists(achepath))
        print(achepath)
        if (os.path.exists(achepath)):
            self.reading = True
            self.thraedreadhistory = readhostorythread(achepath)
            self.thraedreadhistory.MessageSingle.connect(self.statusBar().showMessage)
            self.thraedreadhistory.EnddingSingle.connect(self.loadacheennding)
            self.thraedreadhistory.start()

    # todo:加载缓存
    def loadacheennding(self, data):
        print("data缓存：", data["selectindex"])
        self.data = data["data"]
        lasttime = data["exittime"]
        self.reading = False
        self.readending()
        self.list0.selectColumn(data["selectindex"])
        print("self.list0.currentIndex().column()", self.list0.currentIndex().column())
        self.list0Rowindexchanged()
        self.statusBar().showMessage("已加载缓存！（上次退出时间：" + lasttime + ")")

    # todo:线一宽度改变事件
    def line1widechanged(self, value):
        self.line1widelabel.setText("线一宽:" + str(value))

    # todo:线二宽度改变事件
    def line2widechanged(self, value):
        self.line2widelabel.setText("线二宽:" + str(value))

    # todo:线一颜色改变事件
    def line1colorbottonclicked(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.line1color = col
            self.line1colorbotton.setStyleSheet("QWidget { background-color: %s }"
                                                % col.name())
            # self.line1colorfrm.setStyleSheet("QWidget { background-color: %s }"
            #     % col.name())

    # todo:线二颜色改变事件
    def line2colorbottonclicked(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.line2color = col
            self.line2colorbotton.setStyleSheet("QWidget { background-color: %s }"
                                                % col.name())
            # self.line2colorfrm.setStyleSheet("QWidget { background-color: %s }"
            #     % col.name())

    # todo:（tab3）生成图片事件
    def makeimagebottonclicked(self):
        self.statusBar().showMessage("正在生成图片...")
        self.makethread = makeimage(self.direction, self.line1wide.value(), self.line2wide.value(),
                                    np.array(list(self.line1color.getRgb())), np.array(list(self.line2color.getRgb())))
        self.makethread.MessageSingle.connect(self.statusBar().showMessage)
        self.makethread.EnddingSingle.connect(self.makeimagethreadend)
        self.makethread.start()
        #
        # wmax=1920
        # hmax=1080
        # # imagedata = np.zeros([wmax, hmax])
        # if self.direction=="H":
        #     copynum=math.ceil(1920/float(self.line1wide.value()+self.line2wide.value()))  #向上取整
        #     print("copynum",copynum)
        #     line1=np.array([])
        #     for i in range(self.line1wide.value()*hmax):
        #     #     line1 = np.append(line1, np.array(list(self.line1color.getRgb())))
        #     # line1 = line1.reshape(hmax, self.line1wide.value(), 4)
        #         line1=np.append(line1,np.array(list(self.line1color.getRgb())))
        #     line1=line1.reshape(hmax,self.line1wide.value(),4)
        #
        #     line2 = np.array([])
        #     for i in range(self.line2wide.value() * hmax):
        #     #     line2 = np.append(line2, np.array(list(self.line2color.getRgb())))
        #     # line2 = line2.reshape(hmax, self.line2wide.value(), 4)
        #         line2 = np.append(line2, np.array(list(self.line2color.getRgb())))
        #     line2 = line2.reshape(hmax,self.line2wide.value(), 4)
        #
        #     list12=np.hstack((line1, line2))
        #     list12=list12.astype(np.uint8)
        #     imagedata=np.tile(list12,(1,copynum,1))
        #     imagedata=imagedata[:,0:1920,0:3].copy()
        #     print(imagedata.shape)
        #     height, width,  bytesPerComponent = imagedata.shape
        #     bytesPerLine = bytesPerComponent * width  # 表示彩色图像每个像素占用3个（ndarray图像数组的第三维长度）字节的空间
        #     self.newtempQImg = QImage(imagedata, width, height,bytesPerLine, QImage.Format_RGB888)
        #     self.newtemppixmap = QPixmap(self.newtempQImg)
        #     pixtemp=self.newtemppixmap.scaled(self.lbnewiamge.width(),self.lbnewiamge.height())
        #     self.lbnewiamge.setPixmap(pixtemp)

    # todo:（tab3）加载新生成图片
    def makeimagethreadend(self, qimage, pixmap):
        self.newtempQImg = qimage
        self.newtemppixmap = pixmap
        self.statusBar().showMessage("正在加载图片...")
        pixtemp = self.newtemppixmap.scaled(self.lbnewiamge.width(), self.lbnewiamge.height())
        self.lbnewiamge.setPixmap(pixtemp)
        self.statusBar().showMessage("图片生成成功！")

    def addtolistbuttonclicked(self):
        if (self.newtemppixmap == []):
            self.statusBar().showMessage("请先生成图片")
            return
        if (not os.path.exists(os.getcwd() + "/temp/")):
            os.makedirs(os.getcwd() + "/temp/")
        print(os.getcwd() + "/temp/" + self.direction + "_" + self.line1color.name() + str(
            self.line1wide.value()) + "_" + self.line2color.name() + str(self.line2wide.value()) + ".png")
        filepath = os.getcwd() + "/temp/" + self.direction + "_" + self.line1color.name() + str(
            self.line1wide.value()) + "_" + self.line2color.name() + str(self.line2wide.value()) + ".png"
        try:
            self.newtempQImg.save(filepath)
        except Exception as a:
            print(a)
        self.reading = True
        self.data.addfile(filepath)
        self.reading = False
        self.readending()
        self.statusBar().showMessage("已将图片添加到列表！")
        # filedir, allfilename = os.path.split(filepath)
        # filename, fileextension = os.path.splitext(allfilename)
        # filedict=dict()
        # filedict["alldir"] = filepath  # 文件路径
        # filedict["parentdir"] = filedir  # 父路径
        # filedict["allfilename"] = allfilename  # 全名
        # filedict["filename"] = filename  # 文件名
        # filedict["fileextension"] = fileextension  # 后缀名
        # filedict["pix"] = self.newtemppixmap  # 图片对象
        # filedict["width"] = self.newtemppixmap.width()  # 图片宽度
        # filedict["depth"] = self.newtemppixmap.depth()  # 图片深度bit
        # filedict["height"] = self.newtemppixmap.height()  # 图片高度

    def addtolistandoutbuttonclicked(self):
        pass

    def savetostorebuttonclicked(self):
        pass

    def changestoredirbuttonclick(self):
        path = QFileDialog.getExistingDirectory(self, "请选择图片文件目录")
        if path == "":
            return
        if (not os.path.exists(os.getcwd() + "/ache/")):
            os.makedirs(self.achepath)
        with open(os.getcwd() + "/ache/" + "storepath.ache", "wb") as file:
            pickle.dump(path, file, True)
        self.storedir = path
        self.changestoredirLine.setText(path)
        self.changestoredirLinetab4.setText(path)
        self.statusBar().showMessage("库目录修改成功！！")

    # todo: 光栅阶数滑块改变
    def MultorderSliderchanged(self,value):
        self.Multorderlabel.setText("光栅阶数:"+str(value))

    # todo: 像素宽度滑块改变
    def pixelnwideSliderchanged(self,value):
        self.pixelnwidelabel.setText("像素宽度:" + str(value))

    # todo:多阶光栅生成按钮点击事件 **********************
    def makemultorderimagebuttonclicked(self):
        self.makemultorderthread = makemultorderimagethread(self.direction, self.pixelnwideSlider.value(),
                                                            self.MultorderSlider.value())
        self.statusBar().showMessage("正在生成图片...")
        self.makemultorderthread.MessageSingle.connect(self.statusBar().showMessage)
        self.makemultorderthread.EnddingSingle.connect(self.makemultorderimagethreadend)
        self.makemultorderthread.start()

    # todo:（tab4）加载新生成图片
    def makemultorderimagethreadend(self, qimage, pixmap):
        self.newtempQImg2 = qimage
        self.newtemppixmap2 = pixmap
        self.statusBar().showMessage("正在加载图片...")
        pixtemp = self.newtemppixmap2.scaled(self.lbnewiamge.width(), self.lbnewiamge.height())
        self.lbnewiamge2.setPixmap(pixtemp)
        self.statusBar().showMessage("图片生成成功！")

    def addmultordertolistbuttonclicked(self):
        if (self.newtemppixmap2 == []):
            self.statusBar().showMessage("请先生成图片")
            return
        if (not os.path.exists(os.getcwd() + "/temp/")):
            os.makedirs(os.getcwd() + "/temp/")
        print(os.getcwd() + "/temp/" + self.direction + "_" + "像素宽度（"+str(self.pixelnwideSlider.value())+")_阶数（"+str(self.MultorderSlider.value()) + "）.png")
        filepath = os.getcwd() + "/temp/" + self.direction + "_" + "像素宽度（"+str(self.pixelnwideSlider.value())+")_阶数（"+str(self.MultorderSlider.value()) + "）.png"
        try:
            self.newtempQImg2.save(filepath)
        except Exception as a:
            print(a)
        self.reading = True
        self.data.addfile(filepath)
        self.reading = False
        self.readending()
        self.statusBar().showMessage("已将图片添加到列表！")
        # filedir, allfilename = os.path.split(filepath)
        # filename, fileextension = os.path.splitext(allfilename)
        # filedict=dict()
        # filedict["alldir"] = filepath  # 文件路径
        # filedict["parentdir"] = filedir  # 父路径
        # filedict["allfilename"] = allfilename  # 全名
        # filedict["filename"] = filename  # 文件名
        # filedict["fileextension"] = fileextension  # 后缀名
        # filedict["pix"] = self.newtemppixmap  # 图片对象
        # filedict["width"] = self.newtemppixmap.width()  # 图片宽度
        # filedict["depth"] = self.newtemppixmap.depth()  # 图片深度bit
        # filedict["height"] = self.newtemppixmap.height()  # 图片高度

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = main()
    ui.show()
    sys.exit(app.exec_())
