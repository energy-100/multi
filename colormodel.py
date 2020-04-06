# self.instructions = QLabel("操作提示:\
#                          \n1.辅屏请设置为扩展模式\
#                          \n2.在图片编辑功能下，鼠标滚轮缩放，按住左键移动，单击右键还原\
#                          \n3.当图像尺寸小于窗口尺寸时，辅屏将居中显示图片\
#                          \n4.在图片编辑功能下，默认将图片填充至整个窗口（包括右键还原的图片），若要以原尺寸输出图片请再次在图片列表中点击图片\
#                          \n5.图片库用于保存软件生成的光栅图，可点击[修改库目录]按钮修改图片库默认位置、点击[打开图片库]打开库目录文件夹\
#                          \n6.生成光栅图时，设置完参数点击[生成图片] 来生成光栅图，当提示栏显示“图片生成成功!”后可以使用[添加到列表]将图片添加到列表")
# # self.instructions.adjustSize()
# self.instructions.setScaledContents(True)
# print("self.instructions.minimumSize()", self.instructions.size().width(), self.instructions.size().height())
# self.instructions.setFixedSize(900, 400)

# self.instructions.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
# *****************************************************
# todo:多阶光栅
self.tab4layout = QGridLayout()
self.lbnewiamge2 = QLabel()
self.lbnewiamge2.setStyleSheet("background-color:white;border:1px solid red")
self.lbnewiamge2.setFixedSize(192 * 4, 108 * 4)
self.tab4layout.addWidget(self.lbnewiamge2, 0, 0, 1, 7)
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

self.imagechannelbox = QComboBox()
self.imagechannelbox.addItems(["四通道", "三通道"])
self.imagechannelbox.setCurrentIndex(0)
self.tab4layout.addWidget(self.imagechannelbox, 1, 6, 1, 1)

self.directionbox = QComboBox()
self.directionbox.addItems(["横向(H)", "纵向(V)"])
self.directionbox.setCurrentIndex(0)
self.tab4layout.addWidget(self.directionbox, 2, 6, 1, 1)

self.makemultorderimagebutton = QPushButton("生成图片")
self.makemultorderimagebutton.clicked.connect(self.makemultorderimagebuttonclicked)
self.tab4layout.addWidget(self.makemultorderimagebutton, 3, 0, 1, 1)
self.addmultordertolistbutton = QPushButton("添加到列表")
self.addmultordertolistbutton.clicked.connect(self.addmultordertolistbuttonclicked)
self.tab4layout.addWidget(self.addmultordertolistbutton, 3, 1, 1, 1)
self.addtostoretab4button = QPushButton("保存到图片库")
self.addtostoretab4button.clicked.connect(self.addtostoretab4buttonclicked)
self.tab4layout.addWidget(self.addtostoretab4button, 3, 2, 1, 1)
self.changestoredirbuttontab4 = QPushButton("修改库目录")
self.changestoredirbuttontab4.clicked.connect(self.changestoredirbuttonclick)
self.tab4layout.addWidget(self.changestoredirbuttontab4, 3, 3, 1, 1)
self.changestoredirLinetab4 = QLineEdit()
self.changestoredirLinetab4.setText(self.storedir)
self.changestoredirLinetab4.setReadOnly(True)
self.tab4layout.addWidget(self.changestoredirLinetab4, 3, 4, 1, 3)

# self.line1wide.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
# self.line1wide.setValue(5)
# self.tab3layout.addWidget(self.changestoredirbutton, 3, 3, 1, 1)
# self.changestoredirLine = QLineEdit()
# self.changestoredirLine.setText(self.storedir)
# self.changestoredirLine.setReadOnly(True)
# self.tab3layout.addWidget(self.changestoredirLine, 3, 4, 1, 3)
# *****************************************************

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

self.addtolistbutton = QPushButton("添加到列表")
self.addtolistbutton.clicked.connect(self.addtolistbuttonclicked)
self.tab3layout.addWidget(self.addtolistbutton, 3, 0, 1, 1)
self.addtolistandoutbutton = QPushButton("添加到列表并输出")
self.addtolistandoutbutton.clicked.connect(self.addtolistandoutbuttonclicked)
self.tab3layout.addWidget(self.addtolistandoutbutton, 3, 1, 1, 1)
self.savetostorebutton = QPushButton("保存到图片库")
self.savetostorebutton.clicked.connect(self.savetostorebuttonclicked)
self.tab3layout.addWidget(self.savetostorebutton, 3, 2, 1, 1)
self.changestoredirbutton = QPushButton("修改库目录")
self.changestoredirbutton.clicked.connect(self.changestoredirbuttonclick)
self.tab3layout.addWidget(self.changestoredirbutton, 3, 3, 1, 1)
self.changestoredirLine = QLineEdit()
self.changestoredirLine.setText(self.storedir)
self.changestoredirLine.setReadOnly(True)
self.tab3layout.addWidget(self.changestoredirLine, 3, 4, 1, 3)
self.makeimagebutton = QPushButton("生成图片")
self.makeimagebutton.clicked.connect(self.makeimagebottonclicked)
self.tab3layout.addWidget(self.makeimagebutton, 1, 7, 1, 1)
# ****************************************************

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


def addtolistandoutbuttonclicked(self):
    pass


def savetostorebuttonclicked(self):
    pass
