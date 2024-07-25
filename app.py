import time
from datetime import datetime, timezone

def main():
    obj = PrayerTime()
    #print(time.localtime().tm_gmtoff/60/60)
    #print(datetime.now(timezone.utc).astimezone())
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
    if getYesNo("Ma'ruf requires GPS latitude and longitude coordinates in order to calculate prayer times\nWould you like to use an approximation of your GPS coordinates based on your public IPv4 address? (requires an active internet connection)"):
        pass
    elif getYesNo("Would you like to use an approximation based on your city? (requires an active internet connection)"):
        city = str(input(("Enter your city/country (format: New York, USA)")))
        pass
    else:
        try:
            latitude = float(input("Enter your latitude coordinate (format: 12.34567): ").strip())
            longitude = float(input("Enter your longitude coordinate (format: 12.34567): ").strip())
            prayerTime.setGPScoordinates(latitude, longitude)
        except ValueError:
            print("Please enter a number in the given format")

def getYesNo(question: str) -> bool:
    while True:
        response = str(input(f"{question} (y/n) ")).strip().lower()
        if response in ('y', "yes"):
            return True
        elif response in ('n', "no"):
            return False
        else:
            print("Please answer with 'yes' or 'no'")

class PrayerTime:
    __ts = time.time()
    __month = 0
    __day = 0
    __year = 0
    __utc_offset = 0.0
    __latitude = 0.0
    __longitude = 0.0

    def __init__(self, month, day, year, utc_offset):
        self.__month = month
        self.__day = day
        self.__year = year
        self.__utc_offset = utc_offset

    def __init__(self):
        self.__utc_offset = self.__getLocalUTCOffset()

    def __getLocalUTCOffset(self) -> float:
        self.__ts= time.time()
        return ((datetime.fromtimestamp(self.__ts).timestamp()) - datetime.fromtimestamp(self.__ts, timezone.utc).replace(tzinfo=None).timestamp())/3600.0
    
    def setGPScoordinates(self, latitude: int, longitude: int):
        self.__latitude = latitude
        self.__longitude = longitude

if __name__ == "__main__":
    main()
