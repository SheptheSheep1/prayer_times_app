import sys
import socket
from PySide6 import QtCore, QtWidgets, QtGui, QtSvgWidgets
import app
import random
import string
from datetime import datetime

#prayerTime = app.PrayerTime()
#print(prayerTime)
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.strftime = ""
        self.setWindowTitle("Ma'ruf")
        self.__initUI()
        self.init_style()

    def init_style(self):
        self.setStyleSheet( """
            QPushButton#another_button {background-color:green; color:black; border-radius: 13px;}
            QLabel {}
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
                           font-size: 24px;
                           background-color: #262626;
                           padding-right: 15px;}
            QLabel#region2{
                           font-family: Helvetica;
                           font-size: 14px;
                           color: #848080;
                           padding-right: 15px;
                           margin-bottom: -10px;
                        }
            QPushButton{
                            color: #cccccc;
                            font-size: 16px;
                            font-family: Helvetica;
                            font-weight: normal;
                            margin-right: 15px;
                            margin-bottom: 15px;
                            padding: 5px;

            }
            QLabel#mainDate{
                            color: #FFFFFF;
                            font-size: 20px;
                            font-family: Helvetica;
                            font-weight: normal;
                            padding-bottom: 5px;
            }
        """)


    def __initUI(self):
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        # title
        self.rightTitleLayout = QtWidgets.QVBoxLayout()
        self.rightTitleLayout.addWidget(QtWidgets.QLabel("Scottsdale, Arizona", alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom, objectName="region"))
        self.date = QtWidgets.QLabel("May 30, 2025", alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self.date.setObjectName("region2")
        print(self.date.font())
        self.rightTitleLayout.addWidget(self.date)
        self.rightTitleLayout.setSpacing(0)
        self.rightTitleLayout.setContentsMargins(0,0,0,0)

        self.titleLayout = QtWidgets.QHBoxLayout()
        self.titleLayout.addWidget(QtWidgets.QLabel("Prayer Times", alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, objectName="title"))
        self.titleLayout.setContentsMargins(0,0,0,0)
        self.titleLayout.setSpacing(0)

        self.titleLayout.addLayout(self.rightTitleLayout)

        #subtitle
        self.subtitleLayout = QtWidgets.QHBoxLayout()
        self.leftDate = QtWidgets.QLabel("September 30, 2025", alignment=QtCore.Qt.AlignCenter)
        self.centerDate = QtWidgets.QLabel("October 1, 2025", alignment=QtCore.Qt.AlignCenter)
        self.rightDate = QtWidgets.QLabel("October 2, 2025", alignment=QtCore.Qt.AlignCenter)
        self.centerDate.setObjectName("mainDate")
        self.subtitleLayout.addWidget(self.leftDate, 25)
        self.subtitleLayout.addWidget(self.centerDate, 50)
        self.subtitleLayout.addWidget(self.rightDate, 25)
        self.subtitleLayout.setSpacing(0)
        self.subtitleLayout.setContentsMargins(0,0,0,0)

        self.subLayout = QtWidgets.QHBoxLayout()

        self.midLayout = QtWidgets.QVBoxLayout()
        #fajr time
        self.fajr = QtWidgets.QHBoxLayout()
        self.fajrSvg = QtSvgWidgets.QSvgWidget("./resources/real/fajr.svg")
        self.fajrSvg.setFixedSize(300, 80) #forces fixed for other mainTimes as well
        self.fajr.addWidget(self.fajrSvg, alignment=QtCore.Qt.AlignLeft)
        self.fajrTime = QtWidgets.QLabel(datetime.min.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.fajrTime.setObjectName("mainPrayerTime")
        self.fajr.addWidget(self.fajrTime)
        #sunrise time
        self.sunrise = QtWidgets.QHBoxLayout()
        self.sunrise.addWidget(QtSvgWidgets.QSvgWidget("./resources/real/sunrise.svg"), 75, alignment=QtCore.Qt.AlignLeft)
        self.sunriseTime = QtWidgets.QLabel(datetime.min.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.sunriseTime.setObjectName("mainPrayerTime")
        self.sunrise.addWidget(self.sunriseTime, 25)
        #dhuhr time
        self.dhuhr = QtWidgets.QHBoxLayout()
        self.dhuhr.addWidget(QtSvgWidgets.QSvgWidget("./resources/real/dhuhr.svg"), 75, alignment=QtCore.Qt.AlignLeft)
        self.dhuhrTime = QtWidgets.QLabel(datetime.min.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.dhuhrTime.setObjectName("mainPrayerTime")
        self.dhuhr.addWidget(self.dhuhrTime, 25)
        #asr time
        self.asr = QtWidgets.QHBoxLayout()
        self.asr.addWidget(QtSvgWidgets.QSvgWidget("./resources/real/asr.svg"), 75, alignment=QtCore.Qt.AlignLeft)
        self.asrTime = QtWidgets.QLabel(datetime.min.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.asrTime.setObjectName("mainPrayerTime")
        self.asr.addWidget(self.asrTime, 25)
        #maghrib time
        self.maghrib = QtWidgets.QHBoxLayout()
        self.maghrib.addWidget(QtSvgWidgets.QSvgWidget("./resources/real/maghrib.svg"), 75, alignment=QtCore.Qt.AlignLeft)
        self.maghribTime = QtWidgets.QLabel(datetime.min.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.maghribTime.setObjectName("mainPrayerTime")
        self.maghrib.addWidget(self.maghribTime, 25)
        #isha time
        self.isha = QtWidgets.QHBoxLayout()
        self.isha.addWidget(QtSvgWidgets.QSvgWidget("./resources/real/isha.svg"), 75, alignment=QtCore.Qt.AlignLeft)
        self.ishaTime = QtWidgets.QLabel(datetime.min.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.ishaTime.setObjectName("mainPrayerTime")
        self.isha.addWidget(self.ishaTime, 25)
        
        # add prayer times
        self.midLayout.addLayout(self.fajr)
        self.midLayout.addLayout(self.sunrise)
        self.midLayout.addLayout(self.dhuhr)
        self.midLayout.addLayout(self.asr)
        self.midLayout.addLayout(self.maghrib)
        self.midLayout.addLayout(self.isha)

        #for _ in range(5):
        #    label = QtWidgets.QLabel(datetime.min.strftime("%I:%M:%S %p"), alignment=QtCore.Qt.AlignCenter)
        #    label.setObjectName("mainTime")
        #    self.midLayout.addWidget(label)
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

        # bottom
        self.bottomLayout = QtWidgets.QHBoxLayout()
        self.settingsButton = QtWidgets.QPushButton(QtGui.QIcon("./resources/gear.png"), "Settings")
        self.settingsButton.setIconSize(QtCore.QSize(24,24))
        self.bottomLayout.addWidget(self.settingsButton, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)


        self.mainLayout.addLayout(self.titleLayout, 10)
        self.mainLayout.addLayout(self.subtitleLayout, 5)
        self.mainLayout.addLayout(self.subLayout, 80)
        self.mainLayout.addLayout(self.bottomLayout, 5)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setSpacing(0)

def is_connected(hostname):
    try:
        # see if we can do a dns lookup, return True if it can happen
        host = socket.gethostbyname(hostname)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except Exception:
        pass # ignore errors and return False
    return False

if __name__ == "__main__":
    print(f"internet_connection: {is_connected('one.one.one.one')}")
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.setFixedSize(800, 600)
    widget.show()

    sys.exit(app.exec())
