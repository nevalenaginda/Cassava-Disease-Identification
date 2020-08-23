print('Preparation Apps')      
print('Importing Files\n')
import sys
import cv2
import os, os.path
import numpy as np
import source
import glob
import cv2
import numpy as np

import tensorflow
from tensorflow.keras.models import load_model

from GUI import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.uic import loadUi

print('Executing')
#load the trained model
model=  tensorflow.keras.models.load_model('model/model.h5')

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.upload)
        self.ui.pushButton_2.clicked.connect(self.reprocessing)

    def upload(self):
        files_types = "JPG (*.jpg);;BMP(*.bmp);;PNG (*.png);;JPEG (*.jpeg)"
        fileName, _=QFileDialog.getOpenFileName(None, 'Upload Image', './',files_types)
        self.PATH_IMG = fileName
        if fileName:
            pixmap = QPixmap(fileName)
            self.pixmap = pixmap.scaled(261,191)
            QImage = self.pixmap.toImage()
            self.image = QImage.copy()
            self.ui.label_6.setPixmap(QPixmap.fromImage(self.image))            

    def reprocessing(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        img = cv2.imread(self.PATH_IMG )
        img = cv2.resize(img, (224, 224), interpolation = cv2.INTER_CUBIC)
        img = np.reshape(img, (1, 224, 224, 3))
        img = img/255.
        pred = model.predict(img)
        class_num = np.argmax(pred)
        probability = np.max(pred)
        categories = ['Cassava Bacterial Blight (CBB)', 'Cassava Brown Streak Disease (CBSD)', 'Cassava Green Motle (CGM)', 'Cassava Mosaic Disease (CMD)', 'Healthy']
        Jenis_Penyakit = categories[class_num]
        Error = (1-probability)*100
        self.ui.lineEdit.setText(Jenis_Penyakit )
        self.ui.lineEdit_2.setText(str(round(Error,2)) )
        
if __name__=='__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon/logo.ico'))
    w = Window()
    w.show()
    print('Done\n')
    sys.exit(app.exec_())
    
    

'''
This apps is made by Tukang Kode
Instagram: codee_makerr
23.08.2020
Call me for next project
'''
