import math
import os
import time
from datetime import datetime, timezone
from collections import namedtuple

from geopy.geocoders import Nominatim

def main():
    # print(os.environ['LATITUDE'])
    print("\n-------------------------------------")
    print("-------------------------------------")
    print("----------Welcome to Ma'ruf----------")
    print("-------------------------------------")
    print("-------------------------------------\n")
    if getYesNo("Would you like to use your system date and time?"):
        prayerTime = PrayerTime()
    else:
        year = int(input("Enter the gregorian year in AD (format: '2024'): ").strip())
        month = int(input("Enter the gregorian month (format: '01'): ").strip())
        day = int(input("Enter the day of the month (format: '09'): ").strip())
        utc_timezone = float(input("Enter your timezone's offset from UTC (format: '11.5'): ").strip())
        prayerTime = PrayerTime(month, day, year, utc_timezone)
    if getYesNo("\nMa'ruf requires GPS latitude and longitude coordinates in order to calculate prayer times\nWould you like to use an approximation of your GPS coordinates based on your public IPv4 address? (requires an active internet connection)"):
        pass
    elif getYesNo("\nWould you like to use an approximation based on a given city? (requires an active internet connection, uses Nominatim API)"):
        city = str(input(("Enter your city/country (format: New York, USA): ")))
        prayerTime.setCoordsbyCity(city)
    else:
        try:
            latitude = float(input("Enter your latitude coordinate (format: 12.34567): ").strip())
            longitude = float(input("Enter your longitude coordinate (format: 12.34567): ").strip())
            prayerTime.setGPScoordinates(latitude, longitude)
        except ValueError:
            print("Please enter a number in the given format")
    prayerTime.promptCalcMethod()
    if getYesNo("Would you like to use the Hanafi asr calculation method?"):
        prayerTime.ASR_METHOD = 2
    else: prayerTime.ASR_METHOD = 1

    print(prayerTime.printPrayerTimes())

def getYesNo(question: str) -> bool:
    while True:
        response = str(input(f"{question} (y/n) ")).strip().lower()
        if response in ('y', "yes"):
            return True
        elif response in ('n', "no"):
            return False
        else:
            print("Please answer with 'yes' or 'no'")

def getLocalUTCOffset(time) -> float:
    return ((datetime.fromtimestamp(time).timestamp()) - datetime.fromtimestamp(time, timezone.utc).replace(tzinfo=None).timestamp())/3600.0


