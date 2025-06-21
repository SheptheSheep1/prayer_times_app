#import app
from app import PrayerTime, CalcMethod, Location
from datetime import datetime, timedelta, UTC
import re
import time
import toml
from timezonefinder import TimezoneFinderL
from zoneinfo import ZoneInfo, available_timezones
#from dateutil.relativedelta import relativedelta
import timeit
max_len_region_desc = 90
max_len_method_name = 50
timezone_description = 80


def get_valid_utc_offsets():
    offsets = set()
    now = datetime.now()
    for tz_name in available_timezones():
        tz = ZoneInfo(tz_name)
        offset = tz.utcoffset(now)
        if offset is not None:
            offsets.add(offset.total_seconds() / 3600)
    return sorted(offsets)

def get_valid_tz_names():
    pass


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
        raise ValueError(f"Invalid timezone: {tz}")
    hours = offset.total_seconds() / 3600
    display = f"(UTC{'+' if hours >= 0 else ''}{hours:0.1f}) {tz_name}"   #now_utc = datetime.now(tz=ZoneInfo("UTC"))
    #now_local = now_utc.astimezone(ZoneInfo(tz_name))
    #offset_seconds = (now_local.utcoffset().total_seconds())
    end = timeit.timeit()
    #print(end-start)
    return hours, display



