from PyQt5.QtWidgets import QWidget, QApplication, QLabel,QFrame
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import os
from PyQt5 import QtGui, QtWidgets
import cv2

class Label(QLabel):
# class Label(QWidget,QPainter):
    MessageSignal = QtCore.pyqtSignal(str)
    FilepathSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(Label, self).__init__(parent)
        # self.setDragEnabled(True)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, evn):
        evn.accept()

    def dropEvent(self, evn):
        print("event:",evn.mimeData().text())
        if evn.mimeData().text()!="":
            filename = evn.mimeData().text().split("///")[1]
            self.FilepathSignal.emit(filename)


class Lineedit(QLineEdit):
# class Label(QWidget,QPainter):
    MessageSignal = QtCore.pyqtSignal(str)
    FilepathSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(Lineedit, self).__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)


    def dragEnterEvent(self, evn):
        evn.accept()

    def dropEvent(self, evn):
        filename = evn.mimeData().text().split("///")[1]
        self.setText(filename)
        self.FilepathSignal.emit(filename)


class TableWidget(QTableWidget):
# class Label(QWidget,QPainter):
    MessageSignal = QtCore.pyqtSignal(str)
    FilepathSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(TableWidget, self).__init__(parent)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectColumns)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)


    def dragEnterEvent(self, evn):
        evn.accept()

    def dropEvent(self, evn):
        if evn.source() == self:
            print("进入*****")
            cols = set([mi.column() for mi in self.selectedIndexes()])
            targetCol = self.indexAt(evn.pos()).column()
            cols.discard(targetCol)
            cols = sorted(cols)
            if not cols:
                return
            if targetCol == -1:
                targetCol = self.columnCount()
            for _ in range(len(cols)):
                self.insertRow(targetCol)
            colMapping = dict()  # Src row to target row.
            for idx, col in enumerate(cols):
                if col < targetCol:
                    colMapping[col] = targetCol + idx
                else:
                    colMapping[col + len(cols)] = targetCol + idx
            rowCount = self.rowCount()
            for srcCol, tgtCol in sorted(colMapping.iteritems()):
                for row in range(0, rowCount):
                    self.setItem(tgtCol, row, self.takeItem(srcCol, row))
            for col in reversed(sorted(colMapping.iterkeys())):
                self.removeRow(col)
            evn.accept()
            return
        else:
            filename = evn.mimeData().text().split("///")[1]
            self.FilepathSignal.emit(filename)
            print(filename)


