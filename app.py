import math
from datetime import datetime, timezone
from typing import Dict, Optional
from urllib.request import urlopen
import time
import argparse
import json
import re
from geopy.geocoders import Nominatim

# global variable
debug = False

def main():
    parser = argparse.ArgumentParser(
        prog="Ma'ruf",
        description='Calculates islamic prayer times using on-device calculations exclusively',
        epilog='Visit <https://github.com/SheptheSheep1/prayer_times_app> for more info and documentation.'
    )
    parser.add_argument('-b', '--headless', action='store_true') #run with no other user interaction
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-lat', '--latitude', help='input latitude coordinate')
    parser.add_argument('-lng', '--longitude', help='input longitude coordinate')
    args = parser.parse_args()
    dPrint(args)
    if args.verbose is True:
        global debug 
        debug = True
    # dPrint(os.environ['LATITUDE'])
    dPrint("\n-------------------------------------")
    dPrint("-------------------------------------")
    dPrint("----------Welcome to Ma'ruf----------")
    dPrint("-------------------------------------")
    dPrint("-------------------------------------\n")
    doct = dict()
    if args.headless is False or args.headless is None:
        doct = userInteraction()
    elif args.latitude is not None and args.longitude is not None:
        dPrint("default")
        doct = getDefaultConfig(float(args.latitude), float(args.longitude))
    else:
        print("Must provide latitude(-lat) and longitude(-lng). exiting...")
        exit()
    prayerTime = PrayerTime(doct["month"], doct["day"], doct["year"], doct["utc_offset"], doct["calc_method"], doct["asr_method"], doct["description"], doct["latitude"], doct["longitude"])
    print(prayerTime)

def getDefaultConfig(latitude: float, longitude: float) -> Dict:
    month = datetime.now().month
    day = datetime.now().day
    year = datetime.now().year
    utc_offset = getLocalUTCOffset(time.time())
    asr_method = 2
    description = "Custom"
    latitude = latitude
    longitude = longitude
    return dict(latitude=latitude, longitude=longitude, description=description, calc_method=CalcMethod(), asr_method=asr_method, month=month, day=day, year=year, utc_offset=utc_offset)


def userInteraction() -> Dict:
    latitude = None
    longitude = None
    description = ""
    location = Location()

# date/time
    if getYesNo("Would you like to use your system date/time?"):
        month = datetime.now().date().month
        day = datetime.now().date().day
        year = datetime.now().date().year
        utc_offset = getLocalUTCOffset(time.time())
    else:
        year = int(input("Enter the gregorian year in AD (format: '2024'): ").strip())
        month = int(input("Enter the gregorian month (format: '01'): ").strip())
        day = int(input("Enter the day of the month (format: '09'): ").strip())
        utc_offset = float(input("Enter your timezone's offset from UTC (format: '11.5'): ").strip())

    # location
    if getYesNo("\nMa'ruf requires GPS latitude and longitude coordinates in order to calculate prayer times\nWould you like to use an approximation of your GPS coordinates based on your public IPv4 address? (requires an active internet connection)"):

        latitude, longitude, description = getLocationByIP()
    elif getYesNo("\nWould you like to use an approximation based on a given city? (requires an active internet connection, uses Nominatim API)"):
        user_query = ""
        query_string = ""
        while True:
            try:
                user_query = str(input(("Enter your city/country (format: New York, USA), limit to 40 alphanumeric characters (Aa-Zz, 0-9): ")))
                query_string = Location.processQuery(user_query)
            except ValueError as e:
                dPrint(e)
                continue
            break
        latitude, longitude, description = getLocationByQuery(query_string)
    else:
        try:
            latitude = float(input("Enter your latitude coordinate (format: 12.34): ").strip())
            latitude = "{:.2f}".format(latitude)
            longitude = float(input("Enter your longitude coordinate (format: 12.34): ").strip())
            longitude = "{:.2f}".format(longitude)
            description = "Custom"
        except ValueError:
            dPrint("Please enter a number in the given format")
    
    dPrint(f"({latitude}, {longitude}) {description} set")
    # calc method
    CalcMethod = promptCalcMethod()
    if getYesNo("Would you like to use the Hanafi asr calculation method (2x Shadow Length)?"):
        ASR_METHOD = 2
    else: ASR_METHOD = 1
    method = ""
    if (ASR_METHOD == 1):
        method = "1 Shadow Length (Shafi'i, Maliki, Hanbali)"
    elif (ASR_METHOD == 2):
        method = "2 Shadow Length (Hanafi)"
        dPrint(f"Asr juristic method set to: {method}\n")
        dPrint("Calculating prayer times...\n")

    return dict(latitude=latitude, longitude=longitude, description=description, calc_method=CalcMethod, asr_method=ASR_METHOD, month=month, day=day, year=year, utc_offset=utc_offset)


