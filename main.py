from PyQt6 import QtCore
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import * 
from PyQt6.QtCore import Qt
import sys
from nhanvien import nhanvien

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
nhanvien = nhanvien()

widget.addWidget(nhanvien)
widget.setCurrentIndex(0)
widget.setFixedWidth(930)
widget.setFixedHeight(661)
widget.show()
app.exec()