class TableWidget3(QTableWidget):
# class Label(QWidget,QPainter):
    MessageSignal = QtCore.pyqtSignal(str)
    FilepathSignal = QtCore.pyqtSignal(str)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def dropEvent(self, event):
        if event.source() == self and (event.dropAction() == Qt.MoveAction or self.dragDropMode() == QAbstractItemView.InternalMove):
            success, row, col, topIndex = self.dropOn(event)
            if success:
                selRows = self.getSelectedRowsFast()

                top = selRows[0]
                # print 'top is %d'%top
                dropRow = row
                if dropRow == -1:
                    dropRow = self.rowCount()
                # print 'dropRow is %d'%dropRow
                offset = dropRow - top
                # print 'offset is %d'%offset

                for i, row in enumerate(selRows):
                    r = row + offset
                    if r > self.rowCount() or r < 0:
                        r = 0
                    self.insertRow(r)
                    # print 'inserting row at %d'%r


                selRows = self.getSelectedRowsFast()
                # print 'selected rows: %s'%selRows

                top = selRows[0]
                # print 'top is %d'%top
                offset = dropRow - top
                # print 'offset is %d'%offset
                for i, row in enumerate(selRows):
                    r = row + offset
                    if r > self.rowCount() or r < 0:
                        r = 0

                    for j in range(self.columnCount()):
                        # print 'source is (%d, %d)'%(row, j)
                        # print 'item text: %s'%self.item(row,j).text()
                        source = QTableWidgetItem(self.item(row, j))
                        # print 'dest is (%d, %d)'%(r,j)
                        self.setItem(r, j, source)

                # Why does this NOT need to be here?
                # for row in reversed(selRows):
                    # self.removeRow(row)

                event.accept()

        else:
            QTableView.dropEvent(event)

    def getSelectedRowsFast(self):
        selRows = []
        for item in self.selectedItems():
            if item.row() not in selRows:
                selRows.append(item.row())
        return selRows

    def droppingOnItself(self, event, index):
        dropAction = event.dropAction()

        if self.dragDropMode() == QAbstractItemView.InternalMove:
            dropAction = Qt.MoveAction

        if event.source() == self and event.possibleActions() & Qt.MoveAction and dropAction == Qt.MoveAction:
            selectedIndexes = self.selectedIndexes()
            child = index
            while child.isValid() and child != self.rootIndex():
                if child in selectedIndexes:
                    return True
                child = child.parent()

        return False

    def dropOn(self, event):
        if event.isAccepted():
            return False, None, None, None

        index = QModelIndex()
        row = -1
        col = -1

        if self.viewport().rect().contains(event.pos()):
            index = self.indexAt(event.pos())
            if not index.isValid() or not self.visualRect(index).contains(event.pos()):
                index = self.rootIndex()

        if self.model().supportedDropActions() & event.dropAction():
            if index != self.rootIndex():
                dropIndicatorPosition = self.position(event.pos(), self.visualRect(index), index)

                if dropIndicatorPosition == QAbstractItemView.AboveItem:
                    row = index.row()
                    col = index.column()
                    # index = index.parent()
                elif dropIndicatorPosition == QAbstractItemView.BelowItem:
                    row = index.row() + 1
                    col = index.column()
                    # index = index.parent()
                else:
                    row = index.row()
                    col = index.column()

            if not self.droppingOnItself(event, index):
                # print 'row is %d'%row
                # print 'col is %d'%col
                return True, row, col, index

        return False, None, None, None

    def position(self, pos, rect, index):
        r = QAbstractItemView.OnViewport
        margin = 2
        if pos.y() - rect.top() < margin:
            r = QAbstractItemView.AboveItem
        elif rect.bottom() - pos.y() < margin:
            r = QAbstractItemView.BelowItem
        elif rect.contains(pos, True):
            r = QAbstractItemView.OnItem

        if r == QAbstractItemView.OnItem and not (self.model().flags(index) & Qt.ItemIsDropEnabled):
            r = QAbstractItemView.AboveItem if pos.y() < rect.center().y() else QAbstractItemView.BelowItem

        return r