# class for handling toml configuration file
class AppConfig:
    def __init__(self, path="config.toml"):
        #print("configuring from file...")
        self.path = path
        #self.data = self.load()

    def setDataLoad(self) -> None:
        self.data=self.load()

    def load(self):
        try:
            config = toml.load(self.path)
            self.checkConfig(config)
            return config
        except ValueError as e:
            print(f"invalid toml...{e}loading default values...")
            return self.default()
        except FileNotFoundError:
            return self.default()
        except PermissionError as e:
            print(f"Permission denied while reading from {self.path}: {e}")
            return self.default()
        except OSError as e:
            print(f"OS error while reading from file {self.path}: {e}")
            return self.default()


    def save(self):
        try:
            with open(self.path, "w") as f:
                toml.dump(self.data, f)
        except PermissionError as e:
            print(f"Permission denied while writing to {self.path}: {e}")
            raise e
        except OSError as e:
            print(f"OS error while saving file {self.path}: {e}")
            raise e

    def default(self):
        try: 
            #offset, name = get_offset_name(lat=34.1434, lng=-111.1230)
            offset = -7.0
            name = "(UTC-7.0) America/Phoenix"
        except ValueError as e:
            print("Could not find offset from coordinates... {e}... Using defaults")
            offset = -7.0
            name = "(UTC-7.0) America/Phoenix"
        return{
            #"general":{"dark_mode": True, "utc_offset_timezone": -7.0},
            "general":{"dark_mode": True, "timezone_utc_offset": offset, "timezone_description": name},
            "prayer_times":{"method_name": "From File: ISNA", "fajr_offset": 15.0, "isha_offset": 15.0, "maghrib_to_isha_90": False, "asr_method": 2},
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
    

    def validate_config_types(self, config: dict):
        #print(type(config["prayer_times"]["fajr_offset"]), config["prayer_times"]["fajr_offset"])
        errors = []
    
        try:
            general = config["general"]
            if not isinstance(general.get("dark_mode"), bool):
                errors.append("general.dark_mode must be a bool")
            if not isinstance(general.get("timezone_utc_offset"), float):
                errors.append("general.timezone_utc_offset must be a float")
            if not isinstance(general.get("timezone_description"), str):
                errors.append("general.timezone_description must be a string")
        except KeyError as e:
            errors.append(f"Missing key in general: {e}")
    
        try:
            prayer = config["prayer_times"]
            if not isinstance(prayer.get("method_name"), str):
                errors.append("prayer_times.method_name must be a string")
            if not isinstance(prayer.get("fajr_offset"), float):
                errors.append("prayer_times.fajr_offset must be a float")
            if not isinstance(prayer.get("isha_offset"), float):
                errors.append("prayer_times.isha_offset must be a float")
            if not isinstance(prayer.get("maghrib_to_isha_90"), bool):
                errors.append("prayer_times.maghrib_to_isha_90 must be a bool")
            if not isinstance(prayer.get("asr_method"), int):
                errors.append("prayer_times.asr_method must be an int")
        except KeyError as e:
            errors.append(f"Missing key in prayer_times: {e}")
    
        try:
            loc = config["location"]
            if not isinstance(loc.get("latitude"), float):
                errors.append("location.latitude must be a float")
            if not isinstance(loc.get("longitude"), float):
                errors.append("location.longitude must be a float")
            if not isinstance(loc.get("region_description"), str):
                errors.append("location.region_description must be a string")
        except KeyError as e:
            errors.append(f"Missing key in location: {e}")
    
        if errors:
            raise ValueError("Config validation failed:\n" + "\n".join(errors))

    def truncate_with_ellipsis(self, s: str, max_length: int) -> str:
        if len(s) <= max_length:
            return s
        elif max_length <= 1:
            return "…"[:max_length]  # fallback if max_length is too small
        else:
            return s[:max_length - 1] + "…"

    def checkConfig(self, config):
        self.validate_config_types(config)
        if config["general"]["timezone_utc_offset"] in get_valid_utc_offsets():
            pass
        else:
            raise ValueError(f"invalid utc offset {config["general"]["timezone_utc_offset"]}")
        match = re.fullmatch(r"\(UTC([+-]?\d+(?:\.\d+)?)\)\s+(.+)", config["general"]["timezone_description"] or "")
        if not match:
            raise ValueError("Invalid timezone_description format. Expected: (UTC±offset) TimezoneName, using *nix/IANA standard tz/names")
        else:
            pass
        #self.truncate_with_ellipsis(config["general"]["timezone_description"])
        config["prayer_times"]["method_name"] = self.truncate_with_ellipsis(config["prayer_times"]["method_name"], max_len_method_name)
        config["location"]["region_description"]= self.truncate_with_ellipsis(config["location"]["region_description"], max_len_region_desc)


class Data():
    def __init__(self, grok: datetime, config: AppConfig):
        #print("data init...")
        self.config = config
        # load config values
        self.location = Location(self.config.data["location"]["latitude"], self.config.data["location"]["longitude"], self.config.data["location"]["region_description"])
        self.calcMethod = CalcMethod(self.config.data["prayer_times"]["method_name"], self.config.data["prayer_times"]["fajr_offset"], self.config.data["prayer_times"]["isha_offset"])
        self.asrMethod = self.config.data["prayer_times"]["asr_method"]
        #print("...")
        
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
        #offset_tz, desc = get_offset_name(lat=self.location.getLatitude(), lng=self.location.getLongitude())
        #print("...")
        self.tzMethod = 0 # from location ^
        #self.tzDesc = desc
        self.tzDesc = self.config.data["general"]["timezone_description"]
        #self.utc_offset = ((datetime.fromtimestamp(system_time).timestamp()) - datetime.fromtimestamp(system_time, timezone.utc).replace(tzinfo=None).timestamp())/3600.0 # from system
        #self.utc_offset = offset_tz
        self.utc_offset = self.config.data["general"]["timezone_utc_offset"]

        self.query = ""
        #system_time = time.time()
        #print("UTC offset: ",self.utc_offset)

        #self.prayerYesterday = PrayerTime(self.yesterdayDate.month, self.yesterdayDate.day, self.yesterdayDate.year, self.getUTCOffset(), self.getCalcMethod(), 1, "", self.getLocation().getLatitude(), self.getLocation().getLongitude())
        #self.prayerToday = PrayerTime(self.todayDate.month, self.todayDate.day, self.todayDate.year, self.getUTCOffset(), self.getCalcMethod(), 1, "", self.getLocation().getLatitude(), self.getLocation().getLongitude())
        #self.prayerTomorrow = PrayerTime(self.tomorrowDate.month, self.tomorrowDate.day, self.tomorrowDate.year, self.getUTCOffset(), self.getCalcMethod(), 1, "", self.getLocation().getLatitude(), self.getLocation().getLongitude())
        #print("...")


    def genPrayerTimes(self):
        self.prayerYesterday = PrayerTime(self.yesterdayDate.month, self.yesterdayDate.day, self.yesterdayDate.year, self.getUTCOffset(), self.getCalcMethod(), self.getAsrMethod(), self.getLocation().getDescription(), self.getLocation().getLatitude(), self.getLocation().getLongitude())
        self.prayerYesterday.putPrayerTimes()
        self.prayerToday = PrayerTime(self.todayDate.month, self.todayDate.day, self.todayDate.year, self.getUTCOffset(), self.getCalcMethod(), self.getAsrMethod(), self.getLocation().getDescription(), self.getLocation().getLatitude(), self.getLocation().getLongitude())
        self.prayerToday.putPrayerTimes()
        self.prayerTomorrow = PrayerTime(self.tomorrowDate.month, self.tomorrowDate.day, self.tomorrowDate.year, self.getUTCOffset(), self.getCalcMethod(), self.getAsrMethod(), self.getLocation().getDescription(), self.getLocation().getLatitude(), self.getLocation().getLongitude())
        self.prayerTomorrow.putPrayerTimes()


    def exportConfigToFile(self):
        self.config.data["general"]["timezone_utc_offset"] = self.getUTCOffset()
        #offset, name = get_offset_name(lat=34.1434, lng=-111.1230)
        self.config.data["general"]["timezone_description"] = self.getTzDesc()

        self.config.data["prayer_times"]["method_name"] = self.getCalcMethod().name
        self.config.data["prayer_times"]["fajr_offset"] = float(self.getCalcMethod().fajr_angle)
        self.config.data["prayer_times"]["isha_offset"] = float(self.getCalcMethod().isha_angle)
        self.config.data["prayer_times"]["maghrib_to_isha_90"] = self.getCalcMethod().fixed
        self.config.data["prayer_times"]["asr_method"] = self.getAsrMethod()

        self.config.data["location"]["latitude"] = self.getLocation().getLatitude()
        #print("latitude", self.getLocation().getLatitude())
        self.config.data["location"]["longitude"] = self.getLocation().getLongitude()
        self.config.data["location"]["region_description"] = self.getLocation().getDescription()

        self.config.save()
        #print("saving config to file...")


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
