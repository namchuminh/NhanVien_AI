from PyQt6 import QtCore
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import * 
from PyQt6.QtCore import Qt
import sys, os
import conndb 
import shutil

class nhanvien(QMainWindow):
    def __init__(self):
        super(nhanvien, self).__init__()
        uic.loadUi("nhanvien.ui",self)
        self.image= ""
        self.pixmap = QPixmap("./img/avatar/user.png")
        self.lblAvatar.setPixmap(self.pixmap)
        self.tblNhanVien.setColumnWidth(0,232)
        self.tblNhanVien.setColumnWidth(1,232)
        self.tblNhanVien.setColumnWidth(2,232)
        self.tblNhanVien.setColumnWidth(3,232)
        self.tblNhanVien.clicked.connect(self.getItem)
        self.btnThem.clicked.connect(self.addItem)
        self.btnLamMoi.clicked.connect(self.resetTextBox)
        self.btnChonAnh.clicked.connect(self.chooseImage)
        self.btnSua.clicked.connect(self.updateItem)
        self.btnXoa.clicked.connect(self.deleteItem)
        self.btnTimKiem.clicked.connect(self.searchItem)
        self.btnThoat.clicked.connect(self.exitForm)
        self.conn = conndb.conndb()
        self.loadData()
        
    def addItem(self):
        if self.txtMaNhanVien.text() == "" or self.txtTenNhanVien.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        MaNhanVien = self.txtMaNhanVien.text()
        HoTen = self.txtTenNhanVien.text()
        GioiTinh = self.cbGioiTinh.currentText()
        ChucVu = self.cbChucVu.currentText()
        Avatar = 'user.png' if self.image == "" else self.image
        
        strsql = "INSERT INTO `nhanvien`(`MaNhanVien`, `TenNhanVien`, `GioiTinh`, `ChucVu`, `Avatar`) VALUES ('{0}','{1}','{2}','{3}', '{4}')".format(MaNhanVien, HoTen, GioiTinh, ChucVu, Avatar)
        self.conn.queryExecute(strsql)
        
        self.resetTextBox()
        self.loadData()
    
    def updateItem(self):
        if self.txtMaNhanVien.text() == "" or self.txtTenNhanVien.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        MaNhanVien = self.txtMaNhanVien.text()
        strsql = f"SELECT * FROM nhanvien WHERE MaNhanVien = '{MaNhanVien}'"
        result = self.conn.queryResult(strsql)
        HoTen = self.txtTenNhanVien.text()
        GioiTinh = self.cbGioiTinh.currentText()
        ChucVu = self.cbChucVu.currentText()
        Avatar = result[0][4] if self.image == "" else self.image
        
        strsql = f"UPDATE `nhanvien` SET `TenNhanVien`='{HoTen}',`GioiTinh`='{GioiTinh}',`ChucVu`='{ChucVu}',`Avatar`='{Avatar}' WHERE `MaNhanVien`='{MaNhanVien}'"
        self.conn.queryExecute(strsql)
        
        self.resetTextBox()
        self.loadData()
    
    def deleteItem(self):
        if self.txtMaNhanVien.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng chọn nhân viên cần xóa!")
            return
        MaNhanVien = self.txtMaNhanVien.text()
        strsql = f"DELETE FROM `nhanvien` WHERE MaNhanVien = '{MaNhanVien}'"
        self.conn.queryExecute(strsql)
        
        self.resetTextBox()
        self.loadData()
    
    def searchItem(self):
        if self.txtTimKiem.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui nhập tên nhân viên cần tìm!")
            return
        
        TenNhanVien = self.txtTimKiem.text()
        strsql = f"SELECT * FROM nhanvien WHERE TenNhanVien LIKE '%{TenNhanVien}%'"
        result = self.conn.queryResult(strsql)
        
        row = 0
        self.tblNhanVien.setRowCount(len(result))
        for user in result:
            self.tblNhanVien.setItem(row, 0, QtWidgets.QTableWidgetItem(str(user[0])))
            self.tblNhanVien.setItem(row, 1, QtWidgets.QTableWidgetItem(str(user[1])))
            self.tblNhanVien.setItem(row, 2, QtWidgets.QTableWidgetItem(str(user[2])))
            self.tblNhanVien.setItem(row, 3, QtWidgets.QTableWidgetItem(str(user[3])))
            row = row + 1
        
        self.pixmap = QPixmap("./img/avatar/user.png")
        self.lblAvatar.setPixmap(self.pixmap)
        self.txtMaNhanVien.setEnabled(True)
        
        
    
    def chooseImage(self):
        imgLink = QFileDialog.getOpenFileName(filter='*.jpg *.png')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        avatar = dir_path + '\\' + 'img\\avatar\\' + imgLink[0].split('/')[-1]
        shutil.copyfile(imgLink[0], avatar)
        self.pixmap = QPixmap(imgLink[0])
        self.lblAvatar.setPixmap(self.pixmap)
        self.image = imgLink[0].split('/')[-1]
        
    def resetTextBox(self):
        self.txtMaNhanVien.setText('')
        self.txtTenNhanVien.setText('')
        self.cbGioiTinh.setCurrentText('Nam')
        self.cbChucVu.setCurrentText('Nhân Viên')
        self.pixmap = QPixmap("./img/avatar/user.png")
        self.lblAvatar.setPixmap(self.pixmap)
        
        self.txtMaNhanVien.setEnabled(True)
        self.btnThem.setEnabled(True)
        self.loadData()
        
    def getItem(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        row = self.tblNhanVien.currentRow()
        MaNhanVien = self.tblNhanVien.item(row,0).text()
        HoTen = self.tblNhanVien.item(row,1).text()
        GioiTinh = self.tblNhanVien.item(row,2).text()
        ChucVu = self.tblNhanVien.item(row,3).text()
        
        strsql = f"SELECT * FROM nhanvien WHERE MaNhanVien = '{MaNhanVien}'"
        result = self.conn.queryResult(strsql)

        self.pixmap = QPixmap(dir_path + '\\' + 'img\\avatar\\' + result[0][4])
        self.lblAvatar.setPixmap(self.pixmap)
        self.txtMaNhanVien.setText(MaNhanVien)
        self.txtTenNhanVien.setText(HoTen)
        self.cbGioiTinh.setCurrentText(GioiTinh)
        self.cbChucVu.setCurrentText(ChucVu)
        
        self.txtMaNhanVien.setEnabled(False)
        self.btnThem.setEnabled(False)
        
        
    def loadData(self):
        strsql = "SELECT * FROM nhanvien"
        result = self.conn.queryResult(strsql)
        
        row = 0
        self.tblNhanVien.setRowCount(len(result))
        for user in result:
            self.tblNhanVien.setItem(row, 0, QtWidgets.QTableWidgetItem(str(user[0])))
            self.tblNhanVien.setItem(row, 1, QtWidgets.QTableWidgetItem(str(user[1])))
            self.tblNhanVien.setItem(row, 2, QtWidgets.QTableWidgetItem(str(user[2])))
            self.tblNhanVien.setItem(row, 3, QtWidgets.QTableWidgetItem(str(user[3])))
            row = row + 1
        
        self.txtMaNhanVien.setEnabled(True)
        
    def exitForm(self):
        sys.exit()
    
    def messageBoxInfo(self, title, text):
        reply = QMessageBox()
        reply.setWindowTitle(title)
        reply.setText(text)
        reply.setStandardButtons(QMessageBox.StandardButton.Ok)

        x = reply.exec()
    
        

    