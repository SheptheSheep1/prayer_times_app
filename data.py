#import app
from app import PrayerTime, CalcMethod


class Data():
    def __init__(self):
        self.prayerYesterday = PrayerTime()
        self.prayerToday = PrayerTime()
        self.prayerTomorrow = PrayerTime()

        self.location = {"latitude": 0.0, "longitude": 0.0, "description": ""}

        self.calcMethod = CalcMethod()

    def setPrayerYesterday(self, prayerTime: PrayerTime):
        self.prayerYesterday = prayerTime

    def setPrayerToday(self, prayerTime: PrayerTime):
        self.prayerToday = prayerTime

    def setPrayerTomorrow(self, prayerTime: PrayerTime):
        self.prayerTomorrow = prayerTime

    def setLocation(self, location: dict):
        self.location = location

    def setCalcMethod(self, calcMethod: CalcMethod):
        self.calcMethod = calcMethod

    def getPrayerYesterday(self) -> PrayerTime:
        return self.prayerYesterday
    
    def getPrayerToday(self) -> PrayerTime:
        return self.prayerToday

    def getPrayerTomorrow(self) -> PrayerTime:
        return self.prayerTomorrow
    
    #TODO: Implement Location class in app.py

    def getCalcMethod(self) -> CalcMethod:
        return self.calcMethod
