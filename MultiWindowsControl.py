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
from MyDemo import Label, editimageLabel,Lineedit,TableWidget,TableWidget2,TableWidget3,TableWidget4
import time
from PyQt5.QtWebEngineWidgets import *
from rasterimagemodel import rasterwidget
from vorteximagemodel import vortexwidget
from diffimagemodel import diffwidget
from displayimagelist import displayimagelistwidget



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
        self.progressBar = QProgressBar()
        self.progressBar.setVisible(False)
        self.statusBar().addPermanentWidget(self.progressBar)
        # self.setStyleSheet("background-color:rgb(198,47,47,115);")
        self.move(20, 10)

        # todo:全局变量
        self.filelist = []
        self.reading = False
        self.timestart = -1
        self.settingdict=dict()
        self.data = imageObject()
        self.newtemppixmap2 = []
        self.direction = "H"
        self.direction2 = "H"
        self.settingdict["storedir"] = os.getcwd() + "/store/"
        self.settingdict["interval"] = 500

        # todo:获取屏幕信息
        self.desktop = QApplication.desktop()
        self.screen_count = self.desktop.screenCount()  # 屏幕数量
        self.win1 = self.desktop.screenGeometry(0)  # 参数为显示屏索引，如果安装了两个显示屏，主显示屏索引为0，辅显示屏索引为1
        self.win2 = self.desktop.screenGeometry(1)  # 参数为显示屏索引，如果安装了两个显示屏，主显示屏索引为0，辅显示屏索引为1
        # available_rect = desktop.availableGeometry(0)  # 参数为显示屏索引，如果安装了两个显示屏，主显示屏索引为0，辅显示屏索引为1

        # todo:屏幕1Wigget
        self.widget = QWidget()
        self.widget.setGeometry(self.win1)

        # todo:主屏幕布局
        self.grid = QGridLayout()

        # todo:图片预览列表
        self.list0 = TableWidget()
        self.list0.setDragEnabled(True)
        self.list0.setAcceptDrops(True)
        self.list0.FilepathSignal.connect(self.filepathdrop)
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

        self.list0.horizontalHeader().setSectionsMovable(True)
        self.list0.horizontalHeader().setDragEnabled(True)
        self.list0.horizontalHeader().setDragDropMode(QAbstractItemView.InternalMove)

        # self.list0.setFixedSize(1250,250)
        self.list0.setFixedHeight(250)
        self.grid.addWidget(self.list0, 4, 0, 1, 8)

        # todo:文件列表框
        self.list1 = TableWidget()
        # self.list1 = QTableWidget()
        self.list1.setColumnCount(1)
        self.list1.setRowCount(6)
        self.list1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list1.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list1.setVerticalHeaderLabels(["文件名", "类型", "父路径", "宽度", "高度", "色深"])
        self.list1.setHorizontalHeaderLabels(["图片属性"])


        self.grid.addWidget(self.list1, 0, 6, 1, 2)
        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)
        self.statusBar().showMessage("请添加图片文件")
        # self.resize(1200,870)
        # self.setMinimumHeight(870)
        # self.setMaximumHeight(870)
        # self.setMaximumWidth(1250)
        # self.setMinimumWidth(1250)
        # self.resize(192 * 10, 108 * 10)

        # todo:预览辅屏
        # self.lb = QWidget("请选择图片，或将图片文件拖拽至此！")
        # self.lb = Label("请选择图片，或将图片文件拖拽至此！")
        self.lb = Label()
        # self.lb.resize(192*5, 108*5)
        self.lb.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.lb.setStyleSheet("background-color:white;border:2px solid red")
        self.lb.MessageSignal.connect(self.statusBar().showMessage)
        self.lb.FilepathSignal.connect(self.filepathdrop)
        self.lb.setAcceptDrops(True)
        self.lb.setFixedSize(192 * 5, 108 * 5)

        self.lblabel=QLabel()
        self.lblabel.setText("无图片输出")

        # todo:编辑图片
        # self.lb2 = Label("请选择图片，或将图片文件拖拽至此！")
        self.lb2 = editimageLabel()
        self.lb2.setStyleSheet("background-color:white;border:2px solid red")
        # self.lb.resize(192*5, 108*5)
        # self.lb2.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
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
        self.browser = QWebEngineView()
        # 加载外部页面，调用
        # htmlfile=QFile()
        self.browser.load(QUrl("file:///" +"html/directions.html"))

        # todo:预览图片选项卡
        self.imagetab = QTabWidget()
        self.imagetab.setFont(QFont("Microsoft YaHei", 12))

        # todo:图片输出按钮
        self.outeditimagebutton = QPushButton("将编辑的图片输出到辅屏")
        self.outeditimagebutton.setIcon(QIcon("输入.png"))
        self.outeditimagebutton.clicked.connect(lambda: self.outeditimage())
        # self.grid.addWidget(self.outeditimagebutton, 1, 0, 1, 1)

        # self.imagetab.setStyleSheet("background-color:red")
        self.tab1layout = QVBoxLayout()
        self.tab2layout = QVBoxLayout()
        self.tabinflayout = QHBoxLayout()
        self.tabinflayout.setContentsMargins(0, 0, 0, 0)

        self.tab1widget = QWidget()
        self.tab2widget = QWidget()
        self.tab3widget = QWidget()
        self.tab4widget = QWidget()
        self.tabinfwidget = QWidget()
        self.tabinfwidget.setContentsMargins(0, 0, 0, 0)

        self.tab1layout.addWidget(self.lb)
        self.tab1layout.addWidget(self.lblabel)
        self.tab2layout.addWidget(self.lb2)
        self.tab2layout.addWidget(self.outeditimagebutton)
        self.tabinflayout.addWidget(self.browser)
        # self.tabinflayout.addWidget(self.instructions)

        self.tab1layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.tab2layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        # self.tab3layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        # self.tab4layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.tabinflayout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.tab1widget.setLayout(self.tab1layout)
        self.tab2widget.setLayout(self.tab2layout)
        # self.tab3widget.setLayout(self.tab3layout)
        #         # self.tab4widget.setLayout(self.tab4layout)
        self.tabinfwidget.setLayout(self.tabinflayout)

        self.tab1 = self.imagetab.addTab(self.tab1widget, "辅屏画面预览")
        self.tab2 = self.imagetab.addTab(self.tab2widget, "图片编辑")
        # self.tab3 = self.imagetab.addTab(self.tab3widget, "二阶光栅图片生成")

        self.tab4widget=rasterwidget(self.data,self.settingdict, self.statusBar(), self.newtemppixmap2,self.progressBar)
        self.tab4widget.addtolistenddingSignal.connect(self.readending)
        self.tab4widget.settingchangeSignal.connect(self.savehistory)
        self.tab4widget.massageoutSignal.connect(self.statusBar().showMessage)

        self.tab5widget = vortexwidget(self.data, self.settingdict, self.statusBar(), self.newtemppixmap2,self.progressBar)
        self.tab5widget.addtolistenddingSignal.connect(self.readending)
        self.tab5widget.settingchangeSignal.connect(self.savehistory)
        self.tab5widget.massageoutSignal.connect(self.statusBar().showMessage)

        self.tab6widget = diffwidget(self.data, self.settingdict, self.statusBar(), self.newtemppixmap2,self.progressBar)
        self.tab6widget.addtolistenddingSignal.connect(self.readending)
        self.tab6widget.settingchangeSignal.connect(self.savehistory)
        self.tab6widget.massageoutSignal.connect(self.statusBar().showMessage)

        self.tab7widget = displayimagelistwidget(self.data, self.settingdict, self.statusBar(), self.newtemppixmap2,self.list0,self.lb,self.lb3,self.lblabel)
        self.tab7widget.setContentsMargins(0, 0, 0, 0)
        # self.tab7widget.addtolistenddingSignal.connect(self.readending)
        self.tab7widget.massageoutSignal.connect(self.statusBar().showMessage)
        self.tab7widget.settingchangeSignal.connect(self.savehistory)

        self.tab4 = self.imagetab.addTab(self.tab4widget ,"多阶光栅图片生成")
        self.tab5 = self.imagetab.addTab(self.tab5widget ,"涡旋光束图片生成")
        self.tab6 = self.imagetab.addTab(self.tab6widget ,"衍射光束图片生成")
        # self.tab7 = self.imagetab.addTab(self.tab7widget ,"连续图像输出")
        self.tabinf = self.imagetab.addTab(self.browser, "说明文档")
        # self.tabinf = self.imagetab.addTab(self.tabinfwidget, "说明文档")
        # self.tab1=self.imagetab.addTab(self.lb, "辅屏画面预览")
        # self.tab2=self.imagetab.addTab(self.lb2, "图片编辑")
        # # self.tab1.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        # # self.tab2.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.imagetab.setTabIcon(self.tab1, QtGui.QIcon('display.png'))
        self.imagetab.setTabIcon(self.tab2, QtGui.QIcon('编辑图片.png'))
        # self.imagetab.setTabIcon(self.tab3, QtGui.QIcon('picture.png'))
        self.imagetab.setTabIcon(self.tab4, QtGui.QIcon('多光栅图片生成.png'))
        self.imagetab.setTabIcon(self.tab5, QtGui.QIcon('多光栅图片生成.png'))
        self.imagetab.setTabIcon(self.tab6, QtGui.QIcon('多光栅图片生成.png'))
        self.imagetab.setTabIcon(self.tabinf, QtGui.QIcon('ins.png'))
        self.grid.addWidget(self.imagetab, 0, 0, 1, 6)

        # todo:图片输出按钮
        self.outeditimagebutton = QPushButton("将编辑的图片输出到辅屏")
        self.outeditimagebutton.setIcon(QIcon("输入.png"))
        self.outeditimagebutton.clicked.connect(lambda: self.outeditimage())
        # self.grid.addWidget(self.outeditimagebutton, 1, 0, 1, 1)

        # todo:辅屏检测标签
        self.inflabel = QLabel()
        self.grid.addWidget(self.inflabel, 1, 3, 1, 4)
        self.updatawincountthread=getwincountthread()
        self.updatawincountthread.wincountSingle.connect(self.checkwinclicked)
        self.updatawincountthread.start()

        # todo:库目录路径显示框
        self.storepathline = Lineedit()
        self.storepathline.setText(self.settingdict["storedir"])
        self.storepathline.setReadOnly(True)
        self.grid.addWidget(self.storepathline, 1, 0, 1, 2)

        # todo:修改库目录
        self.changestorebutton = QPushButton("修改图片库路径")
        self.changestorebutton.setIcon(QIcon("路径.png"))
        # self.openstorebutton.setIcon(QIcon("打开.png"))
        self.changestorebutton.clicked.connect(self.changestoreclicked)
        self.grid.addWidget(self.changestorebutton, 1, 2, 1, 1)

        # todo:文件路径显示框
        self.filepathline = Lineedit()
        self.filepathline.setPlaceholderText('请点击右侧按钮选择图片→')
        self.filepathline.FilepathSignal.connect(self.filepathdrop)
        self.filepathline.setReadOnly(True)
        self.grid.addWidget(self.filepathline, 2, 0, 1, 2)

        # todo:打开图片库
        self.openstorebutton = QPushButton("打开图片库")
        self.openstorebutton.setIcon(QIcon("打开.png"))
        self.openstorebutton.clicked.connect(lambda: self.openstore())
        self.grid.addWidget(self.openstorebutton, 2, 2, 1, 1)

        # todo:读取图片库
        self.readstorebutton = QPushButton("添加图片库图片")
        self.readstorebutton.setIcon(QIcon("图库.png"))
        self.readstorebutton.clicked.connect(lambda: self.readstore())
        self.grid.addWidget(self.readstorebutton, 2, 3, 1, 1)

        # todo:读取文件按钮
        self.readfilebutton = QPushButton("添加图片文件")
        self.readfilebutton.setIcon(QIcon("文件.png"))
        self.readfilebutton.clicked.connect(lambda: self.readfile())
        self.grid.addWidget(self.readfilebutton, 2, 4, 1, 1)

        # todo:读取文件夹按钮
        self.readfolderbutton = QPushButton("添加图片文件夹")
        self.readfolderbutton.setIcon(QIcon("文件夹.png"))
        self.readfolderbutton.clicked.connect(lambda: self.readfolder())
        self.grid.addWidget(self.readfolderbutton, 2, 5, 1, 1)

        # todo:删除文件按钮
        self.deletefilebutton = QPushButton("移除图片")
        self.deletefilebutton.setIcon(QIcon("删除.png"))
        self.deletefilebutton.clicked.connect(lambda: self.deletefile())
        self.grid.addWidget(self.deletefilebutton, 2, 6, 1, 1)

        # todo:清空文件按钮
        self.deleteallfilebutton = QPushButton("清空图片")
        self.deleteallfilebutton.setIcon(QIcon("清空.png"))
        self.deleteallfilebutton.clicked.connect(lambda: self.clearfile())
        self.grid.addWidget(self.deleteallfilebutton, 2, 7, 1, 1)
        self.loadache()

    # todo:重写窗口关闭事件
    def closeEvent(self, event):
        self.savehistory()
        self.lb3.close()

    # todo:屏幕检测事件
    def checkwinclicked(self,count):
        if(count>1):
            self.inflabel.setText("当前屏幕数:"+str(QApplication.desktop().screenCount())+"（检测到辅屏，已将信号传送到辅屏！）")
            self.lb3.setGeometry(QApplication.desktop().screenGeometry(1))
            self.lb3.show()
            self.inflabel.setStyleSheet("color:black")
            self.inflabel.setFont(QFont("Microsoft YaHei", 12))
            self.statusBar().showMessage("当前屏幕数"+str(QApplication.desktop().screenCount())+":（检测到辅屏，已将信号传送到辅屏！）")
        else:
            self.lb3.close()
            self.inflabel.setText("当前屏幕数:" + str(QApplication.desktop().screenCount()) + "（未检测到辅屏，输出窗口已关闭！)")
            self.inflabel.setStyleSheet("color:red")
            self.inflabel.setFont(QFont("Microsoft YaHei", 12))
            self.statusBar().showMessage("当前屏幕数:" + str(QApplication.desktop().screenCount()) + "（未检测到辅屏，输出窗口已关闭！)")

    # todo:修改图片库路径
    def changestoreclicked(self):
        path = QFileDialog.getExistingDirectory(self, "请选择图片文件目录")
        if path !="":
            self.settingdict["storedir"]=path
            self.storepathline.setText(path)
            if (not os.path.exists(os.getcwd() + "/ache/")):
                os.makedirs(self.achepath)
            with open(os.getcwd() + "/ache/" + "storepath.ache", "wb") as file:
                pickle.dump(path, file, True)
            self.statusBar().showMessage("图片库目录修改成功！")
        else:
            self.statusBar().showMessage("路径不能为空！")

    # todo:读取文件按钮事件
    def readfile(self):
        if self.reading == True:
            self.statusBar().showMessage("正在读取，请稍后重试！")
        else:
            self.reading == True
            path = QFileDialog.getOpenFileName(self, '请选择图片文件', '', 'Image Files (*.jpg *.png *.jpeg)')
            self.runreadfileThread(path)

    # todo:打开图片库
    def openstore(self):
        if(os.path.exists(self.settingdict["storedir"])):
            startfile(self.settingdict["storedir"])  # 打开文件夹窗口
        else:
            self.statusBar().showMessage("图片库文件夹不存在，请检查！")

    # todo:加载图片库事件
    def readstore(self):
        if os.path.exists(self.settingdict["storedir"]):
            self.runreadfileThread(self.settingdict["storedir"])
            self.statusBar().showMessage("已将图片库添加到列表！")
        else:
            self.statusBar().showMessage("图片库路径不存在！")

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
            # self.savehistory()
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
        self.readending()
        self.lb.clear()
        # self.lb2.clear()
        self.lb3.clear()
        self.statusBar().showMessage("已清空图片列表")

    # todo:将编辑图片输出到辅屏事件
    def outeditimage(self):
        print(self.lb2.singleOffset.x(), self.lb2.singleOffset.y())
        pix = self.lb2.scaledImg.copy(-self.lb2.singleOffset.x(), -self.lb2.singleOffset.y(), self.lb2.width(),
                                      self.lb2.height())
        # print("*******************")
        # print("原图", self.lb2.scaledImg.width(), self.lb2.scaledImg.height())
        # print("裁剪图", pix.width(), pix.height())
        # print("*******************")
        lb2x = self.lb2.singleOffset.x()
        lb2y = self.lb2.singleOffset.y()
        lbx = lb2x
        lby = lb2y
        lb3x = lb2x / self.lb2.width() * self.lb3.width()
        lb3y = lb2y / self.lb2.height() * self.lb3.height()
        self.lb.setPixmap(pix)
        self.lb3.setPixmap(pix.scaled(self.lb3.width() / self.lb2.width() * pix.width(),
                                      self.lb3.height() / self.lb2.height() * pix.height()))
        self.lb3.setCursor(Qt.BlankCursor)
        self.lblabel.setText(self.data.filelist[self.list0.currentIndex().column()]["filename"]+"(编辑后)")
        self.statusBar().showMessage("已将编辑的图片输出到辅屏！")

    # todo:启动读取图片线程
    def runreadfileThread(self, path):
        self.reading == True
        self.thraedreadfile = readfilethread(path, self.data)
        self.thraedreadfile.EnddingSingle.connect(self.readending)
        self.thraedreadfile.MessageSingle.connect(self.statusBar().showMessage)
        self.thraedreadfile.start()
        self.filepathline.setText(path)

    # todo:读取数据，更新图像列表
    def readending(self):
        print(self.tab7widget.width(),self.tab7widget.height())
        self.reading == False
        currentselectcol=self.list0.currentIndex().column()
        print(self.data)
        imagelist = []
        self.list0.clear()
        self.list0.setColumnCount(len(self.data.filelist))
        self.list0.setRowCount(1)
        for i in range(len(self.data.filelist)):
            imagepix = Label()
            image = self.data.filelist[i]
            imagepix.setPixmap(image["pix"].scaled(image["width"] / image["height"] * 200, 200, Qt.KeepAspectRatio,
                                                   Qt.SmoothTransformation))
            # imagepix.resize(image["width"]/image["height"]*20,20)

            # print("比例：",self.data.filelist[i]["height"]/self.data.filelist[i]["width"])
            # imagepix.setCursor(Qt.CrossCursor)
            imagepix.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            # imagelist.append(imagepix)
            imagepix.FilepathSignal.connect(self.filepathdrop)
            self.list0.setCellWidget(0, i, imagepix)
        # 更新自适应宽高尺寸
        self.list0.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.list0.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.list0.selectColumn(currentselectcol)
        # 保存状态
        self.savehistory()

    # todo:点击图像列表事件
    def list0Rowindexchanged(self):
        print("self.list0.rowCount()",self.list1.rowCount())
        if self.list0.currentIndex().column() == -1:
            self.lb.clear()
            # self.lb2.clear()
            self.lb3.clear()
            self.lb3.setCursor(Qt.BlankCursor)
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
        self.lblabel.setText(image["filename"])

        # 更新图片编辑图
        self.lb2.setPixmap(image["pix"])
        # self.lb2.setPixmap(image["pix"].scaled(self.lb.width(), self.lb.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.lb2.setCursor(Qt.CrossCursor)

        # 更新辅屏
        self.lb3.setPixmap(self.data.filelist[self.list0.currentIndex().column()]["pix"])
        self.lb3.setCursor(Qt.BlankCursor)
        # self.lb3.setCursor(Qt.CrossCursor)
        self.timestart = time.time()
        self.statusBar().showMessage("辅屏图片已更新！")

    # todo:保存状态函数
    def savehistory(self):

        achepath = os.getcwd() + "/ache/"
        print("缓存：", self.list0.currentIndex().column())
        setting=dict()
        setting["list0index"]=self.list0.currentIndex().column()
        setting["t4p1"]=self.tab4widget.MultorderSlider.value()
        setting["t4p2"]=self.tab4widget.pixelnwideSlider.value()
        setting["t4p3"]=self.tab4widget.imagechannelbox.currentIndex()
        setting["t4p4"]=self.tab4widget.directionbox.currentIndex()
        setting["t5p1"]=self.tab5widget.par1Slider.value()
        setting["t5p2"]=self.tab5widget.par2Slider.value()
        setting["t5p3"]=self.tab5widget.par3Slider.value()
        setting["t5p4"]=self.tab5widget.displaymodebox.currentIndex()
        setting["t5p5"]=self.tab5widget.directionbox.currentIndex()
        setting["t6p1"]=self.tab6widget.par1Slider.value()
        setting["t6p2"]=self.tab6widget.par2Slider.value()
        setting["t6p3"]=self.tab6widget.displaymodebox.currentIndex()
        setting["t6p4"]=self.tab6widget.directionbox.currentIndex()
        setting["t7p1"]=self.tab7widget.timeSlider.value()
        setting["t7listindex"]=self.tab7widget.imagelist.currentIndex().column()
        setting["t7tempimagelist"]=self.tab7widget.showlist
        setting["t7storeindex"]=0
        setting["filelist"]=self.data.filelist
        setting["exittime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.thraedhistory = savehistorythread(achepath, setting,self.data, self.list0.currentIndex().column())
        self.thraedhistory.MessageSingle.connect(self.statusBar().showMessage)
        self.thraedhistory.start()

    # todo:读取缓存
    def loadache(self):
        # 读取软件配置信息
        if (os.path.exists(os.getcwd() + "/ache/storepath.ache")):

            f = open(os.getcwd() + "/ache/storepath.ache", 'rb')
            path = pickle.load(f)
            f.close()
            print("path",path)
            self.settingdict["storedir"] = path
            self.storepathline.setText(path)
            # self.tab4widget.changestoredirLinetab4.setText(path)
            # self.changestoredirLinetab4.setText(path)
        else:
            self.settingdict["storedir"] = os.getcwd() + "/store/"

        # 读取数据缓存
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
    def loadacheennding(self, setting):
        # print("data缓存：", setting["selectindex"])
        self.data.filelist = setting["filelist"]
        lasttime = setting["exittime"]
        self.reading = False
        self.list0.selectColumn(setting["list0index"])
        # print("self.list0.currentIndex().column()", self.list0.currentIndex().column())
        self.list0Rowindexchanged()

        self.tab4widget.MultorderSlider.setValue(setting["t4p1"])
        self.tab4widget.pixelnwideSlider.setValue(setting["t4p2"])
        self.tab4widget.imagechannelbox.setCurrentIndex(setting["t4p3"])
        self.tab4widget.directionbox.setCurrentIndex(setting["t4p4"])
        self.tab5widget.par1Slider.setValue(setting["t5p1"])
        self.tab5widget.par2Slider.setValue(setting["t5p2"])
        self.tab5widget.par3Slider.setValue(setting["t5p3"])
        self.tab5widget.displaymodebox.setCurrentIndex(setting["t5p4"])
        self.tab5widget.directionbox.setCurrentIndex(setting["t5p5"])
        self.tab6widget.par1Slider.setValue(setting["t6p1"])
        self.tab6widget.par2Slider.setValue(setting["t6p2"])
        self.tab6widget.displaymodebox.setCurrentIndex(setting["t6p3"])
        self.tab6widget.directionbox.setCurrentIndex(setting["t6p4"])
        self.tab7widget.timeSlider.setValue(setting["t7p1"])

        self.tab7widget.showlist=setting["t7tempimagelist"]
        self.tab7widget.update()
        self.tab7widget.imagelist.selectColumn(setting["t7listindex"])
        self.tab7widget.namelist.selectRow(setting["t7listindex"])
        self.readending()
        self.statusBar().showMessage("已加载缓存！（上次退出时间：" + lasttime + ")")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = main()
    ui.show()
    sys.exit(app.exec_())
