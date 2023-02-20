from unittest import result
from PyQt6 import QtCore
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import * 
from PyQt6.QtCore import Qt
import sys
import conndb 

class nhanvien(QMainWindow):
    def __init__(self):
        super(nhanvien, self).__init__()
        uic.loadUi("nhanvien.ui",self)
        self.tblNhanVien.setColumnWidth(0,232)
        self.tblNhanVien.setColumnWidth(1,232)
        self.tblNhanVien.setColumnWidth(2,232)
        self.tblNhanVien.setColumnWidth(3,232)
        self.tblNhanVien.clicked.connect(self.getItem)
        self.btnThem.clicked.connect(self.addItem)
        self.btnLamMoi.clicked.connect(self.resetTextBox)
        self.conn = conndb.conndb()
        self.loadData()
        
    def addItem(self):
        MaNhanVien = self.txtMaNhanVien.text()
        HoTen = self.txtTenNhanVien.text()
        GioiTinh = self.cbGioiTinh.currentText()
        ChucVu = self.cbChucVu.currentText()
        
        strsql = "INSERT INTO `nhanvien`(`MaNhanVien`, `TenNhanVien`, `GioiTinh`, `ChucVu`) VALUES ('{0}','{1}','{2}','{3}')".format(MaNhanVien, HoTen, GioiTinh, ChucVu)
        self.conn.queryExecute(strsql)
        self.loadData()
        
    def resetTextBox(self):
        self.txtMaNhanVien.setText('')
        self.txtTenNhanVien.setText('')
        self.cbGioiTinh.setCurrentText('Nam')
        self.cbChucVu.setCurrentText('Nhân Viên')
        
    def getItem(self):
        row = self.tblNhanVien.currentRow()
        MaNhanVien = self.tblNhanVien.item(row,0).text()
        HoTen = self.tblNhanVien.item(row,1).text()
        GioiTinh = self.tblNhanVien.item(row,2).text()
        ChucVu = self.tblNhanVien.item(row,3).text()
        
        self.txtMaNhanVien.setText(MaNhanVien)
        self.txtTenNhanVien.setText(HoTen)
        self.cbGioiTinh.setCurrentText(GioiTinh)
        self.cbChucVu.setCurrentText(ChucVu)
        
        
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
        
        

    