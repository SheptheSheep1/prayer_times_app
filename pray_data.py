#import app
from app import PrayerTime, CalcMethod, Location, getLocalUTCOffset
from datetime import datetime, timedelta, timezone
import time
import toml
#from dateutil.relativedelta import relativedelta


# class for handling toml configuration file
class AppConfig:
    def __init__(self, path="config.toml"):
        self.path = path
        self.data = self.load()

    def load(self):
        try:
            return toml.load(self.path)
        except FileNotFoundError:
            return self.default()

    def save(self):
        with open(self.path, "w") as f:
            toml.dump(self.data, f)

    def default(self):
        return{
            "general":{"dark_mode": True, "utc_offset_timezone": getLocalUTCOffset(time.time())},
            "prayer_times":{"method_name": "From File", "fajr_angle": 15, "isha_angle": -15, "maghrib_to_isha_90": False, "asr_method": 2},
            "location":{"latitude": 34.1434, "longitude": -111.123, "region_description": "Phoenix, AZ"}
        }

    def setData(self, data:dict):
        self.data=data


class Data():
    def __init__(self, grok: datetime, config: AppConfig):
        self.config = config
        # load config values
        self.location = Location(self.config.data["location"]["latitude"], self.config.data["location"]["longitude"], self.config.data["location"]["region_description"])
        self.calcMethod = CalcMethod(self.config.data["prayer_times"]["method_name"], self.config.data["prayer_times"]["fajr_angle"])
        self.asrMethod = self.config.data["prayer_times"]["asr_method"]


        #self.location = Location()
        #print("Data1: ",grok)
        yesterday = grok + timedelta(days=-1)
        tomorrow = grok + timedelta(days=1)
        self.todayDate = grok
        #print("self",self.todayDate)
        self.yesterdayDate = yesterday
        self.tomorrowDate = tomorrow




        #self.asrMethod = 1
        
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

    def exportConfigToFile(self):
        self.config.data["general"]["utc_offset_timezone"] = self.getUTCOffset()

        self.config.data["prayer_times"]["fajr_angle"] = self.getCalcMethod().fajr_angle
        self.config.data["prayer_times"]["isha_angle"] = self.getCalcMethod().isha_angle
        self.config.data["prayer_times"]["maghrib_to_isha_90"] = self.getCalcMethod().fixed
        self.config.data["prayer_times"]["asr_method"] = self.getAsrMethod()

        self.config.data["location"]["latitude"] = self.getLocation().getLatitude()
        self.config.data["location"]["longitude"] = self.getLocation().getLongitude()
        self.config.data["location"]["region_description"] = self.getLocation().getDescription()

        self.config.save()

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
