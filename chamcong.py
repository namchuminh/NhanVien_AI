from PyQt6 import QtCore, QtGui
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import * 
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
import sys, os, cv2
import conndb 
import shutil
import numpy as np
from datetime import date, datetime


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    
    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while True:
            ret, cv_img = cap.read()
            if ret:
                gray_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                for (x, y, w, h) in cv2.CascadeClassifier(os.path.dirname(os.path.realpath(__file__)) + '/opencv_haarcascade_data/haarcascade_frontalface_default.xml').detectMultiScale(gray_img, 1.1, 9):
                    cv_img = cv2.rectangle(cv_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                self.change_pixmap_signal.emit(cv_img)
            

class chamcong(QMainWindow):
    def __init__(self):
        super(chamcong, self).__init__()
        uic.loadUi("chamcong.ui",self)
        self.btnThoat.clicked.connect(self.exitForm)
        self.conn = conndb.conndb()
        self.loadData()
        
        self.disply_width = 641
        self.display_height = 491
        
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()
        
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(convert_to_Qt_format)
    
    def loadData(self):
        today = date.today()
        now = datetime.now()
        
        Ngay = str(today).split('-')[2] + '/' + str(today).split('-')[1] + '/' + str(today).split('-')[0]
        ThoiGian = str(now).split(" ")[1].split(".")[0]
    
        self.txtNgayHienTai.setText('Ngày: ' + Ngay)
        self.txtThoiGianHienTai.setText('Thời gian: ' + ThoiGian)
        
    def exitForm(self):
        sys.exit()
        
    
        