class PrayerTime:
    ASR_METHOD = 1
    CalcMethod = namedtuple("CalcMethod", ["name", "fajr_angle", "isha_angle", "fixed"])
    __ts = time.time()
    __month = 0
    __day = 0.0
    __year = 0
    __utc_offset = 0.0
    __latitude = 0.0
    __longitude = 0.0
    __geolocator = Nominatim(user_agent='maruf')
    __daysDecimal = 0.0
    CALCULATION_METHOD = CalcMethod(0,0,0,0)

    def __init__(self, month=datetime.now().date().month, day=datetime.now().date().day, year=datetime.now().date().year, utc_offset=getLocalUTCOffset(time.time())):
        self.__month = month
        self.__day = day
        self.__year = year
        self.__utc_offset = utc_offset
        self.__daysDecimal = day + 0.5
    
    def setGPScoordinates(self, latitude: int, longitude: int):
        self.__latitude = latitude
        self.__longitude = longitude
    
    def setCoordsbyCity(self, city: str):
        location = self.geolocator.geocode(city)
        self.__latitude = location.latitude
        longitude = location.longitude

    def promptCalcMethod(self):
        print(f'''
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
        answer = input("\nChoose your calculation method: ").strip()
        # records calculation method as namedtuple 'CalcMethod' in order to maintain actual name of method as opposed just angles
        match answer:
            case 1:
                self.CALCULATION_METHOD = self.CalcMethod("MWL", 18.0, 17.0, False)
            case 2:
                self.CALCULATION_METHOD = self.CalcMethod("ISNA", 15.0, 15.0, False)
            case 3:
                self.CALCULATION_METHOD = self.CalcMethod("Umm al-Qura", 18.5, 90, True)
            case 4:
                self.CALCULATION_METHOD = self.CalcMethod("Gulf", 19.5, 90, True)
            case 5:
                self.CALCULATION_METHOD = self.CalcMethod("Algerian", 18.0, 17.0, False)
            case 6:
                self.CALCULATION_METHOD = self.CalcMethod("Karachi", 18.0, 18.0, False)
            case 7:
                self.CALCULATION_METHOD = self.CalcMethod("Diyanet", 18.0, 17.0, False)
            case 8:
                self.CALCULATION_METHOD = self.CalcMethod("Egypt", 19.5, 17.5, False)
            case 9:
                self.CALCULATION_METHOD = self.CalcMethod("EgyptBis", 20.0, 18.0, False)
            case 10:
                self.CALCULATION_METHOD = self.CalcMethod("Kemenag", 20.0, 18.0, False)
            case 11:
                self.CALCULATION_METHOD = self.CalcMethod("MUIS", 20.0, 18.0, False)
            case 12: 
                self.CALCULATION_METHOD = self.CalcMethod("JAKIM", 20.0, 18.0, False)
            case 13:
                self.CALCULATION_METHOD = self.CalcMethod("UDIF", 12.0, 12.0, False)
            case 14:
                self.CALCULATION_METHOD = self.CalcMethod("France15", 15.0, 15.0, False)
            case 15:
                self.CALCULATION_METHOD = self.CalcMethod("France18", 18.0, 18.0, False)
            case 16:
                self.CALCULATION_METHOD = self.CalcMethod("Tunisia", 18.0, 18.0, False)
            case 17:
                self.CALCULATION_METHOD = self.CalcMethod("Tehran", 17.7, 14.0, False)
            case 18:
                self.CALCULATION_METHOD = self.CalcMethod("Jafari", 16.0, 14.0, False)
            case _:
                self.CALCULATION_METHOD = self.CalcMethod("MWL", 18.0, 17.0, False)
        print(f"{self.CALCULATION_METHOD.name} chosen")

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
        
        >>> date_to_jd(1985,2,17.25)
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
    
    def __calcSunDeclination(self, JD: float) -> float:
        T = (2 * math.pi * (JD - 2451545)) / 365.25
        DELTA = 0.37877 + (23.264 * math.sin(math.radians((57.297*T) - 79.547))) + (0.3812 * math.sin(math.radians((2*57.297*T) - 82.682))) + (0.17132 * math.sin(math.radians((3*57.297*T) - 59.722)))
        return (T, DELTA)

    def __calcEqTime(self, JD: float) -> float:
        U = (JD - 2451545) / 36525
        L0 = 280.46607 + 36000.7698*U
        ET1000 = -(1789 + 237*U) * math.sin(math.radians(L0)) - (7146 - 62*U) * math.cos(math.radians(L0)) + (9934 - 14*U) * math.sin(math.radians(2*L0)) - (29 + 5*U) * math.cos(math.radians(2*L0)) + (74 + 10*U) * math.sin(math.radians(3*L0)) + (320 - 4*U) * math.cos(math.radians(3*L0)) - 212*math.sin(math.radians(4*L0))
        ET = ET1000 / 1000
        return ET

    def __calcSunTransitTime(self, utc_offset: float, longitude: float, eqTime: float) -> float:
        # calculates sun transit time
        TT = 12.0 + utc_offset - (longitude / 15.0) - (eqTime / 60.0)
        return TT

    def __calcSunAltitudes(self, fajr_angle: float, isha_angle: float, elevation: int, asr_method: int, sunDelta: float, latitude: float) -> dict:
        SA_FAJR = -(fajr_angle)
        SA_MAGHRIB = -0.8333 - (0.0347 * math.sqrt(elevation))
        SA_SUNRISE = SA_MAGHRIB
        SA_ASR = math.degrees(math.pow((1/math.tan(math.radians(asr_method + math.tan(math.radians(abs(sunDelta - latitude)))))), -1))
        SA_ISHA = -(isha_angle)
        sunAltitudes = dict(
                fajr = SA_FAJR,
                sunrise = SA_SUNRISE,
                asr = SA_ASR,
                maghrib = SA_MAGHRIB,
                isha = SA_ISHA
                )
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

        return hourAngles

    def __calcPrayerTimes(self) -> dict:
        JD = self.__calcJD(self.__year, self.__month, self.__daysDecimal)
        print(f"JD: {JD}")
        T, DELTA = self.__calcSunDeclination(JD)
        print(f"T: {T}")
        print(f"DELTA: {DELTA}")
        ET = self.__calcEqTime(JD)
        print(f"ET: {ET}")
        TT = self.__calcSunTransitTime(self.__utc_offset, self.__longitude, ET)
        print(f"TT: {TT}")
        sunAltitudes = self.__calcSunAltitudes(self.CALCULATION_METHOD.fajr_angle, self.CALCULATION_METHOD.isha_angle, 0, self.ASR_METHOD, DELTA, self.__latitude)
        print(f"sunAltitudes: {sunAltitudes}")
        hourAngles = self.__calcHourAngles(sunAltitudes, self.__latitude, DELTA)
        print(f"hourAngles: {hourAngles}")
        print(f"{self.__month}/{self.__day}/{self.__year}")

        FAJR = TT - (hourAngles["fajr"] / 15)
        SUNRISE = TT - hourAngles["sunrise"] / 15
        DHUHR = TT + 2/60
        ASR = TT + hourAngles["asr"] / 15
        MAGHRIB = TT + (hourAngles["maghrib"] / 15)
        ISHA = TT + hourAngles["isha"] / 15

        prayerTimes = dict (
                fajr= FAJR,
                sunrise= SUNRISE,
                dhuhr= DHUHR,
                asr= ASR,
                maghrib= MAGHRIB,
                isha= ISHA
                )
        return prayerTimes

    def printPrayerTimes(self):
        print(self.__calcPrayerTimes())

if __name__ == "__main__":
    main()
