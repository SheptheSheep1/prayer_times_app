import time
from datetime import datetime, timezone

def main():
    #print(time.localtime().tm_gmtoff/60/60)
    #print(datetime.now(timezone.utc).astimezone())
    ts = time.time()
    utc_offset = ((datetime.fromtimestamp(ts).timestamp()) - datetime.fromtimestamp(ts, timezone.utc).replace(tzinfo=None).timestamp())/3600.0
    print(utc_offset)

#def convertTimeDec(time: int) 
class PrayerTime:
    def __init__(self, month, day, year, hour, minute):
        pass
    

if __name__ == "__main__":
    main()
