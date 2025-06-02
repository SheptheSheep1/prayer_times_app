import sys
import socket
from data import Data
from PySide6 import QtCore, QtWidgets, QtGui, QtSvgWidgets
import app as zapp
import random
import string
from datetime import datetime
import multiprocessing
import CalcMethods

#prayerTime = app.PrayerTime()
#print(prayerTime)
class MyWidget(QtWidgets.QWidget):
    def __init__(self, isNetwork: bool, data: Data):
        super().__init__()
        self.data = data
        self.strftime = ""
        self.location = zapp.Location()
        if isNetwork:
            print("net")
            self.data.setLocationMethod(0)
            self.location.setLocationByIP()
        else:
            print("no net")
            self.data.setLocationMethod(2)
            self.location.setLocationManually(33.4838, -112.07404)
        self.data.setLocation(self.location)
        print(f"latitude: {self.data.getLocation().getLatitude()}")
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

        self.settingsButton.clicked.connect(self.__open_settings)

    def __open_settings(self):
        self.dialog = SettingsDialog(self, self.data)
        self.dialog.accepted.connect(self.dialog_finished)
        self.dialog.rejected.connect(self.dialog_rejected)
        self.dialog.open()

    def dialog_finished(self):
        self.data.setCalcMethod(self.dialog.calc_dropdown.currentData())
        print(data.getCalcMethod())
        self.data.setAsrMethod(self.dialog.asrMethodDropdown.currentData())
        print(f"asr: {self.data.getAsrMethod()}")
        match(self.dialog.locationBGroup.checkedId()):
            case -1:
                print("no loc checked")
            case 0:
                print("loc ip check")
            case 1:
                print("loc query check")
            case 2:
                print("loc manual check")
        print("finished")

    def dialog_rejected(self):
        print("rejected")

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, data=Data()):
        super().__init__(parent)
        self.setStyleSheet('''
    QLineEdit:disabled {
        color: gray;
        background-color: #262626;
        border: 1px solid #a0a0a0;
    }
    QLineEdit::enabled {
        color: black;
        background-color: #ffffff;
        border: 1px solid #a0a0a0}
        ''')
        self.setFixedSize(640,480)
        self.setWindowTitle("Settings")
        self.data = data
        
        self.layout = QtWidgets.QVBoxLayout()

        #self.layout.addWidget(QtWidgets.QLabel("Settings"), 5, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        # asr method
        self.asrMethodGroup = QtWidgets.QGroupBox("Asr Calculation Method")
        self.asrMethodDropdown = QtWidgets.QComboBox()
        self.asrMethodDropdown.addItem("Shafi'i/Maliki/Hanbali", userData=1)
        self.asrMethodDropdown.addItem("Hanafi", userData=2)
        self.asrMethodDropdown.setCurrentIndex((self.data.getAsrMethod())-1)
        self.asrMethodBox = QtWidgets.QVBoxLayout()
        self.asrMethodBox.addWidget(self.asrMethodDropdown)
        self.asrMethodGroup.setLayout(self.asrMethodBox)

        
        # calculation method
        self.calcMethodGroup = QtWidgets.QGroupBox("Fajr/Isha Calculation Method")
        self.calcMethodVBox = QtWidgets.QVBoxLayout()
        self.calc_dropdown = QtWidgets.QComboBox()
        for name, method in CalcMethods.methods.items():
            self.calc_dropdown.addItem(str(name), userData=method)
        self.calc_dropdown.setCurrentText(str(self.data.getCalcMethod()))
        self.calcMethodVBox.addWidget(self.calc_dropdown)
        self.calcMethodGroup.setLayout(self.calcMethodVBox)


        # location
        self.locationGroup = QtWidgets.QGroupBox("Location Method")
        self.byIP = QtWidgets.QRadioButton("IPv4 Address (internet required)")
        self.byQuery = QtWidgets.QRadioButton("Query to Nominatim Service (internet required)")
        self.byHand = QtWidgets.QRadioButton("Manual Latitude and Longitude")
        self.locationVBox = QtWidgets.QVBoxLayout()
        self.locationVBox.addStretch(1)
        self.locationGroup.setLayout(self.locationVBox)
        # button group
        self.locationBGroup = QtWidgets.QButtonGroup()
        self.locationBGroup.addButton(self.byIP, id=0)
        self.locationBGroup.addButton(self.byQuery, id=1)
        self.locationBGroup.addButton(self.byHand, id=2)
        self.locationBGroup.setExclusive(True)
        self.locationBGroup.button(self.data.getLocationMethod()).setChecked(True)
        self.locationBGroup.buttonClicked.connect(self.update_location_options)
        # line edits
        # latitude
        self.manualTooltip = "Enable Manual Latitude and Longitude Option to Edit"
        self.latitude = QtWidgets.QLineEdit()
        self.latitude.setPlaceholderText("Latitude")
        self.latitude.setEnabled(False)
        self.latitude.setToolTip(self.manualTooltip)
        # longitude
        self.longitude = QtWidgets.QLineEdit()
        self.longitude.setPlaceholderText("Longitude")
        self.longitude.setEnabled(False)
        self.longitude.setToolTip(self.manualTooltip)
        # query
        self.query = QtWidgets.QLineEdit()
        self.query.setPlaceholderText("Enter Region/City Name Here")
        self.query.setEnabled(False)
        self.query.setToolTip("Enable Query Option to Edit")
        # pre fill lines
        match self.data.getLocationMethod():
            case 1:
                self.query.setText(str(self.data.getQuery()))
                self.query.setEnabled(True)
            case 2:
                self.latitude.setText(str(self.data.getLocation().getLatitude()))
                self.latitude.setEnabled(True)
                self.longitude.setText(str(self.data.getLocation().getLongitude()))
                self.longitude.setEnabled(True)
        # VBox
        self.locationVBox.addWidget(self.byIP)
        self.locationVBox.addWidget(self.byQuery)
        self.locationVBox.addWidget(self.query)
        self.locationVBox.addWidget(self.byHand)
        self.locationVBox.addWidget(self.latitude)
        self.locationVBox.addWidget(self.longitude)


        # cancel/save button
        #self.save_button = QtWidgets.QPushButton("Save")
        #self.save_button.clicked.connect(self.accept)
        #self.close_button = QtWidgets.QPushButton("Cancel")
        #self.close_button.clicked.connect(self.reject)
        #self.closeLayout = QtWidgets.QHBoxLayout()
        #self.closeLayout.addWidget(self.close_button, 50)
        #self.closeLayout.addWidget(self.save_button, 50)
        
        self.closeButtons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel)
        self.closeButtons.accepted.connect(self.accept)
        self.closeButtons.rejected.connect(self.reject)
        #self.closeButtons.setCenterButtons(True)


        #self.layout.addWidget(QtWidgets.QSpacerItem(20,40))
        self.layout.addWidget(self.asrMethodGroup)
        self.layout.addWidget(self.locationGroup)
        self.layout.addWidget(self.calcMethodGroup)
        #self.layout.addLayout(self.closeLayout)
        self.layout.addWidget(self.closeButtons)

        self.setLayout(self.layout)

    def update_location_options(self):
        is_custom = self.byHand.isChecked()
        is_query = self.byQuery.isChecked()

        self.latitude.setEnabled(is_custom)
        self.longitude.setEnabled(is_custom)
        self.query.setEnabled(is_query)



def is_connected(hostname, isConnected: list):
    try:
        # see if we can do a dns lookup, return True if it can happen
        host = socket.gethostbyname(hostname)
        s = socket.create_connection((host, 80), 2)
        s.close()
        isConnected[0] = True
        return
    except Exception:
        pass # ignore errors and return False
    isConnected[0] = False
    return

if __name__ == "__main__":
    # holds data for app during runtime (app does not store information otherwise)
    data = Data()

    hostname = "one.one.one.one"
    isConnected = [False]
    checkInternet = multiprocessing.Process(target=is_connected, args=(hostname, isConnected))
    checkInternet.start()
    print("[+] checking internet connectivity...")
    checkInternet.join(3)
    if checkInternet.is_alive():
        print("[-] dns lookup timeout, terminating process...")
        checkInternet.kill()
        checkInternet.join()
    if isConnected[0]:
        print("[+] internet connectivity check succeeded...")
    else:
        print("[-] internet connectivity check failed...")
    #print("[+] internet connectivity check finished")


    app = QtWidgets.QApplication([])

    widget = MyWidget(isConnected[0], data)
    widget.setFixedSize(800, 600)
    widget.show()

    sys.exit(app.exec())