def getYesNo(question: str) -> bool:
    while True:
        response = str(input(f"{question} (y/n) ")).strip().lower()
        if response in ('y', "yes"):
            return True
        elif response in ('n', "no"):
            return False
        else:
            dPrint("Please answer with 'yes' or 'no'")

    
def promptCalcMethod():
    dPrint(f'''
              (1) MWL (Muslim World League) Fajr: 18\N{DEGREE SIGN} Isha: 17\N{DEGREE SIGN}
              (2) ISNA (Islamic Society of North America) Fajr: 15\N{DEGREE SIGN} Isha: 15\N{DEGREE SIGN}
              (3) Umm al-Qura (Umm al-Qura University, Makkah) Fajr: 18.5\N{DEGREE SIGN} Isha: 90 mins after Maghrib, 120 mins during Ramadan
              (4) Gulf Fajr: 19.5\N{DEGREE SIGN} Isha: 90 mins after Maghrib, 120 mins during Ramadan
              (5) Algerian (Algerian Ministry of Religious Affairs and Wakfs) Fajr: 18\N{DEGREE SIGN} Isha: 17\N{DEGREE SIGN}
              (6) Karachi (University of Islamic Sciences, Karachi) Fajr: 18\N{DEGREE SIGN} Isha: 18\N{DEGREE SIGN}
              (7) Diyanet (Diyanet İşleri Başkanlığı, Turkey) Fajr: 18\N{DEGREE SIGN} Isha: 17\N{DEGREE SIGN}
              (8) Egypt (Egyptian General Authority of Survey) Fajr: 19.5\N{DEGREE SIGN} Isha: 17.5\N{DEGREE SIGN}
              (9) EgyptBis (Egyptian General Authority of Survey) Fajr: 20\N{DEGREE SIGN} Isha: 18\N{DEGREE SIGN}
              (10) Kemenag (Kementerian Agama Republik Indonesia) Fajr: 20\N{DEGREE SIGN} Isha: 18\N{DEGREE SIGN}
              (11) MUIS (Majlis Ugama Islam Singapura) Fajr: 20\N{DEGREE SIGN} Isha: 18\N{DEGREE SIGN}
              (12) JAKIM (Jabatan Kemajuan Islam Malaysia) Fajr: 20\N{DEGREE SIGN} Isha: 18\N{DEGREE SIGN}
              (13) UDIF (Union Des Organisations Islamiques De France) Fajr: 12\N{DEGREE SIGN} Isha: 12\N{DEGREE SIGN}
              (14) France15 Fajr: 15\N{DEGREE SIGN} Isha: 15\N{DEGREE SIGN}
              (15) France18 Fajr: 18\N{DEGREE SIGN} Isha: 18\N{DEGREE SIGN}
              (16) Tunisia (Tunisian Ministry of Religious Affairs) Fajr: 18\N{DEGREE SIGN} Isha: 18\N{DEGREE SIGN}
              (17) Tehran (Institute of Geophysics, University of Tehran) Fajr: 17.7\N{DEGREE SIGN} Isha: 14\N{DEGREE SIGN}
              (18) Jafari (Shia Ithna Ashari) Fajr: 16\N{DEGREE SIGN} Isha: 14\N{DEGREE SIGN}
              ''')
    answer = int(input("\nChoose your calculation method: ").strip())
    # records calculation method as namedtuple 'CalcMethod' in order to maintain actual name of method as opposed just angles (DEPRECATED)
    match answer:
        case 1:
            CALCULATION_METHOD = CalcMethod("MWL", 18.0, 17.0, False)
        case 2:
            CALCULATION_METHOD = CalcMethod("ISNA", 15.0, 15.0, False)
        case 3:
            CALCULATION_METHOD = CalcMethod("Umm al-Qura", 18.5, 90, True)
        case 4:
            CALCULATION_METHOD = CalcMethod("Gulf", 19.5, 90, True)
        case 5:
            CALCULATION_METHOD = CalcMethod("Algerian", 18.0, 17.0, False)
        case 6:
            CALCULATION_METHOD = CalcMethod("Karachi", 18.0, 18.0, False)
        case 7:
            CALCULATION_METHOD = CalcMethod("Diyanet", 18.0, 17.0, False)
        case 8:
            CALCULATION_METHOD = CalcMethod("Egypt", 19.5, 17.5, False)
        case 9:
            CALCULATION_METHOD = CalcMethod("EgyptBis", 20.0, 18.0, False)
        case 10:
            CALCULATION_METHOD = CalcMethod("Kemenag", 20.0, 18.0, False)
        case 11:
            CALCULATION_METHOD = CalcMethod("MUIS", 20.0, 18.0, False)
        case 12: 
            CALCULATION_METHOD = CalcMethod("JAKIM", 20.0, 18.0, False)
        case 13:
            CALCULATION_METHOD = CalcMethod("UDIF", 12.0, 12.0, False)
        case 14:
            CALCULATION_METHOD = CalcMethod("France15", 15.0, 15.0, False)
        case 15:
            CALCULATION_METHOD = CalcMethod("France18", 18.0, 18.0, False)
        case 16:
            CALCULATION_METHOD = CalcMethod("Tunisia", 18.0, 18.0, False)
        case 17:
            CALCULATION_METHOD = CalcMethod("Tehran", 17.7, 14.0, False)
        case 18:
            CALCULATION_METHOD = CalcMethod("Jafari", 16.0, 14.0, False)
        case _:
            CALCULATION_METHOD = CalcMethod("booh", 18.0, 17.0, False)
    return CALCULATION_METHOD
    dPrint(f"{CALCULATION_METHOD.name} chosen\n")