class TableWidget2(QTableWidget):
# class Label(QWidget,QPainter):
    MessageSignal = QtCore.pyqtSignal(str)
    FilepathSignal = QtCore.pyqtSignal(str)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setDragDropMode(QAbstractItemView.InternalMove)


    def dropEvent(self, event: QDropEvent):
        print("*******")
        if not event.isAccepted() and event.source() == self:
            print("in*******")
            drop_row = self.drop_on(event)
            print(drop_row)
            rows = sorted(set(item.row() for item in self.selectedItems())) #所有要移动的行
            rows_to_move = [
                [QTableWidgetItem(self.item(row_index, column_index)) for column_index in range(self.columnCount())]
                for row_index in rows]
            print(rows_to_move )
            for row_index in reversed(rows):
                self.removeRow(row_index)
                if row_index < drop_row:
                    drop_row -= 1
            print("row",self.rowCount())
            for row_index, data in enumerate(rows_to_move):
                row_index += drop_row
                self.insertRow(row_index)
                for column_index, column_data in enumerate(data):
                    self.setItem(row_index, column_index, column_data)
            print("row",self.rowCount())
            event.accept()
            for row_index in range(len(rows_to_move)):
                self.item(drop_row + row_index, 0).setSelected(True)
                # self.item(drop_row + row_index, 1).setSelected(True)
            print("row",self.rowCount())
        # super().dropEvent(event)
        print("row", self.rowCount())

    def drop_on(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            return self.rowCount()
            print("drop_on_return:",self.rowCount())

        return index.row() + 1 if self.is_below(event.pos(), index) else index.row()


    def is_below(self, pos, index):
        rect = self.visualRect(index)
        margin = 2
        if pos.y() - rect.top() < margin:
            return False
        elif rect.bottom() - pos.y() < margin:
            return True
        # noinspection PyTypeChecker
        return rect.contains(pos, True) and not (
                    int(self.model().flags(index)) & Qt.ItemIsDropEnabled) and pos.y() >= rect.center().y()


class TableWidget4(QTableWidget):
# class Label(QWidget,QPainter):
    MessageSignal = QtCore.pyqtSignal(str)
    FilepathSignal = QtCore.pyqtSignal(str)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectColumns)
        self.setDragDropMode(QAbstractItemView.InternalMove)


    def dropEvent(self, event):
        if event.source() == self:
            cols = set([mi.column() for mi in self.selectedIndexes()])
            targetCol = self.indexAt(event.pos()).column()
            cols.discard(targetCol)
            cols = sorted(cols)
            if not cols:
                return
            if targetCol == -1:
                targetRow = self.colorCount()
            for _ in range(len(cols)):
                self.insertColumn(targetCol)
            colMapping = dict()  # Src row to target row.
            for idx, col in enumerate(cols):
                if col < targetCol:
                    colMapping[col] = targetCol + idx
                else:
                    colMapping[col + len(cols)] = targetCol + idx
            rowCount = self.rowCount()
            for srcCol, tgtCol in sorted(colMapping.items()):
                for row in range(0, rowCount):
                    self.setItem(tgtCol, row, self.takeItem(srcCol, row))
            for col in reversed(sorted(colMapping.keys())):
                self.removeRow(col)
            event.accept()
            return

    def drop_on(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            return self.columnCount()
            print("drop_on_return:",self.columnCount())

        return index.column() + 1 if self.is_below(event.pos(), index) else index.column()


    def is_below(self, pos, index):
        rect = self.visualRect(index)
        margin = 2
        if pos.x() - rect.left() < margin:
            return False
        elif rect.right() - pos.x() < margin:
            return True
        # noinspection PyTypeChecker
        return rect.contains(pos, True) and not (
                    int(self.model().flags(index)) & Qt.ItemIsDropEnabled) and pos.x() >= rect.center().x()

class editimageLabel(QFrame):
# class editimageLabel(QLabel):
    MessageSignal = QtCore.pyqtSignal(str)
    FilepathSignal = QtCore.pyqtSignal(str)
    def __init__(self):
        super(editimageLabel, self).__init__()
        # self.resize(500, 500)  # 设定窗口大小(根据自己显示图片的大小，可更改)
        # self.setWindowTitle("图片操作")  # 设定窗口名称

        # self.imgPixmap = pix  # 载入图片
        # self.scaledImg = self.imgPixmap.scaled(self.size())  # 初始化缩放图
        self.scaledImg=[]
        self.singleOffset = QPoint(0, 0)  # 初始化偏移值
        self.isLeftPressed = bool(False)  # 图片被点住(鼠标左键)标志位
        self.isImgLabelArea = bool(True)  # 鼠标进入label图片显示区域
        print(self.size(),self.height(),self.width())

    def setPixmap(self,pixmap:QPixmap):
        # self.imgPixmap = pixmap  # 载入图片
        # self.scaledImg = self.imgPixmap.copy()  # 初始化缩放图
        # # self.scaledImg = self.imgPixmap.scaled(self.size())  # 初始化缩放图
        # # self.singleOffset = QPoint(0, 0)
        # self.repaint()


        # self.resize(500, 500)  # 设定窗口大小(根据自己显示图片的大小，可更改)
        # self.setWindowTitle("图片操作")  # 设定窗口名称

        self.imgPixmap = pixmap.copy()  # 载入图片
        # self.scaledImg = self.imgPixmap.scaled(self.size())  # 初始化缩放图
        self.scaledImg = pixmap.copy()  # 初始化缩放图
        self.imageorsize = [(self.width()-pixmap.width())/2,(self.height()-pixmap.height())/2]
        # print(self.imageorsize)
        self.singleOffset = QPoint(self.imageorsize[0],self.imageorsize[1])  # 初始化偏移值
        self.isLeftPressed = bool(False)  # 图片被点住(鼠标左键)标志位
        self.isImgLabelArea = bool(True)  # 鼠标进入label图片显示区域
        self.repaint()

    '''重载绘图: 动态绘图'''

    def paintEvent(self, event):
        if self.scaledImg==[]:
            return
        self.imgPainter = QPainter()  # 用于动态绘制图片
        self.imgFramePainter = QPainter()  # 用于动态绘制图片外线框
        self.imgPainter.begin(self)  # 无begin和end,则将一直循环更新
        self.imgPainter.drawPixmap(self.singleOffset, self.scaledImg)  # 从图像文件提取Pixmap并显示在指定位置
        self.imgFramePainter.setPen(QColor(168, 34, 3))  # 不设置则为默认黑色   # 设置绘图颜色/大小/样式
        self.imgFramePainter.drawRect(10, 10, 480, 480)  # 为图片绘外线狂(向外延展1)
        self.imgPainter.end()  # 无begin和end,则将一直循环更新
        # self.setStyleSheet("background-color:white;border:2px solid red")

    # =============================================================================
    # 图片移动: 首先,确定图片被点选(鼠标左键按下)且未左键释放;
    #          其次,确定鼠标移动;
    #          最后,更新偏移值,移动图片.
    # =============================================================================
    '''重载一下鼠标按下事件(单击)'''

    def mousePressEvent(self, event):
        if self.scaledImg==[]:
            return
        if event.buttons() == QtCore.Qt.LeftButton:  # 左键按下
            # print("鼠标左键单击")  # 响应测试语句
            self.isLeftPressed = True;  # 左键按下(图片被点住),置Ture
            self.preMousePosition = event.pos()  # 获取鼠标当前位置
        # elif event.buttons() == QtCore.Qt.RightButton:  # 右键按下
        #     print("鼠标右键单击")  # 响应测试语句
        # elif event.buttons() == QtCore.Qt.MidButton:  # 中键按下
        #     print("鼠标中键单击")  # 响应测试语句
        # elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.RightButton:  # 左右键同时按下
        #     print("鼠标左右键同时单击")  # 响应测试语句
        # elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.MidButton:  # 左中键同时按下
        #     print("鼠标左中键同时单击")  # 响应测试语句
        # elif event.buttons() == QtCore.Qt.MidButton | QtCore.Qt.RightButton:  # 右中键同时按下
        #     print("鼠标右中键同时单击")  # 响应测试语句
        # elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.MidButton \
        #         | QtCore.Qt.RightButton:  # 左中右键同时按下
        #     print("鼠标左中右键同时单击")  # 响应测试语句

    '''重载一下滚轮滚动事件'''

    def wheelEvent(self, event):
        if self.scaledImg == []:
            return
        print("坐标：",event.x(),event.y())
        print(event.x())
        #        if event.delta() > 0:                                                 # 滚轮上滚,PyQt4
        # This function has been deprecated, use pixelDelta() or angleDelta() instead.
        angle = event.angleDelta() / 8  # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
        angleX = angle.x()  # 水平滚过的距离(此处用不上)
        angleY = angle.y()  # 竖直滚过的距离
        if angleY > 0:  # 滚轮上滚
            scale=10
            # print("鼠标中键上滚",angleY)  # 响应测试语句
            self.scaledImg = self.imgPixmap.scaled(self.scaledImg.width() +self.imgPixmap.width()*0.05, self.scaledImg.height() +self.imgPixmap.height()*0.05)
            # (x / self.scaledImg.)* * addx
            # x-(self.scaledImg./self.imgPixmap*self.scaledImg)

            newWidth = event.x() - (self.scaledImg.width() * (event.x() - self.singleOffset.x())) \
                       / (self.scaledImg.width() - self.imgPixmap.width()*0.05)
            newHeight = event.y() - (self.scaledImg.height() * (event.y() - self.singleOffset.y())) \
                        / (self.scaledImg.height() - self.imgPixmap.height()*0.05)

            # newWidth = event.x() - (self.scaledImg.width() * (event.x() - self.imageorsize[0]) / self.imgPixmap.width())
            # newHeight = event.y() - (self.scaledImg.height() * (event.y() - self.imageorsize[1]) / self.imgPixmap.height())

            self.singleOffset = QPoint(newWidth, newHeight)  # 更新偏移量
            self.repaint()  # 重绘
        else:  # 滚轮下滚
            if self.scaledImg.width() >self.imgPixmap.width()*.15  and self.scaledImg.height()>self.imgPixmap.height()*0.15 :
                # print("原始尺寸：",self.imageorsize[0],self.imageorsize[1])
                # print("鼠标中键下滚")  # 响应测试语句
                self.scaledImg = self.imgPixmap.scaled(self.scaledImg.width() - self.imgPixmap.width() * 0.05,
                                                       self.scaledImg.height() - self.imgPixmap.height() * 0.05)

                newWidth = event.x() - (self.scaledImg.width() * (event.x() - self.singleOffset.x())) \
                           / (self.scaledImg.width() + self.imgPixmap.width()*0.05)
                newHeight = event.y() - (self.scaledImg.height() * (event.y() - self.singleOffset.y())) \
                            / (self.scaledImg.height() + self.imgPixmap.height()*0.05)
                # newWidth = event.x() - (
                #             self.scaledImg.width() * (event.x() - self.imageorsize[0]) / self.imgPixmap.width())
                # newHeight = event.y() - (
                #             self.scaledImg.height() * (event.y() - self.imageorsize[1]) / self.imgPixmap.height())

                self.singleOffset = QPoint(newWidth, newHeight)  # 更新偏移量
                self.repaint()  # 重绘

    '''重载一下鼠标键公开事件'''

    def mouseReleaseEvent(self, event):
        if self.scaledImg==[]:
            return
        if event.buttons() == QtCore.Qt.LeftButton:  # 左键释放
            self.isLeftPressed = False;  # 左键释放(图片被点住),置False
            self.singleOffset = QPoint(event.x(), event.y())
            # print("鼠标左键松开")  # 响应测试语句
        elif event.button() == Qt.RightButton:  # 右键释放
            self.singleOffset = QPoint(self.imageorsize[0],self.imageorsize[1])  # 置为初值
            self.scaledImg = self.imgPixmap.copy()  # 置为初值
            self.repaint()  # 重绘
            # print("鼠标右键松开")  # 响应测试语句

    '''重载一下鼠标移动事件'''

    def mouseMoveEvent(self, event):
        if self.scaledImg==[]:
            return
        if self.isLeftPressed:  # 左键按下
            # print("鼠标左键按下，移动鼠标")  # 响应测试语句
            self.endMousePosition = event.pos() - self.preMousePosition  # 鼠标当前位置-先前位置=单次偏移量
            self.singleOffset = self.singleOffset + self.endMousePosition  # 更新偏移量
            self.preMousePosition = event.pos()  # 更新当前鼠标在窗口上的位置，下次移动用
            self.repaint()  # 重绘


#    '''重载一下鼠标双击事件'''
#    def mouseDoubieCiickEvent(self, event):
#        if event.buttons() == QtCore.Qt.LeftButton:                           # 左键按下
#            self.setText ("双击鼠标左键的功能: 自己定义")
#
#
#    '''重载一下鼠标进入控件事件'''
#    def enterEvent(self, event):
#
#
#    '''重载一下鼠标离开控件事件'''
#    def leaveEvent(self, event):
#

#    '''重载一下鼠标进入控件事件'''
#    def enterEvent(self, event):
#
#
#    '''重载一下鼠标离开控件事件'''
#    def leaveEvent(self, event):
#

    def dragEnterEvent(self, evn):
        evn.accept()

    def dropEvent(self, evn):
        filename = evn.mimeData().text().split("///")[1]
        print(filename)
        print(filename)
        self.FilepathSignal.emit(filename)

    #    '''重载一下鼠标双击事件'''
    #    def mouseDoubieCiickEvent(self, event):
    #        if event.buttons() == QtCore.Qt.LeftButton:                           # 左键按下
    #            self.setText ("双击鼠标左键的功能: 自己定义")
    #
    #
    #    '''重载一下鼠标进入控件事件'''
    #    def enterEvent(self, event):
    #
    #
    #    '''重载一下鼠标离开控件事件'''
    #    def leaveEvent(self, event):
    #

    #    '''重载一下鼠标进入控件事件'''
    #    def enterEvent(self, event):
    #
    #
    #    '''重载一下鼠标离开控件事件'''
    #    def leaveEvent(self, event):
    #

