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
        print(f"location: {self.data.getLocation()}")
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
                            font-size: 36px;
                            padding-left: 15px;
                        }
            QLabel#region{
                            font-family: Helvetica;
                            font-size: 22px;
                            color: #848080;
                            padding-right: 15px;
                            padding-top: 15px;
                            padding-bottom: 5px;
                        }
            QLabel#leftTime{
                            font-family: Helvetica;
                           }
            QLabel#mainPrayerTime{
                           font-size: 20px;
                           background-color: #262626;
                           padding-right: 15px;}
            QLabel#region2{
                           font-family: Helvetica;
                           font-size: 14px;
                           color: #848080;
                           padding-right: 15px;
                        }
            QPushButton {
                            color: #cccccc;
                            font-size: 20px;
                            font-family: Helvetica;
                            font-weight: normal;
                            margin-right: 6px;
                            margin-bottom: 6px;
                            padding: 5px;

            }
            QLabel#mainDate{
                            color: #FFFFFF;
                            font-size: 16px;
                            font-family: Helvetica;
                            font-weight: normal;
                            padding-bottom: 4px;
            }
            QLabel#otherDate{
                            font-size: 14px;
            }
        """)


    def __initUI(self):
        self.dateFtime = "%B %d, %Y"
        self.timeFtime = "%I:%M %p"
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        # title
        self.rightTitleLayout = QtWidgets.QVBoxLayout()
        self.regionLoc = QtWidgets.QLabel(f"{self.data.getLocation().getDescription()}", alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignTop, objectName="region")
        self.rightTitleLayout.addWidget(self.regionLoc)
        #self.rightTitleLayout.addWidget(QtWidgets.QLabel("Scottsdale, Arizona", alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignTop, objectName="region"))
        #self.date = QtWidgets.QLabel("May 30, 2025", alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        #self.date.setObjectName("region2")
        #print(self.date.font())
        #self.rightTitleLayout.addWidget(self.date)
        self.rightTitleLayout.setSpacing(0)
        self.rightTitleLayout.setContentsMargins(0,0,0,0)

        self.titleLayout = QtWidgets.QHBoxLayout()
        self.titleLayout.addWidget(QtWidgets.QLabel("Prayer Times", alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, objectName="title"))
        self.titleLayout.setContentsMargins(0,0,0,0)
        self.titleLayout.setSpacing(0)

        self.titleLayout.addLayout(self.rightTitleLayout)

        #subtitle
        self.subtitleLayout = QtWidgets.QHBoxLayout()
        #self.leftDate = QtWidgets.QLabel("September 30, 2025", alignment=QtCore.Qt.AlignCenter)
        self.leftDate = QtWidgets.QLabel(self.data.getYesterdayDate().strftime(self.dateFtime), alignment=QtCore.Qt.AlignCenter)
        self.centerDate = QtWidgets.QLabel(self.data.getTodayDate().strftime(self.dateFtime), alignment=QtCore.Qt.AlignCenter)
        self.rightDate = QtWidgets.QLabel(self.data.getTomorrowDate().strftime(self.dateFtime), alignment=QtCore.Qt.AlignCenter)
        self.centerDate.setObjectName("mainDate")
        self.leftDate.setObjectName("otherDate")
        self.rightDate.setObjectName("otherDate")
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
        #self.fajrTime = QtWidgets.QLabel(datetime.min.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.fajrTime = QtWidgets.QLabel(self.data.prayerToday.fajr_time.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        #print(self.data.prayerToday)
        self.fajrTime.setObjectName("mainPrayerTime")
        self.fajr.addWidget(self.fajrTime)
        #sunrise time
        self.sunrise = QtWidgets.QHBoxLayout()
        self.sunriseSvg = QtSvgWidgets.QSvgWidget("./resources/real/sunrise.svg")
        self.sunriseSvg.setFixedSize(300, 80)
        self.sunrise.addWidget(self.sunriseSvg, 75, alignment=QtCore.Qt.AlignLeft)
        #self.sunriseTime = QtWidgets.QLabel(datetime.min.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.sunriseTime = QtWidgets.QLabel(self.data.prayerToday.sunrise_time.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.sunriseTime.setObjectName("mainPrayerTime")
        self.sunrise.addWidget(self.sunriseTime, 25)
        #self.sunrise.addWidget(self.sunriseTime)
        #dhuhr time
        self.dhuhr = QtWidgets.QHBoxLayout()
        self.dhuhrSvg = QtSvgWidgets.QSvgWidget("./resources/real/dhuhr.svg")
        self.dhuhrSvg.setFixedSize(300, 80)
        self.dhuhr.addWidget(self.dhuhrSvg, 75, alignment=QtCore.Qt.AlignLeft)
        #self.dhuhrTime = QtWidgets.QLabel(datetime.min.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.dhuhrTime = QtWidgets.QLabel(self.data.prayerToday.dhuhr_time.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.dhuhrTime.setObjectName("mainPrayerTime")
        self.dhuhr.addWidget(self.dhuhrTime, 25)
        #self.dhuhr.addWidget(self.dhuhrTime)
        #asr time
        self.asr = QtWidgets.QHBoxLayout()
        self.asrSvg = QtSvgWidgets.QSvgWidget("./resources/real/asr.svg")
        self.asrSvg.setFixedSize(300, 80)
        self.asr.addWidget(self.asrSvg, 75, alignment=QtCore.Qt.AlignLeft)
        #self.asrTime = QtWidgets.QLabel(datetime.min.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.asrTime = QtWidgets.QLabel(self.data.prayerToday.asr_time.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.asrTime.setObjectName("mainPrayerTime")
        self.asr.addWidget(self.asrTime, 25)
        #maghrib time
        self.maghrib = QtWidgets.QHBoxLayout()
        self.maghribSvg = QtSvgWidgets.QSvgWidget("./resources/real/maghrib.svg")
        self.maghribSvg.setFixedSize(300, 80)
        self.maghrib.addWidget(self.maghribSvg, 75, alignment=QtCore.Qt.AlignLeft)
        #self.maghribTime = QtWidgets.QLabel(datetime.min.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.maghribTime = QtWidgets.QLabel(self.data.prayerToday.maghrib_time.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.maghribTime.setObjectName("mainPrayerTime")
        #self.maghrib.addWidget(self.maghribTime, 25)
        self.maghrib.addWidget(self.maghribTime)
        #isha time
        self.isha = QtWidgets.QHBoxLayout()
        self.ishaSvg = QtSvgWidgets.QSvgWidget("./resources/real/isha.svg")
        self.ishaSvg.setFixedSize(300, 80)
        self.isha.addWidget(QtSvgWidgets.QSvgWidget("./resources/real/isha.svg"), 75, alignment=QtCore.Qt.AlignLeft)
        #self.ishaTime = QtWidgets.QLabel(datetime.min.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.ishaTime = QtWidgets.QLabel(self.data.prayerToday.isha_time.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.ishaTime.setObjectName("mainPrayerTime")
        self.isha.addWidget(self.ishaTime, 25)
        #self.isha.addWidget(self.ishaTime)

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
        self.subMidWidget = QtWidgets.QWidget()
        self.subMidWidget.setLayout(self.midLayout)
        self.subMidWidget.setFixedWidth(400)

        self.leftLayout = QtWidgets.QVBoxLayout()
        for values in self.data.getPrayerYesterday().getPrayertimes().values():
            #label = QtWidgets.QLabel(datetime.min.strftime("%I:%M:%S %p"), alignment=QtCore.Qt.AlignCenter)
            label = QtWidgets.QLabel(values.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignCenter)
            label.setObjectName("leftTime")
            self.leftLayout.addWidget(label)

        self.rightLayout = QtWidgets.QVBoxLayout()
        for values in self.data.getPrayerTomorrow().getPrayertimes().values():
            label = QtWidgets.QLabel(values.strftime("%I:%M %p"), alignment=QtCore.Qt.AlignCenter)
            label.setObjectName("leftTime")
            self.rightLayout.addWidget(label)

        self.subLayout.addLayout(self.leftLayout, 25)
        #self.subLayout.addLayout(self.midLayout, 50)
        self.subLayout.addWidget(self.subMidWidget)
        self.subLayout.addLayout(self.rightLayout, 25)
        self.subLayout.setContentsMargins(0,0,0,0)
        self.subLayout.setSpacing(0)
        self.midWidget = QtWidgets.QWidget()
        self.midWidget.setLayout(self.subLayout)
        self.midWidget.setFixedHeight(int(.8*600))
        #self.midWidget.setFixedWidth(400)

        # bottom
        self.bottomLayout = QtWidgets.QHBoxLayout()
        self.settingsButton = QtWidgets.QPushButton(QtGui.QIcon("./resources/gear.png"), "Settings")
        self.settingsButton.setIconSize(QtCore.QSize(24,24))
        self.settingsButton.setObjectName("settingsButton")
        self.bottomLayout.addWidget(self.settingsButton, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.bottomLayout.setSpacing(0)
        self.bottomLayout.setContentsMargins(0,0,0,0)


        self.mainLayout.addLayout(self.titleLayout, 8)
        self.mainLayout.addLayout(self.subtitleLayout, 5)
        #self.mainLayout.addLayout(self.subLayout, 80)
        self.mainLayout.addWidget(self.midWidget)
        self.mainLayout.addLayout(self.bottomLayout, 7)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setSpacing(0)

        self.settingsButton.clicked.connect(self.__open_settings)
        #self.settingsButton.clicked.connect(lambda :LoadingDialog(self, "Making Web Request...").open())

    def __open_settings(self):
        self.dialog = SettingsDialog(self, self.data)
        self.dialog.accepted.connect(self.dialog_finished)
        self.dialog.rejected.connect(self.dialog_rejected)
        self.dialog.open()

    def updateTimes(self):
        # update location
        self.regionLoc.setText(self.data.getLocation().getDescription())
        print("set",self.data.getLocation().getDescription())
        # update dates
        self.leftDate.setText(self.data.getYesterdayDate().strftime(self.dateFtime))
        self.centerDate.setText(self.data.getTodayDate().strftime(self.dateFtime))
        self.rightDate.setText(self.data.getTomorrowDate().strftime(self.dateFtime))
        # update left layout (yesterday)
        yesterkeys = list(self.data.getPrayerYesterday().getPrayertimes().keys())
        for i in range(self.leftLayout.count()):
            item = self.leftLayout.itemAt(i)
            widget = item.widget()
            if widget and isinstance(widget, QtWidgets.QLabel):
                key = yesterkeys[i]
                widget.setText(self.data.getPrayerYesterday().getPrayertimes()[key].strftime(self.timeFtime))

        # update right layout (tomorrow)
        tomorrow_keys = list(self.data.getPrayerTomorrow().getPrayertimes().keys())
        for i in range(self.rightLayout.count()):
            item = self.rightLayout.itemAt(i)
            widget = item.widget()
            if widget and isinstance(widget, QtWidgets.QLabel):
                key = tomorrow_keys[i]
                widget.setText(self.data.getPrayerTomorrow().getPrayertimes()[key].strftime(self.timeFtime))

        # update mid layout (today)
        self.fajrTime.setText(self.data.getPrayerToday().getPrayertimes()["fajr"].strftime(self.timeFtime))
        self.sunriseTime.setText(self.data.getPrayerToday().getPrayertimes()["sunrise"].strftime(self.timeFtime))
        self.dhuhrTime.setText(self.data.getPrayerToday().getPrayertimes()["dhuhr"].strftime(self.timeFtime))
        self.asrTime.setText(self.data.getPrayerToday().getPrayertimes()["asr"].strftime(self.timeFtime))
        self.maghribTime.setText(self.data.getPrayerToday().getPrayertimes()["maghrib"].strftime(self.timeFtime))
        self.ishaTime.setText(self.data.getPrayerToday().getPrayertimes()["isha"].strftime(self.timeFtime))


    def recalculateData(self):
        self.data.genPrayerTimes()


    def dialog_finished(self):
        self.data.setCalcMethod(self.dialog.calc_dropdown.currentData())
        print(data.getCalcMethod())
        self.data.setAsrMethod(self.dialog.asrMethodDropdown.currentData())
        print(f"asr: {self.data.getAsrMethod()}")
        self.threadz = QtCore.QThread()
        self.worker = None
        match(self.dialog.locationBGroup.checkedId()):
            case -1:
                print("no loc checked")
            case 0:
                print("loc ip check")
                self.worker = WebRequestWorker("byIP")
                # add loading screen for waiting for request
                #self.data.getLocation().setLocationByIP()
            case 1:
                print("loc query check")
                self.worker = WebRequestWorker("byQuery", str(self.dialog.query.text()))
                #self.data.getLocation().setLocationByQuery(self.dialog.query.text())
            case 2:
                self.data.getLocation().setLocationManually(float(self.dialog.latitude.text()), float(self.dialog.longitude.text()))
                print("loc manual check")
        if self.worker is not None:
            self.loading_dialog = LoadingDialog(self)
            self.loading_dialog.show()

            self.worker.moveToThread(self.threadz)
            self.threadz.started.connect(self.worker.run)
            self.worker.finished.connect(self.handle_result)
            self.worker.finished.connect(self.cleanup_thread)
            #self.threadz.finished.connect(self.threadz.deleteLater)

            self.threadz.start()
        print(f"Coords: {self.data.getLocation(), self.data.getLocation().getDescription()}")
        print("finished")
        #self.data.setPrayerYesterday(zapp.PrayerTime(datetime.min.month, datetime.min.day, datetime.min.year))
        #self.data.setPrayerTomorrow(zapp.PrayerTime(datetime.min.month, datetime.min.day, datetime.min.year))
        #self.data.setPrayerToday(zapp.PrayerTime(datetime.min.month, datetime.min.day, datetime.min.year))
        self.data.setDate(self.dialog.get_selected_datetime())
        print(f"date: {self.data.getTodayDate()}")
        self.recalculateData()
        self.updateTimes()
    
    def cleanup_thread(self):
        self.threadz.quit()
        self.threadz.wait()
        self.worker.deleteLater()
        self.threadz.deleteLater()

    def handle_result(self, result):
        self.loading_dialog.hide()
        print(f"got: {result}")
        self.data.setLocation(result)
        self.regionLoc.setText(self.data.getLocation().getDescription())
        self.threadz.quit()
        self.threadz.wait()
        self.worker.deleteLater()
        self.threadz.deleteLater()

    def dialog_rejected(self):
        print("rejected")


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, data=Data(datetime.now())):
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
        #self.setFixedSize(640,480)
        self.setFixedWidth(480)
        self.setWindowTitle("Settings")
        self.data = data
        
        self.layout = QtWidgets.QVBoxLayout()

        #self.layout.addWidget(QtWidgets.QLabel("Settings"), 5, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        # date/time
        self.dateTimeGroup = QtWidgets.QGroupBox("Date")
        self.month_box = QtWidgets.QComboBox()
        self.day_box = QtWidgets.QComboBox()
        self.year_box = QtWidgets.QComboBox()

        self.setup_ui()

        self.dateTimeBox = QtWidgets.QHBoxLayout()
        self.dateTimeBox.addWidget(QtWidgets.QLabel("Month"))
        self.dateTimeBox.addWidget(self.month_box)
        self.dateTimeBox.addWidget(QtWidgets.QLabel("Day"))
        self.dateTimeBox.addWidget(self.day_box)
        self.dateTimeBox.addWidget(QtWidgets.QLabel("Year"))
        self.dateTimeBox.addWidget(self.year_box)
        self.dateTimeGroup.setLayout(self.dateTimeBox)

        # set current
        self.month_box.setCurrentText(str(self.data.todayDate.strftime("%B")))
        self.day_box.setCurrentText(str(self.data.todayDate.day))
        self.year_box.setCurrentText(str(self.data.todayDate.year))

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
        self.layout.addWidget(self.dateTimeGroup)
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
        
    def setup_ui(self):
        # def not copy/p
        # Populate months
        for month in range(1, 13):
            month_name = QtCore.QDate(2000, month, 1).toString("MMMM")
            self.month_box.addItem(month_name, month)

        # Populate years (example: from 1950 to current year + 10)
        current_year = QtCore.QDate.currentDate().year()
        for year in range(current_year - 100, current_year + 11):
            self.year_box.addItem(str(year), year)

        # Connect signals to update days dynamically
        self.month_box.currentIndexChanged.connect(self.update_days)
        self.year_box.currentIndexChanged.connect(self.update_days)

        # Initial update
        self.update_days()

    def update_days(self):
        month = self.month_box.currentData()
        year = self.year_box.currentData()
        if month is None or year is None:
            return

        days_in_month = QtCore.QDate(year, month, 1).daysInMonth()
        current_day = self.day_box.currentText()

        self.day_box.blockSignals(True)
        self.day_box.clear()
        for day in range(1, days_in_month + 1):
            self.day_box.addItem(str(day))
        self.day_box.blockSignals(False)

        # Try to keep previous selection
        if current_day and current_day.isdigit():
            idx = self.day_box.findText(current_day)
            if idx != -1:
                self.day_box.setCurrentIndex(idx)

    def get_selected_date(self):
        # Returns a QDate
        year = int(self.year_box.currentText())
        month = self.month_box.currentData()
        day = int(self.day_box.currentText())
        return QtCore.QDate(year, month, day)

    def get_selected_datetime(self):
        year = int(self.year_box.currentText())
        month = self.month_box.currentData()
        day = int(self.day_box.currentText())
        return datetime(year, month, day)





class LoadingDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, display="Loading..."):
        super().__init__(parent)
        self.setFixedSize(250,100)
        self.setModal(True)
        self.setWindowTitle("Loading")
        self.spinner_label = QtWidgets.QLabel(self)
        self.movie = QtGui.QMovie("./resources/rolling.gif")
        self.spinner_label.setMovie(self.movie)
        self.movie.setScaledSize(QtCore.QSize(32,32))
        self.movie.start()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel(display), alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.spinner_label, alignment=QtCore.Qt.AlignCenter)
        self.setLayout(layout)


#class byIpWorker(QtCore.QThread):
#    finished = QtCore.Signal(str)
#    def run(self):
#        location = zapp.Location()
#        location.setLocationByIP()
#        self.finished.emit(location)
#class byQueryWorker(QtCore.QThread):
#    finished = QtCore.Signal(str)
#    def run(self):
#        location = zapp.Location()
#        location.setLocationByQuery()
class WebRequestWorker(QtCore.QObject):
    finished = QtCore.Signal(object)

    def __init__(self, mode: str, query=""):
        super().__init__()
        self.mode = mode
        self.query = query
        self.location = zapp.Location()

    def run(self):
        if self.mode == "byIP":
            self.location.setLocationByIP()
        elif self.mode == "byQuery":
            self.location.setLocationByQuery(self.query)
        else:
            self.location = zapp.Location()
        self.finished.emit(self.location)



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
    data = Data(datetime.now())

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
