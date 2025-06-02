#import app
from app import PrayerTime, CalcMethod, Location


class Data():
    def __init__(self):
        self.prayerYesterday = PrayerTime()
        self.prayerToday = PrayerTime()
        self.prayerTomorrow = PrayerTime()

        #self.location = {"latitude": 0.0, "longitude": 0.0, "description": ""}
        self.location = Location()

        self.calcMethod = CalcMethod()

        self.asrMethod = 1
        
        self.locationMethod = 0
        self.query = ""

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
    
    def getLocationMethod(self):
        return self.locationMethod
    
    def getQuery(self) -> str:
        return self.query
