from distutils.command import check
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
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
from tinhluong import tinhluong

np.set_printoptions(suppress=True)
model = load_model("./model/keras_Model.h5", compile=False)
class_names = open("./model/labels.txt", "r").readlines()
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    _go = True
    def run(self):
        self._go = True
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._go:
            ret, cv_img = cap.read()
            if ret:
                gray_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                for (x, y, w, h) in cv2.CascadeClassifier(os.path.dirname(os.path.realpath(__file__)) + '/opencv_haarcascade_data/haarcascade_frontalface_default.xml').detectMultiScale(gray_img, 1.1, 9):
                    cv_img = cv2.rectangle(cv_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    face = cv_img[y:y+h, x:x+w]
                    cv2.imwrite(os.path.dirname(os.path.realpath(__file__)) + '/img/checkMark/faceCheck.jpg', face)
                self.change_pixmap_signal.emit(cv_img)
                
    def stop(self):
        self._go = False
        

class chamcong(QMainWindow):
    def __init__(self, widget):
        super(chamcong, self).__init__()
        uic.loadUi("chamcong.ui",self)
        self.widget = widget
        self.btnThoat.clicked.connect(self.exitForm)
        self.btnChamCong.clicked.connect(self.checkMark)
        self.windowNhanVien.clicked.connect(self.switchNhanVien)
        self.windowTinhLuong.clicked.connect(self.switchTinhLuong)
        self.btnMoCamera.clicked.connect(self.openCamera)
        self.btnDongCamera.clicked.connect(self.closeCamera)
        self.conn = conndb.conndb()
        self.loadData()
        
        self.disply_width = 641
        self.display_height = 491
        # create the video capture thread
        self.thread = VideoThread()

    
    def checkMark(self):
        try:
            image = Image.open(os.path.dirname(os.path.realpath(__file__)) + '/img/checkMark/faceCheck.jpg').convert("RGB")
            # resizing the image to be at least 224x224 and then cropping from the center
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
            # turn the image into a numpy array
            image_array = np.asarray(image)
            # Normalize the image
            normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
            # Load the image into the array
            data[0] = normalized_image_array
            # Predicts the model
            prediction = model.predict(data)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]
            

            MaNhanVien = class_name[2:].strip()
            strsql = f"SELECT * FROM nhanvien WHERE MaNhanVien = '{MaNhanVien}'"
            result = self.conn.queryResult(strsql)
            
            TenNhanVien = str(result[0][1])
            
            if len(result) == 0:
                dir_path = os.path.dirname(os.path.realpath(__file__))
                pixmap = QPixmap(dir_path + '\\' + 'img\\avatar\\user.png')
                self.lblAvatar.setPixmap(pixmap)
                self.lblMaNhanVien.setText('')
                self.lblTenNhanVien.setText('')
                self.lblGioiTinh.setText('')
                self.lblChucVu.setText('')
                self.lblNgayChamCong.setText('')
                self.lblThoiGian.setText('')
                self.lblTrangThai.setText('')
                self.messageBoxInfo("Thông báo!", "Nhân viên không tồn tại!")
            else:
                today = date.today()
                now = datetime.now()
                
                Ngay = str(today).split('-')[2] + '/' + str(today).split('-')[1] + '/' + str(today).split('-')[0]
                ThoiGian = str(now).split(" ")[1].split(".")[0]
                
                dir_path = os.path.dirname(os.path.realpath(__file__))
                pixmap = QPixmap(dir_path + '\\' + 'img\\avatar\\' + result[0][4])
                self.lblAvatar.setPixmap(pixmap)
                self.lblMaNhanVien.setText(str(result[0][0]))
                self.lblTenNhanVien.setText(str(result[0][1]))
                self.lblGioiTinh.setText(str(result[0][2]))
                self.lblChucVu.setText(str(result[0][3]))
                self.lblNgayChamCong.setText(Ngay)
                self.lblThoiGian.setText(ThoiGian)
                self.lblTrangThai.setText('Đã Chấm Công')
                
                strsql_select = f"SELECT * FROM tinhluong WHERE MaNhanVien = '{MaNhanVien}' ORDER BY MaTinhLuong DESC"
                result_select = self.conn.queryResult(strsql_select)

                if len(result_select) == 0:
                    self.messageBoxInfo("Thông báo!", "Nhân viên chưa được phép chấm công!\nVui lòng thêm nhân viên vào TÍNH LƯƠNG để chấm công!")
                else:
                    Thuong = int(result_select[0][3])
                    Phat = int(result_select[0][4])
                    HeSoLuong = int(result_select[0][5])
                    
                    strsql_check = f"SELECT COUNT(*) FROM tinhluong WHERE MaNhanVien = '{MaNhanVien}' AND ThoiGian = CURDATE();"
                    result_check = self.conn.queryResult(strsql_check)
                    
                    
                    if int(result_check[0][0]) == 1:
                        self.messageBoxInfo("Thông báo!", f"Nhân viên {TenNhanVien} đã được chấm công trước đó!")
                    else:
                        strsql_insert = f"INSERT INTO `tinhluong`(`MaNhanVien`, `SoCong`, `Thuong`, `Phat`, `HeSoLuong`) VALUES ('{MaNhanVien}', 1, {Thuong}, {Phat}, {HeSoLuong})"
                        result_insert = self.conn.queryExecute(strsql_insert)
                        self.messageBoxInfo("Thông báo!", f"Chấm công cho nhân viên: {TenNhanVien} thành công!!")
        except:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            pixmap = QPixmap(dir_path + '\\' + 'img\\avatar\\user.png')
            self.lblAvatar.setPixmap(pixmap)
            self.lblMaNhanVien.setText('')
            self.lblTenNhanVien.setText('')
            self.lblGioiTinh.setText('')
            self.lblChucVu.setText('')
            self.lblNgayChamCong.setText('')
            self.lblThoiGian.setText('')
            self.lblTrangThai.setText('')
            self.messageBoxInfo("Thông báo!", "Không nhận dạng được khuân mặt!")
            return
    
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
        
        
        
    def messageBoxInfo(self, title, text):
        reply = QMessageBox()
        reply.setWindowTitle(title)
        reply.setText(text)
        reply.setStandardButtons(QMessageBox.StandardButton.Ok)

        x = reply.exec()
        
    def exitForm(self):
        sys.exit()
        
    def switchNhanVien(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() - 2)
    
    def switchTinhLuong(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() - 1)
        
    def openCamera(self):
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()
        
        self.btnMoCamera.setEnabled(False)
        self.btnDongCamera.setEnabled(True)
        self.btnChamCong.setEnabled(True)
        
    def closeCamera(self):
        self.thread.stop()
        self.btnMoCamera.setEnabled(True)
        self.btnDongCamera.setEnabled(False)
        self.btnChamCong.setEnabled(False)