import math
from datetime import datetime, timezone
from typing import Dict
from urllib.request import urlopen
import time
#import argparse
import json
from CalcMethods import CalcMethod, methods
#import re
#import ssl
#import certifi
#from geopy.geocoders import Nominatim

# global variable
debug = False

def main():
    import argparse
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
    prayerTime.putPrayerTimes()
    print(prayerTime)

def getDefaultConfig(latitude: float, longitude: float) -> Dict:
    month = datetime.now().month
    day = datetime.now().day
    year = datetime.now().year
    utc_offset = getLocalUTCOffset(time.time())
    asr_method = 1
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
    location = Location()
    if getYesNo("\nMa'ruf requires GPS latitude and longitude coordinates in order to calculate prayer times\nWould you like to use an approximation of your GPS coordinates based on your public IPv4 address? (requires an active internet connection)"):
        location .setLocationByIP()
        #latitude, longitude, description = getLocationByIP()
    elif getYesNo("\nWould you like to use an approximation based on a given city? (requires an active internet connection, uses Nominatim API)"):
        user_query = ""
        query_string = ""
        while True:
            try:
                user_query = str(input(("Enter your city/country (format: New York, USA), limit to 40 alphanumeric characters (Aa-Zz, 0-9): ")))
                #query_string = Location.processQuery(user_query)
                query_string = processQuery(user_query)
            except ValueError as e:
                dPrint(e)
                continue
            break
        #latitude, longitude, description = getLocationByQuery(query_string)
        location.setLocationByQuery(query_string)
    else:
        try:
            latitude = float(input("Enter your latitude coordinate (format: 12.34): ").strip())
            latitude = "{:.2f}".format(latitude)
            longitude = float(input("Enter your longitude coordinate (format: 12.34): ").strip())
            longitude = "{:.2f}".format(longitude)
            location.setLocationManually(latitude, longitude)
            description = "Custom"
        except ValueError:
            dPrint("Please enter a number in the given format")
    #dPrint(f"({latitude}, {longitude}) {description} set")
    dPrint(f"({location.getLatitude()}, {location.getLongitude()}, {location.getDescription()})")
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

    return dict(latitude=location.getLatitude(), longitude=location.getLongitude(), description=location.getDescription(), calc_method=CalcMethod, asr_method=ASR_METHOD, month=month, day=day, year=year, utc_offset=utc_offset)


def getYesNo(question: str) -> bool:
    while True:
        response = str(input(f"{question} (y/n) ")).strip().lower()
        if response in ('y', "yes"):
            return True
        elif response in ('n', "no"):
            return False
        else:
            dPrint("Please answer with 'yes' or 'no'")

    
def promptCalcMethod() -> CalcMethod:
    CALCULATION_METHOD = None
    count = 0
    keys = list(methods.keys())
    print("")
    for i, key in enumerate(keys, 1):
        print(f"{i}. {key} (Fajr: {methods[key].fajr_angle} Isha: {methods[key].isha_angle})")
    answer = int(input("\nChoose your calculation method: ").strip())

    # ensure index is valid
    index = int(answer) - 1
    while CALCULATION_METHOD is None:
        try:
            if 0 <= index < len(keys):
                selected_key = keys[index]
                CALCULATION_METHOD = methods[selected_key]
                print(f"You chose: {selected_key} with value {methods[selected_key]}")
            else:
                print("Invalid choice. Number out of range")
        except ValueError:
            print("Invalid input. Please enter a number.")

    return CALCULATION_METHOD


def getLocalUTCOffset(time) -> float:
    return ((datetime.fromtimestamp(time).timestamp()) - datetime.fromtimestamp(time, timezone.utc).replace(tzinfo=None).timestamp())/3600.0

