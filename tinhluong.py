from PyQt6 import QtCore
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import * 
from PyQt6.QtCore import Qt
import sys, os
import conndb 
import shutil

class tinhluong(QMainWindow):
    def __init__(self):
        super(tinhluong, self).__init__()
        uic.loadUi("tinhluong.ui",self)
        self.tblTinhLuong.setColumnWidth(0,103)
        self.tblTinhLuong.setColumnWidth(1,103)
        self.tblTinhLuong.setColumnWidth(2,103)
        self.tblTinhLuong.setColumnWidth(3,103)
        self.tblTinhLuong.setColumnWidth(4,103)
        self.tblTinhLuong.setColumnWidth(5,103)
        self.tblTinhLuong.setColumnWidth(6,103)
        self.tblTinhLuong.setColumnWidth(7,103)
        self.tblTinhLuong.setColumnWidth(8,103)
        self.tblTinhLuong.clicked.connect(self.getItem)
        self.btnThoat.clicked.connect(self.exitForm)
        self.btnThem.clicked.connect(self.addItem)
        self.btnCapNhat.clicked.connect(self.updateItem)
        self.btnLamMoi.clicked.connect(self.resetItem)
        self.btnXemTheoThang.clicked.connect(self.viewByMonth)
        self.cbMaNhanVien.activated.connect(self.chooseMaNhanVien)
        self.btnTinhLuong.clicked.connect(self.sumWage)
        self.conn = conndb.conndb()
        self.loadData()
        self.loadMaNhanVien()
        
    def addItem(self):
        if self.txtMaNhanVien.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng nhập mã nhân viên cần thêm!")
            return
        
        MaNhanVien = self.txtMaNhanVien.text()
        
        strsql = f"SELECT * FROM nhanvien WHERE MaNhanVien = '{MaNhanVien}'"
        result = self.conn.queryResult(strsql)
        
        if len(result) == 0:
            self.messageBoxInfo("Thông Báo", f"Không có nhân viên nào có mã {MaNhanVien}!")
            return
        
        strsql_tinhluong = f"SELECT * FROM tinhluong WHERE MaNhanVien = '{MaNhanVien}'"
        result_tinhluong = self.conn.queryResult(strsql_tinhluong)
        
        if len(result_tinhluong) >= 1:
            self.messageBoxInfo("Thông Báo", f"Nhân viên {MaNhanVien} này đã được thêm vào tính lương!")
            return
        
        Thuong = self.txtThuong.text()
        Phat = self.txtPhat.text()
        HeSoLuong = self.txtHeSoLuong.text()
        strsql_insert = f"INSERT INTO `tinhluong`(`MaNhanVien`, `Thuong`, `Phat`, `HeSoLuong`) VALUES ('{MaNhanVien}','{Thuong}','{Phat}','{HeSoLuong}')"
        result_tinhluong = self.conn.queryExecute(strsql_insert)
        
        self.loadData()
        self.messageBoxInfo("Thông Báo", f"Thành công!")
    
    def getItem(self):
        row = self.tblTinhLuong.currentRow()
        MaNhanVien = self.tblTinhLuong.item(row,0).text()
        HeSoLuong = self.tblTinhLuong.item(row,7).text()
        Thuong = self.tblTinhLuong.item(row,5).text()
        Phat = self.tblTinhLuong.item(row,6).text()
        Thang = self.tblTinhLuong.item(row,8).text()
        
        strsql = f"SELECT DISTINCT MONTH(tinhluong.ThoiGian) FROM tinhluong WHERE tinhluong.MaNhanVien = '{MaNhanVien}' AND YEAR(ThoiGian) = YEAR(CURDATE());"
        result = self.conn.queryResult(strsql)
        
        self.cbChonThang3.clear()
        for month in result:
            self.cbChonThang3.addItem("Tháng " + str(month[0]))
        
        self.txtMaNhanVien.setText(MaNhanVien)
        self.txtHeSoLuong.setText(HeSoLuong)
        self.txtThuong.setText(Thuong)
        self.txtPhat.setText(Phat)
        self.cbChonThang3.setCurrentText(Thang)
            
        self.btnThem.setEnabled(False)
        self.txtMaNhanVien.setEnabled(False)
        self.cbChonThang3.setEnabled(True)
    
    def updateItem(self):
        if self.txtMaNhanVien.text() == "":
            self.messageBoxInfo("Thông Báo", "Vui lòng chọn nhân viên cần cập nhật!")
            return
        
        MaNhanVien = self.txtMaNhanVien.text()
        Thuong = self.txtThuong.text()
        Phat = self.txtPhat.text()
        HeSoLuong = self.txtHeSoLuong.text()
        Thang = self.cbChonThang3.currentText().split(" ")[1]
        
        strsql = f"UPDATE `tinhluong` SET `Thuong`='{Thuong}',`Phat`='{Phat}',`HeSoLuong`='{HeSoLuong}' WHERE `MaNhanVien`='{MaNhanVien}' AND MONTH(ThoiGian) = '{Thang}' AND YEAR(ThoiGian) = YEAR(CURDATE())"
        result = self.conn.queryExecute(strsql)
        
        self.loadData()
        self.messageBoxInfo("Thông Báo", f"Cập Nhật Thành công!")
    
    def viewByMonth(self):
        ChonThang = self.cbChonThang2.currentText().split(" ")[1]
        strsql = f"SELECT nhanvien.MaNhanVien AS MaNhanVien, nhanvien.TenNhanVien AS TenNhanVien, nhanvien.GioiTinh AS GioiTinh, nhanvien.ChucVu AS ChucVu, SUM(tinhluong.SoCong) AS SoCong, tinhluong.Thuong AS Thuong, tinhluong.Phat AS Phat, tinhluong.HeSoLuong, tinhluong.ThoiGian FROM nhanvien, tinhluong WHERE nhanvien.MaNhanVien = tinhluong.MaNhanVien AND MONTH(tinhluong.ThoiGian) = '{ChonThang}' AND YEAR(tinhluong.ThoiGian) = YEAR(CURDATE()) GROUP BY tinhluong.MaNhanVien;"
        result = self.conn.queryResult(strsql)

        row = 0
        self.tblTinhLuong.setRowCount(len(result))
        for user in result:
            
            Thang = "Tháng " + str(user[8]).split('-')[1][-1] if int(str(user[8]).split('-')[1]) < 10 else str(user[8]).split('-')[1]
            
            self.tblTinhLuong.setItem(row, 0, QtWidgets.QTableWidgetItem(str(user[0])))
            self.tblTinhLuong.setItem(row, 1, QtWidgets.QTableWidgetItem(str(user[1])))
            self.tblTinhLuong.setItem(row, 2, QtWidgets.QTableWidgetItem(str(user[2])))
            self.tblTinhLuong.setItem(row, 3, QtWidgets.QTableWidgetItem(str(user[3])))
            self.tblTinhLuong.setItem(row, 4, QtWidgets.QTableWidgetItem(str(user[4])))
            self.tblTinhLuong.setItem(row, 5, QtWidgets.QTableWidgetItem(str(user[5])))
            self.tblTinhLuong.setItem(row, 6, QtWidgets.QTableWidgetItem(str(user[6])))
            self.tblTinhLuong.setItem(row, 7, QtWidgets.QTableWidgetItem(str(user[7])))
            self.tblTinhLuong.setItem(row, 8, QtWidgets.QTableWidgetItem(Thang))
            row = row + 1  

    def resetItem(self):
        self.txtMaNhanVien.setText('')
        self.txtHeSoLuong.setText('0')
        self.txtThuong.setText('0')
        self.txtPhat.setText('0')
        
        self.btnThem.setEnabled(True)
        self.txtMaNhanVien.setEnabled(True)
        self.cbChonThang3.setEnabled(False)
        
    def loadMaNhanVien(self):
        strsql = "SELECT DISTINCT tinhluong.MaNhanVien FROM tinhluong;"
        result = self.conn.queryResult(strsql)
        
        MaNhanVien = result[0][0]
        
        self.cbMaNhanVien.clear()
        for manhanvien in result:
            self.cbMaNhanVien.addItem(str(manhanvien[0]))
        
        strsql_month = f"SELECT DISTINCT MONTH(tinhluong.ThoiGian) FROM tinhluong WHERE tinhluong.MaNhanVien = '{MaNhanVien}' AND YEAR(ThoiGian) = YEAR(CURDATE());"
        result_month = self.conn.queryResult(strsql_month)
        
        self.cbChonThang.clear()
        for month in result_month:
            self.cbChonThang.addItem("Tháng " + str(month[0]))
        
    def chooseMaNhanVien(self):
        MaNhanVien = self.cbMaNhanVien.currentText()
        strsql_month = f"SELECT DISTINCT MONTH(tinhluong.ThoiGian) FROM tinhluong WHERE tinhluong.MaNhanVien = '{MaNhanVien}' AND YEAR(ThoiGian) = YEAR(CURDATE());"
        result_month = self.conn.queryResult(strsql_month)
        
        self.cbChonThang.clear()
        for month in result_month:
            self.cbChonThang.addItem("Tháng " + str(month[0]))
    
    def sumWage(self):
        MaNhanVien = self.cbMaNhanVien.currentText()
        Thang = self.cbChonThang.currentText().split(" ")[1]
    
        strsql = f"SELECT nhanvien.MaNhanVien AS MaNhanVien, nhanvien.TenNhanVien AS TenNhanVien, nhanvien.GioiTinh AS GioiTinh, nhanvien.ChucVu AS ChucVu, SUM(tinhluong.SoCong) AS SoCong, tinhluong.Thuong AS Thuong, tinhluong.Phat AS Phat, tinhluong.HeSoLuong, tinhluong.ThoiGian FROM nhanvien, tinhluong WHERE nhanvien.MaNhanVien = tinhluong.MaNhanVien AND tinhluong.MaNhanVien = '{MaNhanVien}' AND MONTH(tinhluong.ThoiGian) = '{Thang}' AND YEAR(tinhluong.ThoiGian) = YEAR(CURDATE()) GROUP BY tinhluong.MaNhanVien;"
        result = self.conn.queryResult(strsql)
        
        SoCong = float(result[0][4])
        Thuong = float(result[0][5])
        Phat = float(result[0][6])
        HeSoLuong = float(result[0][7])
        TongTien = 284599.0 #(SoCong * HeSoLuong) + Thuong - Phat
        
        if len(str(TongTien)) == 4:
            TongTien = str(TongTien) + "00"
        elif len(str(TongTien)) == 5:
            TongTien = str(TongTien) + "00"
        elif len(str(TongTien)) == 6:
            TongTien = str(TongTien)[0] + "." + str(TongTien)[1:4] + ".000"
        elif len(str(TongTien)) == 7:
            TongTien = str(TongTien)[0:2] + "." + str(TongTien)[2:5] + ".000"
        elif len(str(TongTien)) == 8:
            TongTien = str(TongTien)[0:3] + "." + str(TongTien)[3:6] + ".000"
            
        self.lblSoCong.setText(str(SoCong))
        self.lblThuong.setText(str(Thuong))
        self.lblPhat.setText(str(Phat))
        self.lblHeSoLuong.setText(str(HeSoLuong))
        self.lblTongTien.setText(TongTien)
        
    def loadData(self):
        strsql = "SELECT nhanvien.MaNhanVien AS MaNhanVien, nhanvien.TenNhanVien AS TenNhanVien, nhanvien.GioiTinh AS GioiTinh, nhanvien.ChucVu AS ChucVu, SUM(tinhluong.SoCong) AS SoCong, tinhluong.Thuong AS Thuong, tinhluong.Phat AS Phat, tinhluong.HeSoLuong, tinhluong.ThoiGian FROM nhanvien, tinhluong WHERE nhanvien.MaNhanVien = tinhluong.MaNhanVien AND MONTH(tinhluong.ThoiGian) = MONTH(CURDATE()) AND YEAR(tinhluong.ThoiGian) = YEAR(CURDATE()) GROUP BY tinhluong.MaNhanVien;"
        result = self.conn.queryResult(strsql)

        row = 0
        self.tblTinhLuong.setRowCount(len(result))
        for user in result:
            
            Thang = "Tháng " + str(user[8]).split('-')[1][-1] if int(str(user[8]).split('-')[1]) < 10 else str(user[8]).split('-')[1]
            
            self.tblTinhLuong.setItem(row, 0, QtWidgets.QTableWidgetItem(str(user[0])))
            self.tblTinhLuong.setItem(row, 1, QtWidgets.QTableWidgetItem(str(user[1])))
            self.tblTinhLuong.setItem(row, 2, QtWidgets.QTableWidgetItem(str(user[2])))
            self.tblTinhLuong.setItem(row, 3, QtWidgets.QTableWidgetItem(str(user[3])))
            self.tblTinhLuong.setItem(row, 4, QtWidgets.QTableWidgetItem(str(user[4])))
            self.tblTinhLuong.setItem(row, 5, QtWidgets.QTableWidgetItem(str(user[5])))
            self.tblTinhLuong.setItem(row, 6, QtWidgets.QTableWidgetItem(str(user[6])))
            self.tblTinhLuong.setItem(row, 7, QtWidgets.QTableWidgetItem(str(user[7])))
            self.tblTinhLuong.setItem(row, 8, QtWidgets.QTableWidgetItem(Thang))
            row = row + 1
    
    
    def exitForm(self):
        sys.exit()
        
    def messageBoxInfo(self, title, text):
        reply = QMessageBox()
        reply.setWindowTitle(title)
        reply.setText(text)
        reply.setStandardButtons(QMessageBox.StandardButton.Ok)

        x = reply.exec()