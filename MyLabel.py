from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
from PyQt5 import QtCore
import os
from PyQt5 import QtGui, QtWidgets
import cv2

class Label(QLabel):
    MessageSignal = QtCore.pyqtSignal(str)
    FilepathSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(Label, self).__init__(parent)


    def dragEnterEvent(self, evn):
        evn.accept()

    def dropEvent(self, evn):
        filename = evn.mimeData().text().split("///")[1]
        print(filename)
        print(filename)
        self.FilepathSignal.emit(filename)