class Location:
    def __init__(self, latitude=0.0, longitude=0.0, description="Custom"):
        self.latitude = latitude
        self.longitude = longitude
        self.description = description
        self.__ssl_context = None

    def __str__(self):
        return(f"({self.latitude}, {self.longitude})")
    def getLatitude(self):
        return self.latitude
    def getLongitude(self):
        return self.longitude
    def getDescription(self):
        return self.description

    def setLocationByIP(self):
        #import ssl
        #import certifi
        #self.__ssl_context = ssl.create_default_context(cafile=certifi.where())
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
        #print(self.description)
    
    def setLocationByQuery(self, query: str):
        import ssl
        import certifi
        from geopy.geocoders import Nominatim

        self.__ssl_context = ssl.create_default_context(cafile=certifi.where())

        geolocator = Nominatim(user_agent='maruf', ssl_context=self.__ssl_context)
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
    import re
    query = query.strip()
    if not re.match(r"^^[A-Za-z0-9\s.'\-&,]+$", query):
        raise ValueError("Error! Only non-empty alphanumeric characters allowed.")
    elif len(query) > 40:
        raise ValueError("Error! Input larger than 40 characters.")
    return query


#class CalcMethod:
#    def __init__(self, name="MWL", fajr_angle=18.0, isha_angle=17.0, fixed=False):
#        self.name = name
#        self.fajr_angle = fajr_angle
#        self.isha_angle = isha_angle
#        self.fixed = fixed
#
#    def __str__(self):
#        return (self.name)

