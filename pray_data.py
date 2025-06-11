#import app
from app import PrayerTime, CalcMethod, Location, getLocalUTCOffset
from datetime import datetime, timedelta, timezone, UTC
import time
import toml
from timezonefinder import TimezoneFinderL
from zoneinfo import ZoneInfo
#from dateutil.relativedelta import relativedelta
import timeit

#lat, lng to utc_offset
def get_offset_name(*, lat, lng):
    start = timeit.timeit()

    """
    Returns a location's time zone offset from UTC in minutes using zoneinfo.
    """
    #print("clang: ", TimezoneFinder.using_clang_pip())  # returns True or False
    tf = TimezoneFinderL(in_memory=True)
    #tz_name = tf.certain_timezone_at(lat=lat, lng=lng)
    tz_name = tf.timezone_at(lat=lat, lng=lng)

    now = datetime.now(UTC).now()

    if tz_name is None:
        raise ValueError("Could not determine the timezone for the given coordinates")

    tz = ZoneInfo(tz_name)
        
    offset = now.astimezone(tz).utcoffset()
    if offset is None:
        hours = None
        display = None
    if offset is not None:
        hours = offset.total_seconds() / 3600
        display = f"(UTC{'+' if hours >= 0 else ''}{hours:0.1f}) {tz_name}"   #now_utc = datetime.now(tz=ZoneInfo("UTC"))
    #now_local = now_utc.astimezone(ZoneInfo(tz_name))
    #offset_seconds = (now_local.utcoffset().total_seconds())
    end = timeit.timeit()
    print(end-start)
    return hours, display



# class for handling toml configuration file
class AppConfig:
    def __init__(self, path="config.toml"):
        print("configuring from file...")
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
        offset, name = get_offset_name(lat=34.1434, lng=-111.1230)
        return{
            #"general":{"dark_mode": True, "utc_offset_timezone": getLocalUTCOffset(time.time())},
            "general":{"dark_mode": True, "timezone_utc_offset": offset, "timezone_description": name},
            "prayer_times":{"method_name": "From File: ISNA", "fajr_angle": 15, "isha_angle": -15, "maghrib_to_isha_90": False, "asr_method": 2},
            "location":{"latitude": 34.1434, "longitude": -111.123, "region_description": "Phoenix, AZ"}
        }

    def conf_exists(self) -> bool:
        try:
            toml.load(self.path)
            return True
        except FileNotFoundError:
            return False

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

        self.darkMode = True


        #self.asrMethod = 1
        
        self.locationMethod = 0
        
        # timezone vars
        offset_tz, desc = get_offset_name(lat=self.location.getLatitude(), lng=self.location.getLongitude())
        self.tzMethod = 0 # from location ^
        self.tzDesc = desc
        #self.utc_offset = ((datetime.fromtimestamp(system_time).timestamp()) - datetime.fromtimestamp(system_time, timezone.utc).replace(tzinfo=None).timestamp())/3600.0 # from system
        self.utc_offset = offset_tz

        self.query = ""
        system_time = time.time()
        #print("UTC offset: ",self.utc_offset)

        self.prayerYesterday = PrayerTime(self.yesterdayDate.month, self.yesterdayDate.day, self.yesterdayDate.year, self.getUTCOffset(), self.getCalcMethod(), 1, "", self.getLocation().getLatitude(), self.getLocation().getLongitude())
        self.prayerToday = PrayerTime(self.todayDate.month, self.todayDate.day, self.todayDate.year, self.getUTCOffset(), self.getCalcMethod(), 1, "", self.getLocation().getLatitude(), self.getLocation().getLongitude())
        self.prayerTomorrow = PrayerTime(self.tomorrowDate.month, self.tomorrowDate.day, self.tomorrowDate.year, self.getUTCOffset(), self.getCalcMethod(), 1, "", self.getLocation().getLatitude(), self.getLocation().getLongitude())


    def genPrayerTimes(self):
        self.prayerYesterday = PrayerTime(self.yesterdayDate.month, self.yesterdayDate.day, self.yesterdayDate.year, self.getUTCOffset(), self.getCalcMethod(), self.getAsrMethod(), self.getLocation().getDescription(), self.getLocation().getLatitude(), self.getLocation().getLongitude())
        self.prayerToday = PrayerTime(self.todayDate.month, self.todayDate.day, self.todayDate.year, self.getUTCOffset(), self.getCalcMethod(), self.getAsrMethod(), self.getLocation().getDescription(), self.getLocation().getLatitude(), self.getLocation().getLongitude())
        self.prayerTomorrow = PrayerTime(self.tomorrowDate.month, self.tomorrowDate.day, self.tomorrowDate.year, self.getUTCOffset(), self.getCalcMethod(), self.getAsrMethod(), self.getLocation().getDescription(), self.getLocation().getLatitude(), self.getLocation().getLongitude())


    def exportConfigToFile(self):
        self.config.data["general"]["timezone_utc_offset"] = self.getUTCOffset()
        #offset, name = get_offset_name(lat=34.1434, lng=-111.1230)
        self.config.data["general"]["timezone_description"] = self.getTzDesc()

        self.config.data["prayer_times"]["method_name"] = self.getCalcMethod().name
        self.config.data["prayer_times"]["fajr_angle"] = self.getCalcMethod().fajr_angle
        self.config.data["prayer_times"]["isha_angle"] = self.getCalcMethod().isha_angle
        self.config.data["prayer_times"]["maghrib_to_isha_90"] = self.getCalcMethod().fixed
        self.config.data["prayer_times"]["asr_method"] = self.getAsrMethod()

        self.config.data["location"]["latitude"] = self.getLocation().getLatitude()
        print("latitude", self.getLocation().getLatitude())
        self.config.data["location"]["longitude"] = self.getLocation().getLongitude()
        self.config.data["location"]["region_description"] = self.getLocation().getDescription()

        self.config.save()
        print("saving config to file...")


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

    def setUTCOffset(self, offset: float):
        self.utc_offset = offset

    def setTzMethod(self, index: int):
        self.tzMethod = index

    def setTzDesc(self, desc: str):
        self.tzDesc = desc

    def setDarkMode(self, mode: bool):
        self.darkMode = mode

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
    
    def getTzMethod(self) -> int:
        return self.tzMethod

    def getTzDesc(self) -> str:
        return self.tzDesc
    
    def getDarkMode(self) -> bool:
        return self.darkMode
