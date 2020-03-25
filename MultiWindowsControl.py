
from datetime import datetime
import datetime
import numpy as np
import cv2
import math
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
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
from MyLabel import Label,editimageLabel

# 主对话框
class main(QMainWindow):
    #图片改变信号
    imagechangedSignal = QtCore.pyqtSignal(object)
    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        # 软件配置
        self.setFont(QFont("Microsoft YaHei", 12))
        self.setWindowTitle('辅屏图像控制软件')
        self.setWindowIcon(QIcon('xyjk.png'))
        self.move(20,10)
        # 全局变量
        self.filelist=[]
        self.reading=False

        self.data=imageObject()

        #获取屏幕信息
        desktop = QApplication.desktop()
        self.screen_count = desktop.screenCount()  #屏幕数量
        print( self.screen_count)
        win1 = desktop.screenGeometry(0)  # 参数为显示屏索引，如果安装了两个显示屏，主显示屏索引为0，辅显示屏索引为1
        win2 = desktop.screenGeometry(1)  # 参数为显示屏索引，如果安装了两个显示屏，主显示屏索引为0，辅显示屏索引为1
        # available_rect = desktop.availableGeometry(0)  # 参数为显示屏索引，如果安装了两个显示屏，主显示屏索引为0，辅显示屏索引为1

        #屏幕1Wigget
        self.widget = QWidget()
        self.widget.setGeometry(win1)

        # 主屏幕布局
        self.grid = QGridLayout()


        # 预览辅屏
        # self.lb = QWidget("请选择图片，或将图片文件拖拽至此！")
        # self.lb = Label("请选择图片，或将图片文件拖拽至此！")
        self.lb = Label()
        # self.lb.resize(192*5, 108*5)
        self.lb.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.lb.setStyleSheet("border:1px solid black;background-color:white")
        self.lb.MessageSignal.connect(self.statusBar().showMessage)
        self.lb.FilepathSignal.connect(self.filepathdrop)
        self.lb.setAcceptDrops(True)
        self.lb.setFixedSize(192*5, 108*5)


        # 预览图片
        # self.lb2 = Label("请选择图片，或将图片文件拖拽至此！")
        self.lb2 = editimageLabel()
        # self.lb.resize(192*5, 108*5)
        # self.lb2.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.lb2.setStyleSheet("border:1px solid black;background-color:white")
        self.lb2.MessageSignal.connect(self.statusBar().showMessage)
        self.lb2.FilepathSignal.connect(self.filepathdrop)
        self.lb2.setAcceptDrops(True)
        self.lb2.setFixedSize(192*5, 108*5)

        # self.grid.addWidget(self.lb,0,0,1,4)

        # 设置辅屏对象
        self.lb3 = Label()
        self.lb3.setWindowIcon(QIcon('display.png'))
        self.lb3.setWindowTitle('辅屏窗口')
        self.lb3.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.lb3.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus | Qt.WindowStaysOnTopHint)
        self.lb3.setCursor(Qt.BlankCursor) # 设置鼠标隐藏
        if self.screen_count>1:
            self.lb3.setGeometry(win2)
            self.lb3.show()


        # 预览图片选项卡
        self.imagetab = QTabWidget()
        self.tab1=self.imagetab.addTab(self.lb, "辅屏画面预览")
        self.tab2=self.imagetab.addTab(self.lb2, "图片编辑")
        self.imagetab.setTabIcon(self.tab1, QtGui.QIcon('display.png'))
        self.imagetab.setTabIcon(self.tab2, QtGui.QIcon('picture.png'))
        self.grid.addWidget(self.imagetab, 0, 0, 1, 8)

        # 读取文件按钮
        self.outeditimagebutton = QPushButton("将编辑的图片输出到辅屏")
        self.outeditimagebutton.clicked.connect(lambda: self.outeditimage())
        self.grid.addWidget(self.outeditimagebutton, 1, 0, 1, 1)

        # inflabel
        self.inflabel=QLabel("提示：在图片编辑功能下，鼠标滚轮缩放，按住左键移动，单击右键还原")
        self.grid.addWidget(self.inflabel, 1, 1, 1, 7)
        # 文件路径显示框
        self.filepathline=QLineEdit()
        self.filepathline.setPlaceholderText('请点击右侧按钮选择图片→')
        self.filepathline.setReadOnly(True)
        self.grid.addWidget(self.filepathline,2,0,1,6)

        #读取文件按钮
        self.readfilebutton=QPushButton("添加图片文件")
        self.readfilebutton.clicked.connect(lambda:self.readfile())
        self.grid.addWidget(self.readfilebutton,2,6,1,1)

        # 读取文件夹按钮
        self.readfolderbutton=QPushButton("添加图片文件夹")
        self.readfolderbutton.clicked.connect(lambda:self.readfolder())
        self.grid.addWidget(self.readfolderbutton,2,7,1,1)

        # 删除文件按钮
        self.deletefilebutton=QPushButton("移除图片")
        self.deletefilebutton.clicked.connect(lambda:self.deletefile())
        self.grid.addWidget(self.deletefilebutton,2,8,1,1)

        # 清空文件按钮
        self.deletefilebutton=QPushButton("清空图片")
        self.deletefilebutton.clicked.connect(lambda:self.clearfile())
        self.grid.addWidget(self.deletefilebutton,2,9,1,1)

        #图片预览列表
        self.list0 = QTableWidget()
        self.list0.setRowCount(1)
        self.list0.setColumnCount(1)
        self.list0.setSelectionBehavior(QAbstractItemView.SelectColumns)
        self.list0.clicked.connect(self.list0Rowindexchanged)
        # self.list0.setWindowFlags(Qt.FramelessWindowHint)
        self.list0.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list0.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel) #一行也可以滚动
        self.list0.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)  #一列也可以滚动
        self.list0.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.list0.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.list0.setFixedSize(1250,250)
        self.list0.setFixedHeight(250)
        self.grid.addWidget(self.list0, 3, 0, 1, 10)

        
        #文件列表框
        self.list1 = QTableWidget()
        self.list1.setColumnCount(1)
        self.list1.setRowCount(6)
        self.list1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list1.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.list1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list1.setVerticalHeaderLabels(["文件名","类型","父路径","宽度","高度","色深"])
        self.list1.setHorizontalHeaderLabels(["属性值"])
        self.grid.addWidget(self.list1,0,8,2,2)
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

    def closeEvent(self, event):
        self.savehistory()

    # 读取文件按钮事件
    def readfile(self):
        if self.reading==True:
            self.statusBar().showMessage("正在读取，请稍后重试！")
        else:
            self.reading == True
            path=QFileDialog.getOpenFileName(self, '请选择图片文件', '', 'Image Files (*.jpg *.png *.jpeg)')
            self.runreadfileThread(path)

    # 读取文件夹按钮事件
    def readfolder(self):
        if self.reading==True:
            self.statusBar().showMessage("正在读取，请稍后重试！")
        else:
            self.reading == True
            path=QFileDialog.getExistingDirectory(self, "请选择图片文件目录")
            self.runreadfileThread(path)

    # 拖拽路径进入软件
    def filepathdrop(self,path):
        if self.reading==True:
            self.statusBar().showMessage("正在读取，请稍后重试！")
        else:
            self.runreadfileThread(path)


    # 移除图片
    def deletefile(self):
        if self.list0.currentIndex().column()<0:
            self.statusBar().showMessage("请选择要移除图片")
        else:
            tempindex=self.list0.currentIndex().column()
            file=self.data.filelist.pop(self.list0.currentIndex().column())
            self.savehistory()
            self.readending()
            if tempindex==len(self.data.filelist):
                self.list0.selectColumn(len(self.data.filelist)-1)
            else:
                self.list0.selectColumn(tempindex)
            self.statusBar().showMessage("已移除图片‘"+file["allfilename"]+"’")
            self.list1.clearContents() #清空数据 保留表头
            self.list0Rowindexchanged()

    # 清空图片
    def clearfile(self):
        self.data.filelist=[]
        self.list0.clearContents()
        self.list1.clearContents()
        self.list0.setColumnCount(0)
        self.list0.setRowCount(0)
        self.lb.clear()
        # self.lb2.clear()
        self.lb3.clear()
        self.statusBar().showMessage("已清空图片列表")

    # 将编辑图片输出到辅屏
    def outeditimage(self):
        print(self.lb2.singleOffset.x(),self.lb2.singleOffset.y())
        pix=self.lb2.scaledImg.copy(-self.lb2.singleOffset.x(),-self.lb2.singleOffset.y(),self.lb.width(),self.lb.height())
        lb2x=self.lb2.singleOffset.x()
        lb2y=self.lb2.singleOffset.y()
        lbx=lb2x
        lby=lb2y
        lb3x=lb2x/self.lb2.width()*self.lb3.width()
        lb3y=lb2y/self.lb2.height()*self.lb3.height()
        self.lb.setPixmap(pix)
        self.lb3.setPixmap(pix.scaled(self.lb3.width(),self.lb3.height()))
        self.statusBar().showMessage("已将编辑的图片输出到辅屏！")

    # 启动读取图片线程
    def runreadfileThread(self,path):
        self.reading == True
        self.thraedreadfile = readfilethread(path ,self.data)
        self.thraedreadfile.EnddingSingle.connect(self.readending)
        self.thraedreadfile.MessageSingle.connect(self.statusBar().showMessage)
        self.thraedreadfile.start()
        self.filepathline.setText(path)


    # 读取数据，更新图像列表
    def readending(self):
        self.reading==False
        print(self.data)
        imagelist=[]
        self.list0.clear()
        self.list0.setColumnCount(len(self.data.filelist))
        self.list0.setRowCount(1)
        for i in range(len(self.data.filelist)):
            imagepix=QLabel()
            image=self.data.filelist[i]
            imagepix.setPixmap(image["pix"].scaled(image["width"]/image["height"]*200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            # imagepix.resize(image["width"]/image["height"]*20,20)

            # print("比例：",self.data.filelist[i]["height"]/self.data.filelist[i]["width"])
            # imagepix.setCursor(Qt.CrossCursor)
            imagepix.setAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
            imagelist.append(imagepix)
            self.list0.setCellWidget(0, i, imagepix)
        # 更新自适应宽高尺寸
        self.list0.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.list0.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # 保存状态
        self.savehistory()




    # 点击图像列表
    def list0Rowindexchanged(self):
        if self.list0.currentIndex().column()==-1:
            self.lb.clear()
            # self.lb2.clear()
            self.lb3.clear()
            return

        print("self.fileindex:",self.list0.currentIndex().column())
        self.list1.setItem(0, 0, QTableWidgetItem(str(self.data.filelist[self.list0.currentIndex().column()]["filename"])))
        self.list1.setItem(1, 0, QTableWidgetItem(str(self.data.filelist[self.list0.currentIndex().column()]["fileextension"])))
        self.list1.setItem(2, 0, QTableWidgetItem(str(self.data.filelist[self.list0.currentIndex().column()]["parentdir"])))
        self.list1.setItem(3, 0, QTableWidgetItem(str(self.data.filelist[self.list0.currentIndex().column()]["width"])))
        self.list1.setItem(4, 0, QTableWidgetItem(str(self.data.filelist[self.list0.currentIndex().column()]["height"])))
        self.list1.setItem(5, 0, QTableWidgetItem(str(self.data.filelist[self.list0.currentIndex().column()]["depth"])))

        # 更新铺屏预览图
        image = self.data.filelist[self.list0.currentIndex().column()]
        # 根据辅屏比例修改预览图中图片比例
        imageresize=image["pix"].scaled(image["width"] /1920* self.lb.width(),image["height"] /1080* self.lb.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.lb.setPixmap(imageresize)
        self.lb.setCursor(Qt.CrossCursor)

        # 更新图片预览图
        self.lb2.setPixmap(image["pix"].scaled(self.lb.width(),self.lb.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.lb2.setCursor(Qt.CrossCursor)

        # 更新辅屏
        self.lb3.setPixmap(self.data.filelist[self.list0.currentIndex().column()]["pix"])
        # self.lb3.setCursor(Qt.CrossCursor)
        self.statusBar().showMessage("辅屏图片已更新！")

    # 保存状态函数
    def savehistory(self):
        achepath = os.getcwd() + "/ache/"
        print("缓存：",self.list0.currentIndex().column())
        self.thraedhistory = savehistorythread(achepath, self.data,self.list0.currentIndex().column())
        self.thraedhistory.MessageSingle.connect(self.statusBar().showMessage)
        self.thraedhistory.start()

    # 读取缓存
    def loadache(self):
        achepath = os.getcwd()+"/ache/history.ache"
        print(os.path.exists(achepath))
        print(achepath)
        if (os.path.exists(achepath)):
            self.reading=True
            self.thraedreadhistory = readhostorythread(achepath)
            self.thraedreadhistory.MessageSingle.connect(self.statusBar().showMessage)
            self.thraedreadhistory.EnddingSingle.connect(self.loadacheennding)
            self.thraedreadhistory.start()

    # 加载缓存
    def loadacheennding(self,data):
        print("data缓存：",data["selectindex"])
        self.data=data["data"]
        lasttime=data["exittime"]
        self.reading=False
        self.readending()
        self.list0.selectColumn(data["selectindex"])
        print("self.list0.currentIndex().column()",self.list0.currentIndex().column())
        self.list0Rowindexchanged()
        self.statusBar().showMessage("已加载缓存！（上次退出时间："+lasttime+")")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = main()
    ui.show()
    sys.exit(app.exec_())