class PrayerTime:
    #from geopy.geocoders import Nominatim
    ASR_METHOD: int = 1
    #CalcMethod = namedtuple("CalcMethod", ["name", "fajr_angle", "isha_angle", "fixed"])
    #__ts = time.time()
    #__month = 0
    #__day = 0
    #__year = 0
    #__utc_offset = 0.0
    #__geolocator = Nominatim(user_agent='maruf')
    #__daysDecimal = 0.0
    #__latitude = None
    #__longitude = None
    #__description = ""
    #CALCULATION_METHOD = CalcMethod()


    fajr_time=datetime.min
    sunrise_time=datetime.min
    dhuhr_time=datetime.min
    asr_time=datetime.min
    maghrib_time=datetime.min
    isha_time=datetime.min

    #def __init__(self, month=datetime.now().date().month, day=datetime.now().date().day, year=datetime.now().date().year, utc_offset=getLocalUTCOffset(time.time()), calc_method=CalcMethod(), asr_method=1, loc_desc="", latitude=34.5, longitude=-111.0):
    def __init__(self, month: int, day: int, year: int, utc_offset: float, calc_method: CalcMethod, asr_method: int, loc_desc: str, latitude: float, longitude: float):
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
        self.prayerTimes = dict()
        #self.prayerTimes = self.__calcPrayerTimes()
    
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

    def __calcSunAltitudes(self, calcMethod: CalcMethod, elevation: int, asr_method: int, sunDelta: float, latitude: float) -> dict:
        fajr_angle = calcMethod.fajr_angle
        isha_angle = calcMethod.isha_angle

        SA_FAJR = -(fajr_angle)
        SA_MAGHRIB = -0.8333 - (0.0347 * math.sqrt(elevation))
        SA_SUNRISE = SA_MAGHRIB
        #SA_ASR = math.degrees(math.pow((1/math.tan(math.radians(asr_method + math.tan(math.radians(abs(sunDelta - latitude)))))), -1))
        SA_ASR = math.atan(1/(self.ASR_METHOD+math.tan(math.radians(abs(sunDelta - latitude)))))
        SA_ISHA = -(isha_angle) if calcMethod.fixed == False else None
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
        cos_HA_ISHA = (math.sin(math.radians(sunAltitudes["isha"])) - math.sin(math.radians(latitude)) * math.sin(math.radians(sunDelta))) / (math.cos(math.radians(latitude)) * math.cos(math.radians(sunDelta))) if sunAltitudes["isha"] is not None else None

        HA_FAJR = math.degrees(math.acos(cos_HA_FAJR))
        HA_MAGHRIB = math.degrees(math.acos(cos_HA_MAGHRIB))
        HA_ASR = math.degrees(math.acos(cos_HA_ASR))
        HA_SUNRISE = HA_MAGHRIB
        HA_ISHA = math.degrees(math.acos(cos_HA_ISHA)) if cos_HA_ISHA is not None else None

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
    def __calcAsrDiff(self, jd, Lat, asrMethod) -> float:
        d = jd-2451545.0

        g = 357.529 + 0.98560028* d
        q = 280.459 + 0.98564736* d
        L = q + 1.915* math.sin(math.radians(g)) + 0.020* math.sin(math.radians(2*g))
        
        e = 23.439 - 0.00000036* d
        
        D = math.degrees(math.asin(math.sin(math.radians(e))* math.sin(math.radians(L))))  # declination of the Sun
        dPrint(f"Declination of the Sun: {D}")
        
        #top = math.sin(math.radians(math.degrees(self.arccot(asrMethod+math.tan(math.radians(Lat-D))))-math.degrees((math.sin(math.radians(Lat)))*math.sin(math.radians(D)))))
        #bottom = math.cos(math.radians(Lat))*math.cos(math.radians(D))
        #asr_del = (1/15)*(math.degrees(math.acos(top/bottom)))
                # Asr shadow length formula
        angle = math.degrees(self.arccot(asrMethod + math.tan(abs(math.radians(Lat - D)))))
        #print("asr angle: ", angle)

        # Compute hour angle
        numerator = math.sin(math.radians(angle)) - math.sin(math.radians(Lat)) * math.sin(math.radians(D))
        denominator = math.cos(math.radians(Lat)) * math.cos(math.radians(D))
        hour_angle = math.acos(numerator / denominator)
        #print("hour_angle_asr: ", hour_angle)

        # Convert to time (1 hour = 15 degrees)
        asr_diff_hours = math.degrees(hour_angle) / 15.0
        return asr_diff_hours
    
    def putPrayerTimes(self) -> None:
        self.prayerTimes = self.calcPrayerTimes()

    # returns dict with prayertimes as datetime objects
    def calcPrayerTimes(self) -> dict:
        JD = self.__calcJD(self.__year, self.__month, self.__daysDecimal)
        T, DELTA = self.__calcSunDeclination(JD)
        ET = self.__calcEqTime(JD)
        TT = self.__calcSunTransitTime(self.__utc_offset, self.__longitude, ET)
        sunAltitudes = self.__calcSunAltitudes(self.CALCULATION_METHOD, 0, self.ASR_METHOD, DELTA, self.__latitude)
        hourAngles = self.__calcHourAngles(sunAltitudes, self.__latitude, DELTA)
        
        #asr_time = noon + timedelta(minutes_after_noon)

        # compute asr

        FAJR = TT - (hourAngles["fajr"] / 15)
        SUNRISE = TT - hourAngles["sunrise"] / 15
        DHUHR = TT + 2/60
        # ASR = TT + hourAngles["asr"] / 15
        ASR = DHUHR + self.__calcAsrDiff(JD, self.__latitude, self.ASR_METHOD)
        MAGHRIB = TT + (hourAngles["maghrib"] / 15)
        ISHA = (TT + hourAngles["isha"] / 15) if sunAltitudes["isha"] is not None else MAGHRIB + 1.5
        
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
        retStr = ""
        for k, v in self.prayerTimes.items():
            retStr += f"\n{k}: {v}"
        return retStr

        #f"FAJR: {self.prayerTimes.get("fajr").strftime("%I:%M:%S %p")}"
        #        f"\nSUNRISE: {self.prayerTimes.get("sunrise").strftime("%I:%M:%S %p")}"
        #        f"\nDHUHR: {self.prayerTimes.get("dhuhr").strftime("%I:%M:%S %p")}"
        #        f"\nASR: {self.prayerTimes.get("asr").strftime("%I:%M:%S %p")}"
        #f"\nMAGHRIB: {self.prayerTimes.get("maghrib").strftime("%I:%M:%S %p")}"
        #        f"\nISHA: {self.prayerTimes.get("isha").strftime("%I:%M:%S %p")}"
        

    #def __str__(self):
    #    return(
    #    f"FAJR: {self.fajr_time.strftime("%I:%M:%S %p")}"
    #    f"\nSUNRISE: {self.sunrise_time.strftime("%I:%M:%S %p")}"
    #    f"\nDHUHR: {self.dhuhr_time.strftime("%I:%M:%S %p")}"
    #    f"\nASR: {self.asr_time.strftime("%I:%M:%S %p")}"
    #    f"\nMAGHRIB: {self.maghrib_time.strftime("%I:%M:%S %p")}"
    #    f"\nISHA: {self.isha_time.strftime("%I:%M:%S %p")}"
    #    )

    
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
