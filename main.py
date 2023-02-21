from PyQt6 import QtCore
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import * 
from PyQt6.QtCore import Qt
import sys
from nhanvien import nhanvien
from tinhluong import tinhluong

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

nhanvien = nhanvien()
tinhluong = tinhluong()


widget.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
widget.addWidget(nhanvien)
widget.addWidget(tinhluong)


widget.setCurrentIndex(1)
widget.setFixedWidth(930)
widget.setFixedHeight(661)
widget.show()
app.exec()