def getLocalUTCOffset(time) -> float:
    return ((datetime.fromtimestamp(time).timestamp()) - datetime.fromtimestamp(time, timezone.utc).replace(tzinfo=None).timestamp())/3600.0

class Location:
    def __init__(self, latitude=0.0, longitude=0.0, description=""):
        self.latitude = latitude
        self.longitude = longitude
        self.description = description

    def __str__(self):
        return(f"({self.latitude}, {self.longitude})")
    def getLatitude(self):
        return self.latitude
    def getLongitude(self):
        return self.longitude
    def getDescription(self):
        return self.description

    def setLocationByIP(self):
        url = "http://ip-api.com/json/"
        try:
            with urlopen(url) as response:
                body = response.read()
        except Exception as e:
            raise e
        responseDict = json.loads(body)
        latitude = responseDict["lat"]
        longitude = responseDict["lon"]
        desc = "".join([responseDict["city"],","," ",responseDict["region"]])
        #return (latitude, longitude, desc)
        self.latitude = latitude
        self.longitude = longitude
        self.description = desc
        print(self.description)
    
    def setLocationByQuery(self, query: str):
        geolocator = Nominatim(user_agent='maruf')
        # TODO: Actual exception handling
        location = geolocator.geocode(query)
        if location is None:
            print("location is NoneType")
        #return (location.latitude, location.longitude, location.address)
        self.latitude = location.latitude
        self.longitude = location.longitude
        self.description = location.address

    def setLocationManually(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.description = "Custom Location"
    
def processQuery(query: str) -> str:
    query = query.strip()
    if not re.match(r"^^[A-Za-z0-9\s.'\-&,]+$", query):
        raise ValueError("Error! Only non-empty alphanumeric characters allowed.")
    elif len(query) > 40:
        raise ValueError("Error! Input larger than 40 characters.")
    return query


class CalcMethod:
    def __init__(self, name="MWL", fajr_angle=18.0, isha_angle=17.0, fixed=False):
        self.name = name
        self.fajr_angle = fajr_angle
        self.isha_angle = isha_angle
        self.fixed = fixed

    def __str__(self):
        return (self.name)

class PrayerTime:
    ASR_METHOD: int = 1
    #CalcMethod = namedtuple("CalcMethod", ["name", "fajr_angle", "isha_angle", "fixed"])
    __ts = time.time()
    __month = 0
    __day = 0
    __year = 0
    __utc_offset = 0.0
    __geolocator = Nominatim(user_agent='maruf')
    __daysDecimal = 0.0
    __latitude = None
    __longitude = None
    __description = ""
    CALCULATION_METHOD = CalcMethod()

    prayerTimes = dict()

    fajr_time=datetime.min
    sunrise_time=datetime.min
    dhuhr_time=datetime.min
    asr_time=datetime.min
    maghrib_time=datetime.min
    isha_time=datetime.min

    def __init__(self, month=datetime.now().date().month, day=datetime.now().date().day, year=datetime.now().date().year, utc_offset=getLocalUTCOffset(time.time()), calc_method=CalcMethod(), asr_method=1, loc_desc="", latitude=34.0, longitude=-111.0):
        self.__month = month
        self.__day = day
        self.__year = year
        self.__utc_offset = utc_offset
        self.__daysDecimal = day + 0.5
        self.CALCULATION_METHOD = calc_method
        self.ASR_METHOD = asr_method
        self.__description = loc_desc
        self.__latitude = latitude
        self.__longitude = longitude
        self.prayerTimes = self.__calcPrayerTimes()
    
    def setGPScoordinates(self, latitude: float, longitude: float):
        self.__latitude = latitude
        self.__longitude = longitude
    
    def setLocation(self, latitude: float, longitude: float, description: str):
        self.__latitude = latitude
        self.__longitude = longitude
        self.__description = description

    def setCalcMethod(self, calcMethod):
        self.CALCULATION_METHOD = calcMethod

    # calculates Julian days in decimal from a given gregorian date
    def __calcJD(self, year, month, day) -> float:
        # shameless copy&p...
        """
        Convert a date to Julian Day.
        
        Algorithm from 'Practical Astronomy with your Calculator or Spreadsheet', 
            4th ed., Duffet-Smith and Zwart, 2011.
        
        Parameters
        ----------
        year : int
            Year as integer. Years preceding 1 A.D. should be 0 or negative.
            The year before 1 A.D. is 0, 10 B.C. is year -9.
            
        month : int
            Month as integer, Jan = 1, Feb. = 2, etc.
        
        day : float
            Day, may contain fractional part.
        
        Returns
        -------
        jd : float
            Julian Day
            
        Examples
        --------
        Convert 6 a.m., February 17, 1985 to Julian Day
        
        date_to_jd(1985,2,17.25)
        2446113.75
        
        """
        if month == 1 or month == 2:
            yearp = year - 1
            monthp = month + 12
        else:
            yearp = year
            monthp = month
        
        # this checks where we are in relation to October 15, 1582, the beginning
        # of the Gregorian calendar.
        if ((year < 1582) or
            (year == 1582 and month < 10) or
            (year == 1582 and month == 10 and day < 15)):
            # before start of Gregorian calendar
            B = 0
        else:
            # after start of Gregorian calendar
            A = math.trunc(yearp / 100.)
            B = 2 - A + math.trunc(A / 4.)
            
        if yearp < 0:
            C = math.trunc((365.25 * yearp) - 0.75)
        else:
            C = math.trunc(365.25 * yearp)
            
        D = math.trunc(30.6001 * (monthp + 1))
        
        jd = B + C + D + day + 1720994.5
        
        return jd
    
    def __calcSunDeclination(self, JD: float) -> tuple:
        T = (2 * math.pi * (JD - 2451545)) / 365.25
        DELTA = 0.37877 + (23.264 * math.sin(math.radians((57.297*T) - 79.547))) + (0.3812 * math.sin(math.radians((2*57.297*T) - 82.682))) + (0.17132 * math.sin(math.radians((3*57.297*T) - 59.722)))
        return (T, DELTA)

    def __calcEqTime(self, JD: float) -> float:
        U = (JD - 2451545) / 36525
        L0 = 280.46607 + 36000.7698*U
        ET1000 = -(1789 + 237*U) * math.sin(math.radians(L0)) - (7146 - 62*U) * math.cos(math.radians(L0)) + (9934 - 14*U) * math.sin(math.radians(2*L0)) - (29 + 5*U) * math.cos(math.radians(2*L0)) + (74 + 10*U) * math.sin(math.radians(3*L0)) + (320 - 4*U) * math.cos(math.radians(3*L0)) - 212*math.sin(math.radians(4*L0))
        ET = ET1000 / 1000
        dPrint(f"\nU: {U}\nL0:{L0}\nET1000:{ET1000}\n")
        dPrint(f"Equation of Time: {ET} minutes")
        return ET

    def __calcSunTransitTime(self, utc_offset: float, longitude: float, eqTime: float) -> float:
        # calculates sun transit time
        TT = 12.0 + utc_offset - (longitude / 15.0) - (eqTime / 60.0)
        dPrint(f"Sun Transit Time: {TT} hours")
        return TT

    def __calcSunAltitudes(self, fajr_angle: float, isha_angle: float, elevation: int, asr_method: int, sunDelta: float, latitude: float) -> dict:
        SA_FAJR = -(fajr_angle)
        SA_MAGHRIB = -0.8333 - (0.0347 * math.sqrt(elevation))
        SA_SUNRISE = SA_MAGHRIB
        #SA_ASR = math.degrees(math.pow((1/math.tan(math.radians(asr_method + math.tan(math.radians(abs(sunDelta - latitude)))))), -1))
        SA_ASR = math.atan(1/(self.ASR_METHOD+math.tan(math.radians(abs(sunDelta - latitude)))))
        SA_ISHA = -(isha_angle)
        sunAltitudes = dict(
                fajr = SA_FAJR,
                sunrise = SA_SUNRISE,
                asr = SA_ASR,
                maghrib = SA_MAGHRIB,
                isha = SA_ISHA
                )
        dPrint(f"Sun Altitudes: {sunAltitudes}")
        return sunAltitudes

    def __calcHourAngles(self, sunAltitudes: dict, latitude: float, sunDelta: float) -> dict:
        cos_HA_FAJR = (math.sin(math.radians(sunAltitudes["fajr"])) - math.sin(math.radians(latitude)) * math.sin(math.radians(sunDelta))) / (math.cos(math.radians(latitude)) * math.cos(math.radians(sunDelta)))
        cos_HA_ASR = (math.sin(math.radians(sunAltitudes["asr"])) - math.sin(math.radians(latitude)) * math.sin(math.radians(sunDelta))) / (math.cos(math.radians(latitude)) * math.cos(math.radians(sunDelta)))
        cos_HA_MAGHRIB = (math.sin(math.radians(sunAltitudes["sunrise"]))) - math.sin(math.radians(latitude)) * math.sin(math.radians(sunDelta)) / (math.cos(math.radians(latitude)) * math.cos(math.radians(sunDelta)))
        cos_HA_SUNRISE = cos_HA_MAGHRIB
        cos_HA_ISHA = (math.sin(math.radians(sunAltitudes["isha"])) - math.sin(math.radians(latitude)) * math.sin(math.radians(sunDelta))) / (math.cos(math.radians(latitude)) * math.cos(math.radians(sunDelta)))

        HA_FAJR = math.degrees(math.acos(cos_HA_FAJR))
        HA_MAGHRIB = math.degrees(math.acos(cos_HA_MAGHRIB))
        HA_ASR = math.degrees(math.acos(cos_HA_ASR))
        HA_SUNRISE = HA_MAGHRIB
        HA_ISHA = math.degrees(math.acos(cos_HA_ISHA))

        hourAngles = dict(
                fajr= HA_FAJR,
                sunrise= HA_SUNRISE,
                asr= HA_ASR,
                maghrib= HA_MAGHRIB,
                isha= HA_ISHA
                )
        dPrint(f"Hour Angles: {hourAngles}")

        return hourAngles
    
    # params: jd: julian days, Lat: latitude, returns a double representing decimal hours after solar zenith for asr
    def __calcAsrDiff(self, jd, Lat) -> float:
        d = jd-2451545.0

        g = 357.529 + 0.98560028* d
        q = 280.459 + 0.98564736* d
        L = q + 1.915* math.sin(math.radians(g)) + 0.020* math.sin(math.radians(2*g))
        
        e = 23.439 - 0.00000036* d
        
        D = math.degrees(math.asin(math.sin(math.radians(e))* math.sin(math.radians(L))))  # declination of the Sun
        dPrint(f"Declination of the Sun: {D}")
        
        top = math.sin(math.radians(math.degrees(self.arccot(2+math.tan(math.radians(Lat-D))))-math.degrees((math.sin(math.radians(Lat)))*math.sin(math.radians(D)))))
        bottom = math.cos(math.radians(Lat))*math.cos(math.radians(D))
        asr_del = (1/15)*(math.degrees(math.acos(top/bottom)))
        return asr_del
    
    # returns dict with prayertimes as datetime objects
    def __calcPrayerTimes(self) -> dict:
        JD = self.__calcJD(self.__year, self.__month, self.__daysDecimal)
        T, DELTA = self.__calcSunDeclination(JD)
        ET = self.__calcEqTime(JD)
        TT = self.__calcSunTransitTime(self.__utc_offset, self.__longitude, ET)
        sunAltitudes = self.__calcSunAltitudes(self.CALCULATION_METHOD.fajr_angle, self.CALCULATION_METHOD.isha_angle, 0, self.ASR_METHOD, DELTA, self.__latitude)
        hourAngles = self.__calcHourAngles(sunAltitudes, self.__latitude, DELTA)
        
        #asr_time = noon + timedelta(minutes_after_noon)

        # compute asr

        FAJR = TT - (hourAngles["fajr"] / 15)
        SUNRISE = TT - hourAngles["sunrise"] / 15
        DHUHR = TT + 2/60
        # ASR = TT + hourAngles["asr"] / 15
        ASR = DHUHR + self.__calcAsrDiff(JD, self.__latitude)
        MAGHRIB = TT + (hourAngles["maghrib"] / 15)
        ISHA = TT + hourAngles["isha"] / 15
        
        dPrint(FAJR)
        prayerTimes = dict (
                fajr= self.convertHrs(FAJR),
                sunrise= self.convertHrs(SUNRISE),
                dhuhr= self.convertHrs(DHUHR),
                asr= self.convertHrs(ASR),
                maghrib= self.convertHrs(MAGHRIB),
                isha= self.convertHrs(ISHA)
                )
        self.fajr_time = prayerTimes["fajr"]
        self.sunrise_time = prayerTimes["sunrise"]
        self.dhuhr_time = prayerTimes["dhuhr"]
        self.asr_time = prayerTimes["asr"]
        self.maghrib_time = prayerTimes["maghrib"]
        self.isha_time = prayerTimes["isha"]

        return prayerTimes


    def __str__(self):
        return(
        f"FAJR: {self.fajr_time.strftime("%I:%M:%S %p")}"
        f"\nSUNRISE: {self.sunrise_time.strftime("%I:%M:%S %p")}"
        f"\nDHUHR: {self.dhuhr_time.strftime("%I:%M:%S %p")}"
        f"\nASR: {self.asr_time.strftime("%I:%M:%S %p")}"
        f"\nMAGHRIB: {self.maghrib_time.strftime("%I:%M:%S %p")}"
        f"\nISHA: {self.isha_time.strftime("%I:%M:%S %p")}"
        )

    
    def convertHrs(self, decimal) -> datetime:
        # convert a number of hours in decimal to a datetime object
        dPrint(f"decimal: {decimal}")
        # case: negative hours
        if decimal < 0:
            decimal += 24
        hours = int(decimal)
        minutes = int((decimal - hours) * 60)
        seconds = int((((decimal - hours) * 60) - minutes) * 60)

        dPrint(
            f"\nhours: {hours}"
            f"\nminutes: {minutes}"
            f"\nsecond: {seconds}"
        )
        time = datetime(self.__year, self.__month, self.__day, hours, minutes, seconds)
        #return time.strftime("%H:%M:%S
        return time
    
    def getPrayertimes(self) -> dict:
        return self.prayerTimes

    def getGPSCoordinates(self) -> tuple:
        return self.__latitude, self.__longitude
    
    def darccot(self, x: float) -> float:
        return self.rtd(math.atan(1/x))

    def rtd(self, radians: float) -> float:
        return (radians * 180.0) / math.pi
    
    def dtr(self, degrees: float) -> float:
        return (degrees * math.pi) / 180.0

    def dtan(self, d: float) -> float:
        return math.tan(self.dtr(d))

    def dsin(self, d: float) -> float:
        return math.sin(self.dtr(d))

    def dcos(self, d: float) -> float:
        return math.cos(self.dtr(d))

    def darccos(self, x: float) -> float:
        return self.rtd(math.acos(x))

    def arccot(self, x):
        return math.pi / 2 - math.atan(x) 

def dPrint(input):
    if debug is True:
        print(input)

if __name__ == "__main__":
    main()
