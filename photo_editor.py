from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QGroupBox, QRadioButton, QHBoxLayout, QButtonGroup, QListWidget, QTextEdit, QLineEdit, QInputDialog, QFileDialog
from PyQt5.QtGui import QPixmap
import os
from PIL import Image
from PIL.ImageFilter import SHARPEN
app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Easy Editor')
main_win.resize(700,400)
noteslist = QListWidget()
lbimage = QLabel('Картинка')
but1 = QPushButton('Папка')
but2 = QPushButton('Лево')
but3 = QPushButton('Право')
but4 = QPushButton('Зеркало')
but5 = QPushButton('Резкость')
but6 = QPushButton('Ч/Б')
row = QHBoxLayout()
layout1 = QVBoxLayout()
layout2 = QVBoxLayout()
layout3 = QHBoxLayout()
layout1.addWidget(but1)
layout1.addWidget(noteslist)
layout2.addWidget(lbimage, 95)
layout3.addWidget(but2)
layout3.addWidget(but3)
layout3.addWidget(but4)
layout3.addWidget(but5)
layout3.addWidget(but6)
layout2.addLayout(layout3)
row.addLayout(layout1)
row.addLayout(layout2)
main_win.setLayout(row)
workdir = ''
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
def filter(files, extensions):
    result = list()
    for x in files:
        for y in extensions:
            if x.endswith(y):
                result.append(x)
    return result
def ShowFilenamesList():
    chooseWorkdir()
    extensions = ['.jpeg', '.png', '.gif', '.bmp', '.jpg']
    files = filter(os.listdir(workdir), extensions)
    noteslist.clear()
    for i in files:
        noteslist.addItem(i)
but1.clicked.connect(ShowFilenamesList)
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.folder = 'Modified/'
    def loadImage(self, filename):
        self.filename = filename
        imagepath = os.path.join(workdir,filename)
        self.image = Image.open(imagepath)
    def showImage(self, path):
        lbimage.hide()
        pixmapimage = QPixmap(path)
        w,h = lbimage.width(), lbimage.height()
        pixmapimage = pixmapimage.scaled(w,h, Qt.KeepAspectRatio)
        lbimage.setPixmap(pixmapimage)
        lbimage.show()
    def saveImage(self):
        path = os.path.join(workdir, self.folder)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        imagepath = os.path.join(workdir,self.folder,self.filename)
        self.showImage(imagepath)
    def left_side(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        imagepath = os.path.join(workdir, self.folder, self.filename)
        self.showImage(imagepath)
    def right_side(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        imagepath = os.path.join(workdir, self.folder, self.filename)
        self.showImage(imagepath)
    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        imagepath = os.path.join(workdir, self.folder, self.filename)
        self.showImage(imagepath)
    def do_sharp(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        imagepath = os.path.join(workdir, self.folder, self.filename)
        self.showImage(imagepath)
def showChosenImage():
    if noteslist.currentRow()>=0:
        filename = noteslist.currentItem().text()
        workimage.loadImage(filename)
        imagepath = os.path.join(workdir, workimage.filename)
        workimage.showImage(imagepath)

workimage = ImageProcessor()
noteslist.currentRowChanged.connect(showChosenImage)
but6.clicked.connect(workimage.do_bw)
but2.clicked.connect(workimage.left_side)
but3.clicked.connect(workimage.right_side)
but4.clicked.connect(workimage.do_mirror)
but5.clicked.connect(workimage.do_sharp)

                           


main_win.show()
app.exec()

