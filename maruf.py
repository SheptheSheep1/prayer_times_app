import sys
import pray_data
from PySide6.QtCore import QThread, Qt, QTimer, QDate, QSize, QObject, Signal, Slot
from PySide6.QtGui import QIcon, QMovie
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDialog, QLineEdit, QComboBox, QGroupBox, QCheckBox, QDialogButtonBox, QRadioButton, QDialogButtonBox, QApplication, QButtonGroup
#from PySide6 import    QtSvgWidgets
import app as zapp
#import random
#import string
from datetime import datetime, time, UTC
from multiprocessing import freeze_support, Process, Value
import CalcMethods
import os
import qdarktheme
#import traceback
#import time as atime
#import timeit
from zoneinfo import ZoneInfo, available_timezones
#from timezonefinder import TimezoneFinder

#def resource_path(relative_path):
#    if hasattr(sys, '_MEIPASS'):
#        base_path = sys._MEIPASS  # For PyInstaller-like environments
#    elif '__compiled__' in globals():
#        print("compiled")
#        base_path = os.path.dirname(sys.executable)
#    else:
#        #return os.path.join(os.path.abspath("."), relative_path)
#        #return relative_path
#        base_path = os.path.abspath(".")
#    return os.path.join(base_path, relative_path)
def resource_path(relative_path):
    # Detect compiled (Nuitka) mode
    if getattr(sys, 'frozen', False) or '__compiled__' in globals():
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.normpath(os.path.join(base_path, relative_path))


