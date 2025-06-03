#import app
from app import PrayerTime, CalcMethod, Location
from datetime import datetime, timedelta, timezone
import time
#from dateutil.relativedelta import relativedelta



class Data():
    def __init__(self, grok: datetime):
        self.location = Location()
        #print("Data1: ",grok)
        yesterday = grok + timedelta(days=-1)
        tomorrow = grok + timedelta(days=1)
        self.todayDate = grok
        #print("self",self.todayDate)
        self.yesterdayDate = yesterday
        self.tomorrowDate = tomorrow

        #self.location = {"latitude": 0.0, "longitude": 0.0, "description": ""}

        self.calcMethod = CalcMethod()

        self.asrMethod = 1
        
        self.locationMethod = 0
        self.query = ""
        system_time = time.time()
        self.utc_offset = ((datetime.fromtimestamp(system_time).timestamp()) - datetime.fromtimestamp(system_time, timezone.utc).replace(tzinfo=None).timestamp())/3600.0
        #print("UTC offset: ",self.utc_offset)

        self.prayerYesterday = PrayerTime(self.yesterdayDate.month, self.yesterdayDate.day, self.yesterdayDate.year, self.getUTCOffset(), self.getCalcMethod(), 1, "", self.getLocation().getLatitude(), self.getLocation().getLongitude())
        self.prayerToday = PrayerTime(self.todayDate.month, self.todayDate.day, self.todayDate.year, self.getUTCOffset(), self.getCalcMethod(), 1, "", self.getLocation().getLatitude(), self.getLocation().getLongitude())
        self.prayerTomorrow = PrayerTime(self.tomorrowDate.month, self.tomorrowDate.day, self.tomorrowDate.year, self.getUTCOffset(), self.getCalcMethod(), 1, "", self.getLocation().getLatitude(), self.getLocation().getLongitude())

    def genPrayerTimes(self):
        self.prayerYesterday = PrayerTime(self.yesterdayDate.month, self.yesterdayDate.day, self.yesterdayDate.year, self.getUTCOffset(), self.getCalcMethod(), self.getAsrMethod(), self.getLocation().getDescription(), self.getLocation().getLatitude(), self.getLocation().getLongitude())
        self.prayerToday = PrayerTime(self.todayDate.month, self.todayDate.day, self.todayDate.year, self.getUTCOffset(), self.getCalcMethod(), self.getAsrMethod(), self.getLocation().getDescription(), self.getLocation().getLatitude(), self.getLocation().getLongitude())
        self.prayerTomorrow = PrayerTime(self.tomorrowDate.month, self.tomorrowDate.day, self.tomorrowDate.year, self.getUTCOffset(), self.getCalcMethod(), self.getAsrMethod(), self.getLocation().getDescription(), self.getLocation().getLatitude(), self.getLocation().getLongitude())

    def setPrayerYesterday(self, prayerTime: PrayerTime):
        self.prayerYesterday = prayerTime

    def setPrayerToday(self, prayerTime: PrayerTime):
        self.prayerToday = prayerTime

    def setPrayerTomorrow(self, prayerTime: PrayerTime):
        self.prayerTomorrow = prayerTime

    def setLocation(self, location: Location):
        self.location = location
    
    def setLocationMethod(self, locationMethodIndex):
        self.locationMethod = locationMethodIndex

    def setCalcMethod(self, calcMethod: CalcMethod):
        self.calcMethod = calcMethod

    def setAsrMethod(self, multiplier: int):
        self.asrMethod = multiplier

    def setQuery(self, query: str):
        self.query = query

    def setDate(self, dateTime: datetime):
        self.todayDate = dateTime
        self.yesterdayDate = dateTime + timedelta(days=-1)
        self.tomorrowDate = dateTime + timedelta(days=1)

    def setTodayDate(self, dateTime: datetime):
        self.todayDate = dateTime

    def setYesterdayDate(self, dateTime: datetime):
        self.yesterdayDate = dateTime

    def setTomorrowDate(self, dateTime: datetime):
        self.tomorrowDate = dateTime

    def getPrayerYesterday(self) -> PrayerTime:
        return self.prayerYesterday
    
    def getPrayerToday(self) -> PrayerTime:
        return self.prayerToday

    def getPrayerTomorrow(self) -> PrayerTime:
        return self.prayerTomorrow

    def getCalcMethod(self) -> CalcMethod:
        return self.calcMethod
    
    # return asr multiplier
    def getAsrMethod(self) -> int:
        return self.asrMethod

    def getLocation(self) -> Location:
        return self.location
    
    def getLocationMethod(self) -> int:
        return self.locationMethod
    
    def getQuery(self) -> str:
        return self.query

    def getTodayDate(self) -> datetime:
        return self.todayDate
    
    def getYesterdayDate(self) -> datetime:
        return self.yesterdayDate
    
    def getTomorrowDate(self) -> datetime:
        return self.tomorrowDate

    def getUTCOffset(self) -> float:
        return self.utc_offset
