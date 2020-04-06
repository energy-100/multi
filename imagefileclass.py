
import os
import sys
from PyQt5.QtGui import *



class imageObject():
    def __init__(self):
        self.filelist=[]

    # 添加文件或文件夹
    def addfile(self,filepath,filelist=[]):
        # 判断文件或路径
        # filepath是文件
        if os.path.isfile(filepath):
            print("是文件")
            # filepath是文件
            file={}
            if os.path.splitext(filepath)[1] in [".png",".jpg",".jpeg"]:
                file=self.loadimagefile(filepath)
                self.filelist.append(file)
            return file
        # filepath是文件夹
        elif(os.path.isdir(filepath)):
            print("是文件夹")
            newaddfilelist = []
            files = os.listdir(filepath)
            for f in files:
                #若为子文件夹
                if (os.path.isdir(filepath + '/' + f)):
                    # 排除隐藏文件夹。因为隐藏文件夹过多
                    if (f[0] == '.'):
                        pass
                    else:
                        # 添加非隐藏文件夹
                        pass
                # 若为文件
                # if (os.path.isfile(filepath + '/' + f)):
                else:
                    # 添加文件
                    if (os.path.splitext(f)[1] in [".png",".jpg",".jpeg"]):
                        file=self.loadimagefile(filepath + '/' + f)
                        self.filelist.append(file)
                        newaddfilelist.append(file)

            else:
                return
            return newaddfilelist

    # 读取单文件
    def loadimagefile(self,filepath):
        filedict = {}
        filedir, allfilename = os.path.split(filepath)
        filename, fileextension = os.path.splitext(allfilename)
        filepix = QPixmap(filepath)
        filedict["alldir"] = filepath  # 文件路径
        filedict["parentdir"] = filedir  # 父路径
        filedict["allfilename"] = allfilename  # 全名
        filedict["filename"] = filename  # 文件名
        filedict["fileextension"] = fileextension  # 后缀名
        filedict["pix"] = filepix  # 图片对象
        filedict["width"] = filepix.width()  # 图片宽度
        filedict["depth"] = filepix.depth()  # 图片深度bit
        filedict["height"] = filepix.height()  # 图片高度
        return filedict

    def update(self, data):
            self.filelist=data.filelist
            # self.