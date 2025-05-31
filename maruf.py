import sys
from PySide6 import QtCore, QtWidgets, QtGui, QtSvgWidgets
from salah_app import app
import random
import string
from datetime import datetime

#prayerTime = app.PrayerTime()
#print(prayerTime)
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ma'ruf")
        self.__initUI()
        self.init_style()

    def init_style(self):
        self.setStyleSheet( """QPushButton {background-color:blue; border:none;}
            QPushButton::pressed {background-color:black; color:white; border:2px solid yellow;}
            QPushButton#another_button {background-color:green; color:black; border-radius: 13px;}
            QLabel {font-family: Helvetica;}
            QLabel#nonmain {background-color:#262626}
            QLabel#mainTime {background-color:#262626;
                           font-size: 24px;}
            QLabel#title{
                            font-family: Helvetica;
                            font-size: 48px;
                            padding-left: 15px;
                        }
            QLabel#region{
                            font-family: Helvetica;
                            font-size: 22px;
                            color: #848080;
                            padding-right: 15px;
                            margin-bottom: -10px;
                        }
            QLabel#leftTime{
                            font-family: Helvetica;
                           }
            QLabel#mainPrayerTime{
                           font-size: 24px;}
            QLabel#region2{
                           font-family: Helvetica;
                           font-size: 14px;
                           color: #848080;
                           padding-right: 15px;
                           margin-bottom: -10px;
                        }
        """)


    def __initUI(self):
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        # title
        self.rightTitleLayout = QtWidgets.QVBoxLayout()
        self.rightTitleLayout.addWidget(QtWidgets.QLabel("Scottsdale, Arizona", alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom, objectName="region"))
        self.date = QtWidgets.QLabel("May 30, 2025", alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self.date.setObjectName("region2")
        self.rightTitleLayout.addWidget(self.date)
        self.rightTitleLayout.setSpacing(0)
        self.rightTitleLayout.setContentsMargins(0,0,0,0)

        self.titleLayout = QtWidgets.QHBoxLayout()
        self.titleLayout.addWidget(QtWidgets.QLabel("Prayer Times", alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, objectName="title"))

        self.titleLayout.addLayout(self.rightTitleLayout)

        self.subLayout = QtWidgets.QHBoxLayout()

        self.midLayout = QtWidgets.QVBoxLayout()
        self.fajr = QtWidgets.QHBoxLayout()
        self.fajr.addWidget(QtSvgWidgets.QSvgWidget("./resources/fajr.svg"), 75, alignment=QtCore.Qt.AlignLeft)
        self.fajrTime = QtWidgets.QLabel(datetime.min.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.fajrTime.setObjectName("mainPrayerTime")
        self.fajr.addWidget(self.fajrTime, 25)
        self.midLayout.addLayout(self.fajr)
        for _ in range(5):
            label = QtWidgets.QLabel(datetime.min.strftime("%I:%M:%S %p"), alignment=QtCore.Qt.AlignCenter)
            label.setObjectName("mainTime")
            self.midLayout.addWidget(label)
        self.fajr.setContentsMargins(0,0,0,0)
        self.fajr.setSpacing(0)
        self.midLayout.setContentsMargins(0,0,0,0)
        self.midLayout.setSpacing(0)

        self.leftLayout = QtWidgets.QVBoxLayout()
        for _ in range(6):
            label = QtWidgets.QLabel(datetime.min.strftime("%I:%M:%S %p"), alignment=QtCore.Qt.AlignCenter)
            label.setObjectName("leftTime")
            self.leftLayout.addWidget(label)

        self.rightLayout = QtWidgets.QVBoxLayout()
        for _ in range(6):
            label = QtWidgets.QLabel(datetime.min.strftime("%I:%M:%S %p"), alignment=QtCore.Qt.AlignCenter)
            label.setObjectName("rightTime")
            self.rightLayout.addWidget(label)

        self.subLayout.addLayout(self.leftLayout, 25)
        self.subLayout.addLayout(self.midLayout, 50)
        self.subLayout.addLayout(self.rightLayout, 25)
        self.subLayout.setContentsMargins(0,0,0,0)
        self.subLayout.setSpacing(0)

        self.mainLayout.addLayout(self.titleLayout, 10)
        self.mainLayout.addLayout(self.subLayout, 80)
        # TODO: Add settings button and maybe other
        self.mainLayout.addWidget(QtWidgets.QLabel("SETTINGS PLCHLDER"), 10)
        self.mainLayout.setContentsMargins(0,0,0,0)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.setFixedSize(800, 600)
    widget.show()

    sys.exit(app.exec())