#prayerTime = app.PrayerTime()
#print(prayerTime)
class MyWidget(QWidget):
    def __init__(self, isNetwork: bool, data: pray_data.Data, conf_file_existence: bool):
        super().__init__()
        self.data = data
        self.strftime = ""
        print("dark mode:",self.data.getDarkMode())
        if isNetwork and not conf_file_existence:
            print("net")
            self.data.setLocationMethod(0)
            self.data.getLocation().setLocationByIP()
            #self.location.setLocationByIP()
            #self.data.setLocation(self.location)
        elif conf_file_existence:
            self.data.setLocationMethod(2)
        else:
            print("no net")
            self.data.setLocationMethod(2)
            self.data.getLocation().setLocationManually(33.5, -112.1)
            #self.location.setLocationManually(33.5, -112.1)
            #self.data.setLocation(self.location)
        self.data.genPrayerTimes()
        print(f"location: {self.data.getLocation()}")
        print(f"timezone info: (utc_offset: {self.data.getUTCOffset()} desc: {self.data.getTzDesc()})")
        self.setWindowTitle("Ma'ruf")
        self.__initUI()
        self.init_style()
        #self.set_style_color()

    def is_dark_theme(self):
        return self.data.getDarkMode()

    def init_style(self):

        if self.data.getDarkMode() is True:
            qdarktheme.setup_theme("dark")
            self.setStyleSheet("""
                QPushButton#another_button {background-color:green; color:black; border-radius: 13px;}
                QLabel#mainTime {
                               font-size: 24px;}
                QLabel#title{
                                font-family: Helvetica;
                                font-size: 36px;
                                padding-left: 15px;
                            }
                QLabel#region{
                                font-family: Helvetica;
                                font-size: 22px;
                                padding-right: 15px;
                                padding-top: 15px;
                                padding-bottom: 5px;
                            }
                QLabel#leftTime{
                                font-family: Helvetica;
                               }
                QLabel#mainPrayerTime{
                               font-size: 18px;
                               padding-right: 15px;
                               border-radius: 0px;
                               background-color: #262626;
                               }
                QLabel#region2{
                               font-family: Helvetica;
                               font-size: 14px;
                               padding-right: 15px;
                            }
                QLabel#bottomInfo{
                                font-size: 10px;
                                padding-left: 15px;
                }
                QPushButton {
                                font-size: 16px;
                                font-family: Helvetica;
                                font-weight: normal;
                                margin-right: 6px;
                                margin-bottom: 6px;
                                padding: 5px;

                }
                QLabel#mainDate{
                                font-size: 16px;
                                font-family: Helvetica;
                                font-weight: normal;
                                padding-bottom: 4px;
                }
                QLabel#otherDate{
                                font-size: 14px;
                }
            """)
        else:
            qdarktheme.setup_theme("light")
            self.setStyleSheet("""
                QPushButton#another_button {background-color:green; color:black; border-radius: 13px;}
                QLabel {border-radius: 0px}
                QLabel#mainTime {
                               font-size: 24px;}
                QLabel#title{
                                font-family: Helvetica;
                                font-size: 36px;
                                padding-left: 15px;
                            }
                QLabel#region{
                                font-family: Helvetica;
                                font-size: 22px;
                                padding-right: 15px;
                                padding-top: 15px;
                                padding-bottom: 5px;
                            }
                QLabel#leftTime{
                                font-family: Helvetica;
                               }
                QLabel#mainPrayerTime{
                               font-size: 18px;
                               padding-right: 15px;
                               border-radius: 0px;
                               background-color: #d9d9d9;
                               }
                QLabel#region2{
                               font-family: Helvetica;
                               font-size: 14px;
                               padding-right: 15px;
                            }
                QLabel#bottomInfo{
                                font-size: 10px;
                                padding-left: 15px;
                }
                QPushButton {
                                font-size: 16px;
                                font-family: Helvetica;
                                font-weight: normal;
                                margin-right: 6px;
                                margin-bottom: 6px;
                                padding: 5px;

                }
                QLabel#mainDate{
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
        self.mainLayout = QVBoxLayout(self)

        # title
        self.rightTitleLayout = QVBoxLayout()
        self.regionLoc = QLabel(f"{self.data.getLocation().getDescription()}", alignment=Qt.AlignRight | Qt.AlignTop, objectName="region")
        self.rightTitleLayout.addWidget(self.regionLoc)
        #self.rightTitleLayout.addWidget(QLabel("Scottsdale, Arizona", alignment=Qt.AlignRight | Qt.AlignTop, objectName="region"))
        #self.date = QLabel("May 30, 2025", alignment=Qt.AlignRight | Qt.AlignTop)
        #self.date.setObjectName("region2")
        #print(self.date.font())
        #self.rightTitleLayout.addWidget(self.date)
        self.rightTitleLayout.setSpacing(0)
        self.rightTitleLayout.setContentsMargins(0,0,0,0)

        self.titleLayout = QHBoxLayout()
        self.titleLayout.addWidget(QLabel("Prayer Times", alignment=Qt.AlignLeft | Qt.AlignVCenter, objectName="title"))
        self.titleLayout.setContentsMargins(0,0,0,0)
        self.titleLayout.setSpacing(0)

        self.titleLayout.addLayout(self.rightTitleLayout)

        #subtitle
        self.subtitleLayout = QHBoxLayout()
        #self.leftDate = QLabel("September 30, 2025", alignment=Qt.AlignCenter)
        #print("datetime:",self.data.getTodayDate())
        self.leftDate = QLabel(self.data.getYesterdayDate().strftime(self.dateFtime), alignment=Qt.AlignCenter)
        self.centerDate = QLabel(self.data.getTodayDate().strftime(self.dateFtime), alignment=Qt.AlignCenter)
        #print("center:",self.data.getTodayDate())
        self.rightDate = QLabel(self.data.getTomorrowDate().strftime(self.dateFtime), alignment=Qt.AlignCenter)
        self.centerDate.setObjectName("mainDate")
        self.leftDate.setObjectName("otherDate")
        self.rightDate.setObjectName("otherDate")
        self.subtitleLayout.addWidget(self.leftDate, 25)
        self.subtitleLayout.addWidget(self.centerDate, 50)
        self.subtitleLayout.addWidget(self.rightDate, 25)
        self.subtitleLayout.setSpacing(0)
        self.subtitleLayout.setContentsMargins(0,0,0,0)

        self.subLayout = QHBoxLayout()

        self.midLayout = QVBoxLayout()
        #fajr time
        self.fajr = QHBoxLayout()
        self.fajr_path_dark = resource_path("resources/maruf_assets/fajr.svg")
        self.fajr_path_light = resource_path("resources/maruf_assets/fajr_light.svg")
        self.fajrSvg = QSvgWidget(self.fajr_path_dark) if self.is_dark_theme() else QSvgWidget(self.fajr_path_light)
        self.fajrSvg.setFixedSize(300, 80) #forces fixed for other mainTimes as well
        self.fajr.addWidget(self.fajrSvg, alignment=Qt.AlignLeft)
        #self.fajrTime = QLabel(datetime.min.strftime("%I:%M %p"), alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.fajrTime = QLabel(self.data.prayerToday.fajr_time.strftime("%I:%M %p"), alignment=Qt.AlignCenter)
        #print(self.data.prayerToday)
        self.fajrTime.setObjectName("mainPrayerTime")
        self.fajrTime.setFixedWidth(100)
        self.fajr.addWidget(self.fajrTime)
        #sunrise time
        self.sunrise = QHBoxLayout()
        self.sunrise_path_dark = resource_path("resources/maruf_assets/sunrise.svg")
        self.sunrise_path_light = resource_path("resources/maruf_assets/sunrise_light.svg")
        self.sunriseSvg = QSvgWidget(self.sunrise_path_dark) if self.is_dark_theme() else QSvgWidget(self.sunrise_path_light)
        #self.sunriseSvg = QSvgWidget(resource_path("resources/maruf_assets/sunrise.svg"))
        self.sunriseSvg.setFixedSize(300, 80)
        self.sunrise.addWidget(self.sunriseSvg, 75, alignment=Qt.AlignLeft)
        #self.sunriseTime = QLabel(datetime.min.strftime("%I:%M %p"), alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.sunriseTime = QLabel(self.data.prayerToday.sunrise_time.strftime("%I:%M %p"), alignment=Qt.AlignCenter)
        self.sunriseTime.setObjectName("mainPrayerTime")
        self.sunriseTime.setFixedWidth(100)
        self.sunrise.addWidget(self.sunriseTime, 25)
        #self.sunrise.addWidget(self.sunriseTime)
        #dhuhr time
        self.dhuhr = QHBoxLayout()
        self.dhuhr_path_dark = resource_path("resources/maruf_assets/dhuhr.svg")
        self.dhuhr_path_light = resource_path("resources/maruf_assets/dhuhr_light.svg")
        self.dhuhrSvg = QSvgWidget(self.dhuhr_path_dark) if self.is_dark_theme() else QSvgWidget(self.dhuhr_path_light)
        #self.dhuhrSvg = QSvgWidget(resource_path("resources/maruf_assets/dhuhr.svg"))
        self.dhuhrSvg.setFixedSize(300, 80)
        self.dhuhr.addWidget(self.dhuhrSvg, 75, alignment=Qt.AlignLeft)
        #self.dhuhrTime = QLabel(datetime.min.strftime("%I:%M %p"), alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.dhuhrTime = QLabel(self.data.prayerToday.dhuhr_time.strftime("%I:%M %p"), alignment=Qt.AlignCenter)
        self.dhuhrTime.setObjectName("mainPrayerTime")
        self.dhuhr.addWidget(self.dhuhrTime, 25)
        #self.dhuhr.addWidget(self.dhuhrTime)
        #asr time
        self.asr = QHBoxLayout()
        self.asr_path_dark = resource_path("resources/maruf_assets/asr.svg")
        self.asr_path_light = resource_path("resources/maruf_assets/asr_light.svg")
        self.asrSvg = QSvgWidget(self.asr_path_dark) if self.is_dark_theme() else QSvgWidget(self.asr_path_light)
        #self.asrSvg = QSvgWidget(resource_path("resources/maruf_assets/asr.svg"))
        self.asrSvg.setFixedSize(300, 80)
        self.asr.addWidget(self.asrSvg, 75, alignment=Qt.AlignLeft)
        #self.asrTime = QLabel(datetime.min.strftime("%I:%M %p"), alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.asrTime = QLabel(self.data.prayerToday.asr_time.strftime("%I:%M %p"), alignment=Qt.AlignCenter)
        self.asrTime.setObjectName("mainPrayerTime")
        self.asr.addWidget(self.asrTime, 25)
        #maghrib time
        self.maghrib = QHBoxLayout()
        self.maghrib_path_dark = resource_path("resources/maruf_assets/maghrib.svg")
        self.maghrib_path_light = resource_path("resources/maruf_assets/maghrib_light.svg")
        self.maghribSvg = QSvgWidget(self.maghrib_path_dark) if self.is_dark_theme() else QSvgWidget(self.maghrib_path_light)
        #self.maghribSvg = QSvgWidget(resource_path("resources/maruf_assets/maghrib.svg"))
        self.maghribSvg.setFixedSize(300, 80)
        self.maghrib.addWidget(self.maghribSvg, 75, alignment=Qt.AlignLeft)
        #self.maghribTime = QLabel(datetime.min.strftime("%I:%M %p"), alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.maghribTime = QLabel(self.data.prayerToday.maghrib_time.strftime("%I:%M %p"), alignment=Qt.AlignCenter)
        self.maghribTime.setObjectName("mainPrayerTime")
        #self.maghrib.addWidget(self.maghribTime, 25)
        self.maghrib.addWidget(self.maghribTime, 25)
        #isha time
        self.isha = QHBoxLayout()
        self.isha_path_dark = resource_path("resources/maruf_assets/isha.svg")
        self.isha_path_light = resource_path("resources/maruf_assets/isha_light.svg")
        self.ishaSvg = QSvgWidget(self.isha_path_dark) if self.is_dark_theme() else QSvgWidget(self.isha_path_light)
        #self.ishaSvg = QSvgWidget(resource_path("resources/maruf_assets/isha.svg"))
        self.ishaSvg.setFixedSize(300, 80)
        self.isha.addWidget(self.ishaSvg, 75, alignment=Qt.AlignLeft)
        #self.ishaTime = QLabel(datetime.min.strftime("%I:%M %p"), alignment=Qt.AlignRight | Qt.AlignVCenter)
        self.ishaTime = QLabel(self.data.prayerToday.isha_time.strftime("%I:%M %p"), alignment=Qt.AlignCenter)
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
        #    label = QLabel(datetime.min.strftime("%I:%M:%S %p"), alignment=Qt.AlignCenter)
        #    label.setObjectName("mainTime")
        #    self.midLayout.addWidget(label)
        self.fajr.setContentsMargins(0,0,0,0)
        self.fajr.setSpacing(0)
        self.midLayout.setContentsMargins(0,0,0,0)
        self.midLayout.setSpacing(0)
        self.subMidWidget = QWidget()
        self.subMidWidget.setLayout(self.midLayout)
        self.subMidWidget.setFixedWidth(400)

        self.leftLayout = QVBoxLayout()
        for values in self.data.getPrayerYesterday().getPrayertimes().values():
            #label = QLabel(datetime.min.strftime("%I:%M:%S %p"), alignment=Qt.AlignCenter)
            label = QLabel(values.strftime("%I:%M %p"), alignment=Qt.AlignCenter)
            label.setObjectName("leftTime")
            self.leftLayout.addWidget(label)

        self.rightLayout = QVBoxLayout()
        for values in self.data.getPrayerTomorrow().getPrayertimes().values():
            label = QLabel(values.strftime("%I:%M %p"), alignment=Qt.AlignCenter)
            label.setObjectName("leftTime")
            self.rightLayout.addWidget(label)

        self.subLayout.addLayout(self.leftLayout, 25)
        #self.subLayout.addLayout(self.midLayout, 50)
        self.subLayout.addWidget(self.subMidWidget)
        self.subLayout.addLayout(self.rightLayout, 25)
        self.subLayout.setContentsMargins(0,0,0,0)
        self.subLayout.setSpacing(0)
        self.midWidget = QWidget()
        self.midWidget.setLayout(self.subLayout)
        self.midWidget.setFixedHeight(int(.8*600))
        #self.midWidget.setFixedWidth(400)

        # bottom
        self.bottomLayout = QHBoxLayout()
        self.bottomInfo = QLabel(self.data.getTzDesc(), alignment=Qt.AlignLeft | Qt.AlignVCenter)
        self.bottomInfo.setObjectName("bottomInfo")
        self.settingsButton = QPushButton(QIcon(resource_path("resources/maruf_assets/gear.png")), "Settings")
        self.settingsButton.setIconSize(QSize(24,24))
        self.settingsButton.setObjectName("settingsButton")
        self.bottomLayout.addWidget(self.bottomInfo)
        self.bottomLayout.addWidget(self.settingsButton, alignment=Qt.AlignRight | Qt.AlignBottom)
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
        #print(self.data.getAsrMethod())
        # update location
        self.regionLoc.setText(self.data.getLocation().getDescription())
        #print("set",self.data.getLocation().getDescription())
        # update dates
        self.leftDate.setText(self.data.getYesterdayDate().strftime(self.dateFtime))
        self.centerDate.setText(self.data.getTodayDate().strftime(self.dateFtime))
        self.rightDate.setText(self.data.getTomorrowDate().strftime(self.dateFtime))
        # update left layout (yesterday)
        yesterkeys = list(self.data.getPrayerYesterday().getPrayertimes().keys())
        for i in range(self.leftLayout.count()):
            item = self.leftLayout.itemAt(i)
            widget = item.widget()
            if widget and isinstance(widget, QLabel):
                key = yesterkeys[i]
                widget.setText(self.data.getPrayerYesterday().getPrayertimes()[key].strftime(self.timeFtime))

        # update right layout (tomorrow)
        tomorrow_keys = list(self.data.getPrayerTomorrow().getPrayertimes().keys())
        for i in range(self.rightLayout.count()):
            item = self.rightLayout.itemAt(i)
            widget = item.widget()
            if widget and isinstance(widget, QLabel):
                key = tomorrow_keys[i]
                widget.setText(self.data.getPrayerTomorrow().getPrayertimes()[key].strftime(self.timeFtime))

        # update mid layout (today)
        self.fajrTime.setText(self.data.getPrayerToday().getPrayertimes()["fajr"].strftime(self.timeFtime))
        self.sunriseTime.setText(self.data.getPrayerToday().getPrayertimes()["sunrise"].strftime(self.timeFtime))
        self.dhuhrTime.setText(self.data.getPrayerToday().getPrayertimes()["dhuhr"].strftime(self.timeFtime))
        self.asrTime.setText(self.data.getPrayerToday().getPrayertimes()["asr"].strftime(self.timeFtime))
        self.maghribTime.setText(self.data.getPrayerToday().getPrayertimes()["maghrib"].strftime(self.timeFtime))
        self.ishaTime.setText(self.data.getPrayerToday().getPrayertimes()["isha"].strftime(self.timeFtime))

        self.fajrSvg.load(self.fajr_path_dark) if self.is_dark_theme() else self.fajrSvg.load(self.fajr_path_light)
        self.sunriseSvg.load(self.sunrise_path_dark) if self.is_dark_theme() else self.sunriseSvg.load(self.sunrise_path_light)
        self.dhuhrSvg.load(self.dhuhr_path_dark) if self.is_dark_theme() else self.dhuhrSvg.load(self.dhuhr_path_light)
        self.asrSvg.load(self.asr_path_dark) if self.is_dark_theme() else self.asrSvg.load(self.asr_path_light)
        self.maghribSvg.load(self.maghrib_path_dark) if self.is_dark_theme() else self.maghribSvg.load(self.maghrib_path_light)
        self.ishaSvg.load(self.isha_path_dark) if self.is_dark_theme() else self.ishaSvg.load(self.isha_path_light)
        


    def recalculateData(self):
        self.data.genPrayerTimes()

    def dialog_finished(self):
        self.data.setDarkMode(self.dialog.darkModeSwitch.isChecked())
        self.data.setCalcMethod(self.dialog.calc_dropdown.currentData())
        #print(data.getCalcMethod())
        self.data.setAsrMethod(self.dialog.asrMethodDropdown.currentData())
        #print(f"asr: {self.data.getAsrMethod()}")
        self.threadz = QThread()
        self.worker = None
        self.loc_thread_done = False
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
            self.worker.error.connect(self.error_thread)
            self.worker.finished.connect(self.handle_result)
            self.worker.finished.connect(self.cleanup_thread)
            #self.threadz.finished.connect(self.threadz.deleteLater)

            self.timeout_timer = QTimer(self)
            self.timeout_timer.setSingleShot(True)
            self.timeout_timer.timeout.connect(self.timeout_thread)
            self.timeout_timer.start(8000) # allow 8 seconds to finish
            print("started timer")

            self.threadz.start()
            #self.threadz.join(5)
        print(f"Coords: {self.data.getLocation()}, {self.data.getLocation().getDescription()}")
        print("location finished")
        match self.dialog.utcOffsetBGroup.checkedId():
            case -1:
                print("no tz checked")
                if self.data.getTzMethod() != -1:
                    print("tz method changed...")
                    self.tz_method_changed = True

            case 0:
                print("tz by loc checked")
                if self.data.getTzMethod() != 0:
                    print("tz method changed...")
                    self.tz_method_changed = True
                    
            case 1:
                print("manual tz chosen")
                #self.data.setTzMethod(self.dialog.utcOffsetBGroup.checkedId())
                self.data.setUTCOffset(self.dialog.utcOffsetInput.currentData().total_seconds()/3600.0)
                self.data.setTzDesc(self.dialog.utcOffsetInput.currentText())
                #print(self.dialog.utcOffsetInput.currentData().total_seconds()/3600)
                self.data.setTzMethod(1)
                print(self.data.getUTCOffset(), self.data.getTzDesc())
            case 2:
                print("system tz chosen")
                if self.data.getTzMethod() != 2:
                    self.tz_method_changed = True
                    print("tz method changed...")
                    local_time = datetime.now().astimezone()
                    hours = local_time.utcoffset().total_seconds() / 3600.0
                    name = local_time.tzinfo.key if hasattr(local_time.tzinfo, 'key') else str(local_time.tzinfo)
                    self.data.setUTCOffset(hours)
                    display = f"(UTC{'+' if hours >= 0 else ''}{hours:0.1f}) {name}"
                    self.data.setTzDesc(display)
                    self.data.setTzMethod(2)
        print(f"timezone info: (utc_offset: {self.data.getUTCOffset()} desc: {self.data.getTzDesc()})")
        #self.data.setTzMethod(self.dialog.utcOffsetBGroup.checkedId())
        #self.data.setPrayerYesterday(zapp.PrayerTime(datetime.min.month, datetime.min.day, datetime.min.year))
        #self.data.setPrayerTomorrow(zapp.PrayerTime(datetime.min.month, datetime.min.day, datetime.min.year))
        #self.data.setPrayerToday(zapp.PrayerTime(datetime.min.month, datetime.min.day, datetime.min.year))
        self.data.setDate(self.dialog.get_selected_datetime())
        print(f"date: {self.data.getTodayDate()}")
        self.recalculateData()
        self.updateTimes()
        #self.__initUI()
        self.init_style()
        #self.set_style_color()
    
    def cleanup_thread(self):
        print("cleaning up threads...")
        self.threadz.quit()
        self.threadz.wait()
        self.worker.deleteLater()
        self.threadz.deleteLater()

    def error_thread(self, message):
        print("thread error...keeping location from before save...")
        self.loading_dialog.hide()
        self.timeout_timer.stop()
        self.threadz.quit()
        self.threadz.wait()

    def timeout_thread(self):
        if self.loc_thread_done:
            print("loc timed out!")
            self.threadz.quit()
            self.threadz.wait()

    def handle_result(self, result, mode):
        print("handling result...")
        self.loading_dialog.hide()
        print(f"got: {result}")
        self.data.setLocation(result)
        print("set", self.data.getLocation().getLatitude(), self.data.getLocation().getLongitude())
        self.regionLoc.setText(self.data.getLocation().getDescription())
        if mode == "byQuery":
            self.data.setLocationMethod(1)
        elif mode == "byIP":
            self.data.setLocationMethod(0)
        else:
            self.data.setLocationMethod(2)
        if self.data.getTzMethod() == 0:
            offset, name = pray_data.get_offset_name(lat=self.data.getLocation().getLatitude(), lng=self.data.getLocation().getLongitude())
            self.data.setUTCOffset(offset)
            self.data.setTzMethod(0)
            self.data.setTzDesc(name)
        print(f"set: {self.data.getTzDesc()}")
        self.recalculateData()
        self.updateTimes()
        self.threadz.quit()
        self.threadz.wait()
        self.worker.deleteLater()
        self.threadz.deleteLater()

    def dialog_rejected(self):
        print("rejected")


class SettingsDialog(QDialog):
    def __init__(self, parent=None, data=pray_data.Data(datetime.now(), pray_data.AppConfig())):
        super().__init__(parent)
    #    self.setStyleSheet('''
    #QLineEdit:disabled {
    #    color: gray;
    #    background-color: #262626;
    #    border: 1px solid #a0a0a0;
    #}
    #QLineEdit::enabled {
    #    color: black;
    #    background-color: #ffffff;
    #    border: 1px solid #a0a0a0}
    #    ''')
        #self.setFixedSize(640,480)
        self.setFixedWidth(480)
        self.setWindowTitle("Settings")
        self.data = data
        
        self.layout = QVBoxLayout()

        #self.layout.addWidget(QLabel("Settings"), 5, alignment=Qt.AlignHCenter | Qt.AlignTop)
        
        # dark mode
        self.darkModeGroup = QGroupBox("App Theme")
        self.darkModeVBox = QVBoxLayout()
        self.darkModeSwitch = QCheckBox("Dark Mode")
        self.darkModeVBox.addWidget(self.darkModeSwitch)
        self.darkModeGroup.setLayout(self.darkModeVBox)
        self.darkModeSwitch.setChecked(self.data.getDarkMode())

        # date/time
        self.dateTimeGroup = QGroupBox("Date")
        self.month_box = QComboBox()
        self.day_box = QComboBox()
        self.year_box = QComboBox()
        self.year_box.setFixedWidth(80)

        self.setup_date()

        self.dateTimeBox = QHBoxLayout()
        self.dateTimeBox.addWidget(QLabel("Month"))
        self.dateTimeBox.addWidget(self.month_box)
        self.dateTimeBox.addWidget(QLabel("Day"))
        self.dateTimeBox.addWidget(self.day_box)
        self.dateTimeBox.addWidget(QLabel("Year"))
        self.dateTimeBox.addWidget(self.year_box)
        self.dateTimeGroup.setLayout(self.dateTimeBox)

        # set current
        self.month_box.setCurrentText(str(self.data.todayDate.strftime("%B")))
        self.day_box.setCurrentText(str(self.data.todayDate.day))
        self.year_box.setCurrentText(str(self.data.todayDate.year))

        # asr method
        self.asrMethodGroup = QGroupBox("Asr Calculation Method")
        self.asrMethodDropdown = QComboBox()
        self.asrMethodDropdown.addItem("Shafi'i/Maliki/Hanbali", userData=1)
        self.asrMethodDropdown.addItem("Hanafi", userData=2)
        self.asrMethodDropdown.setCurrentIndex((self.data.getAsrMethod())-1)
        self.asrMethodBox = QVBoxLayout()
        self.asrMethodBox.addWidget(self.asrMethodDropdown)
        self.asrMethodGroup.setLayout(self.asrMethodBox)

        
        # calculation method
        self.calcMethodGroup = QGroupBox("Fajr/Isha Calculation Method")
        self.calcMethodVBox = QVBoxLayout()
        self.calc_dropdown = QComboBox()
        for name, method in CalcMethods.methods.items():
            self.calc_dropdown.addItem(str(name), userData=method)
        self.calc_dropdown.addItem(str(self.data.getCalcMethod().name), userData=self.data.getCalcMethod())
        self.calc_dropdown.setCurrentText(str(self.data.getCalcMethod()))
        self.calcMethodVBox.addWidget(self.calc_dropdown)
        self.calcMethodGroup.setLayout(self.calcMethodVBox)


        # location
        self.locationGroup = QGroupBox("Location Method")
        self.byIP = QRadioButton("IPv4 Address (internet required)")
        self.byQuery = QRadioButton("Query to Nominatim Service (internet required)")
        self.byHand = QRadioButton("Manual Latitude and Longitude")
        self.locationVBox = QVBoxLayout()
        self.locationVBox.addStretch(1)
        self.locationGroup.setLayout(self.locationVBox)
        # button group
        self.locationBGroup = QButtonGroup()
        self.locationBGroup.addButton(self.byIP, id=0)
        self.locationBGroup.addButton(self.byQuery, id=1)
        self.locationBGroup.addButton(self.byHand, id=2)
        self.locationBGroup.setExclusive(True)
        self.locationBGroup.button(self.data.getLocationMethod()).setChecked(True)
        self.locationBGroup.buttonClicked.connect(self.update_location_options)
        # line edits
        # latitude
        self.manualTooltip = "Enable Manual Latitude and Longitude Option to Edit"
        self.latitude = QLineEdit()
        self.latitude.setPlaceholderText("Latitude")
        self.latitude.setEnabled(False)
        self.latitude.setToolTip(self.manualTooltip)
        # longitude
        self.longitude = QLineEdit()
        self.longitude.setPlaceholderText("Longitude")
        self.longitude.setEnabled(False)
        self.longitude.setToolTip(self.manualTooltip)
        # query
        self.query = QLineEdit()
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

        # Timezone/UTC Offset
        self.utcOffsetGroup = QGroupBox("Timezone")
        self.tzBySystem = QRadioButton("Set Timezone By System Settings")
        self.tzBySystem.setToolTip("Maruf will fetch your system timezone settings")
        self.tzByLocation = QRadioButton("Set Timezone By Location")
        self.tzByHand = QRadioButton("Set Timezone Manually")
        # button group
        self.utcOffsetBGroup = QButtonGroup()
        self.utcOffsetBGroup.addButton(self.tzBySystem, id =2)
        self.utcOffsetBGroup.addButton(self.tzByLocation, id=0)
        self.utcOffsetBGroup.addButton(self.tzByHand, id=1)
        self.utcOffsetBGroup.setExclusive(True)
        # combo box
        self.utcOffsetInput = QComboBox()
        self.utcOffsetInput.setEnabled(False)
        self.utcOffsetInput.setToolTip("Enable Set Timezone Manually to Edit")
        self.populate_timezones()
        self.utcOffsetBGroup.button(self.data.getTzMethod()).setChecked(True)
        self.utcOffsetBGroup.buttonClicked.connect(self.update_tz_options)
        match self.data.getTzMethod():
            case 0:
                pass
            case 1:
                self.utcOffsetInput.setEnabled(True)
                self.utcOffsetInput.setCurrentText(self.data.getTzDesc())
            case 2:
                pass

        # VBox
        self.utcOffsetVBox = QVBoxLayout()
        self.utcOffsetGroup.setLayout(self.utcOffsetVBox)
        self.utcOffsetVBox.addWidget(self.tzBySystem)
        self.utcOffsetVBox.addWidget(self.tzByLocation)
        self.utcOffsetVBox.addWidget(self.tzByHand)
        self.utcOffsetVBox.addWidget(self.utcOffsetInput)


        # cancel/save button
        #self.save_button = QPushButton("Save")
        #self.save_button.clicked.connect(self.accept)
        #self.close_button = QPushButton("Cancel")
        #self.close_button.clicked.connect(self.reject)
        #self.closeLayout = QHBoxLayout()
        #self.closeLayout.addWidget(self.close_button, 50)
        #self.closeLayout.addWidget(self.save_button, 50)
        
        self.closeButtons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.closeButtons.accepted.connect(self.accept)
        self.closeButtons.rejected.connect(self.reject)
        #self.closeButtons.setCenterButtons(True)


        #self.layout.addWidget(QSpacerItem(20,40))
        self.layout.addWidget(self.darkModeGroup)
        self.layout.addWidget(self.dateTimeGroup)
        self.layout.addWidget(self.asrMethodGroup)
        self.layout.addWidget(self.locationGroup)
        self.layout.addWidget(self.calcMethodGroup)
        #self.layout.addLayout(self.closeLayout)
        self.layout.addWidget(self.utcOffsetGroup)
        self.layout.addWidget(self.closeButtons)

        self.setLayout(self.layout)

    def populate_timezones(self):
        #now = datetime.utcnow()
        now = datetime.now(UTC).now()

        tz_entries = []
        for name in sorted(available_timezones()):
            try:
                tz = ZoneInfo(name)
                offset = now.astimezone(tz).utcoffset()
                if offset is not None:
                    hours = offset.total_seconds() / 3600
                    display = f"(UTC{'+' if hours >= 0 else ''}{hours:0.1f}) {name}"
                    tz_entries.append((offset, display))
            except Exception:
                continue  # skip broken ones
        # Sort by offset then by name
        tz_entries.sort()
        for utc_timedelta, display in tz_entries:
            self.utcOffsetInput.addItem(display, userData=utc_timedelta)


    def update_location_options(self):
        is_custom = self.byHand.isChecked()
        is_query = self.byQuery.isChecked()

        self.latitude.setEnabled(is_custom)
        self.longitude.setEnabled(is_custom)
        self.query.setEnabled(is_query)

    def update_tz_options(self):
        #is_system = self.tzBySystem.isChecked()
        #is_location = self.tzByLocation.isChecked()
        is_custom = self.tzByHand.isChecked()

        self.utcOffsetInput.setEnabled(is_custom)
        
    def setup_date(self):
        # def not copy/p
        # Populate months
        for month in range(1, 13):
            month_name = QDate(2000, month, 1).toString("MMMM")
            self.month_box.addItem(month_name, month)

        # Populate years (example: from 1950 to current year + 10)
        current_year = QDate.currentDate().year()
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

        days_in_month = QDate(year, month, 1).daysInMonth()
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
        return QDate(year, month, day)

    def get_selected_datetime(self):
        year = int(self.year_box.currentText())
        month = self.month_box.currentData()
        day = int(self.day_box.currentText())
        return datetime(year, month, day)



class LoadingDialog(QDialog):
    def __init__(self, parent=None, display="Loading..."):
        super().__init__(parent)
        self.setFixedSize(250,100)
        self.setModal(True)
        self.setWindowTitle("Loading")
        self.spinner_label = QLabel(self)
        self.movie = QMovie(resource_path("resources/maruf_assets/rolling.gif"))
        self.spinner_label.setMovie(self.movie)
        self.movie.setScaledSize(QSize(32,32))
        self.movie.start()

        layout = QVBoxLayout()
        layout.addWidget(QLabel(display), alignment=Qt.AlignCenter)
        layout.addWidget(self.spinner_label, alignment=Qt.AlignCenter)
        self.setLayout(layout)



class WebRequestWorker(QObject):
    finished = Signal(object, str)
    error = Signal(str)

    def __init__(self, mode: str, query=""):
        super().__init__()
        self.mode = mode
        self.query = query
        self.location = zapp.Location()

    @Slot()
    def run(self):
        import traceback
        try:
            if self.mode == "byIP":
                self.location.setLocationByIP()
            elif self.mode == "byQuery":
                self.location.setLocationByQuery(self.query)
            else:
                self.location = zapp.Location()
            self.finished.emit(self.location, self.mode)
        except Exception:
            err_msg = traceback.format_exc()
            self.error.emit(err_msg)



# internet connection check
def is_connected(hostname, isConnected: list):
    import socket
    try:
        # see if we can do a dns lookup, return True if it can happen
        host = socket.gethostbyname(hostname)
        s = socket.create_connection((host, 80), 2)
        s.close()
        isConnected.value = True
        return
    except Exception:
        pass # ignore errors and return False
    isConnected.value = False
    #return

if __name__ == "__main__":
    freeze_support()
    app = QApplication([])

    # 1. Show splash screen
    #splash_pix = QPixmap(400, 300)
    #splash_pix.fill(Qt.black)  # You can use an image instead
    #splash = QSplashScreen(splash_pix)
    #splash.showMessage("Loading app...", Qt.AlignBottom | Qt.AlignCenter, Qt.white)
    #splash.show()

    #settingsDialog = LoadingDialog()
    #settingsDialog.show()
    #app.processEvents()
    #atime.sleep(4)
    conf_file_exists = os.path.exists("config.toml")
    appConfig = pray_data.AppConfig()

    midnight_today = datetime.combine(datetime.today(), time.min)
    # holds data for app during runtime (app does not store information otherwise)
    data = pray_data.Data(midnight_today, appConfig)

    #print("midnight: ",data.getTodayDate())
    hostname = "one.one.one.one" # check for 1.1.1.1 to dns lookup
    #isConnected = [False]
    isConnected = Value('b', False)
    if not conf_file_exists:
        checkInternet = Process(target=is_connected, args=(hostname, isConnected))
        checkInternet.start()
        print("[+] checking internet connectivity...")
        checkInternet.join(4) # allow 4 seconds for connection to be made, otherwise kill
        if checkInternet.is_alive():
            print("[-] dns lookup timeout, terminating process...")
            checkInternet.kill()
            checkInternet.join()
        if isConnected.value:
            print("[+] internet connectivity check succeeded...")
        else:
            print("[-] internet connectivity check failed...")
        #print("[+] internet connectivity check finished")


    #qdarktheme.setup_theme("dark", corner_shape="sharp")
    qdarktheme.setup_theme("dark")
    data.setDarkMode(True)
    app.setWindowIcon(QIcon(resource_path("resources/maruf_assets/maruf_icon.png")))
    
    widget = MyWidget(isConnected.value, data, conf_file_exists)
    #widget = MyWidget(True, data)

    widget.setWindowIcon(QIcon(resource_path("resources/maruf_assets/maruf_icon.png")))
    widget.setFixedSize(800, 600)
    #settingsDialog.accept()
    widget.show()    # 4. Close splash
    #splash.finish(main_win)
    app.exec()
    data.exportConfigToFile()
    sys.exit()
