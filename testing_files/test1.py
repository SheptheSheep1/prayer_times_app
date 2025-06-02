import math
from datetime import datetime, timedelta

class PrayerTimes:
    def __init__(self, latitude, longitude, date):
        self.latitude = latitude
        self.longitude = longitude
        self.date = date
        self.timezone = -7
        self.julian_date = self.calculate_julian_date()

    # Get the timezone offset in hours for the given date and location
    def get_timezone_offset(self):
        # Automatically get the current timezone offset
        offset = datetime.now().astimezone().utcoffset().total_seconds() / 3600
        return offset

    # Calculate the Julian date
    def calculate_julian_date(self):
        year = self.date.year
        month = self.date.month
        day = self.date.day
        if month <= 2:
            year -= 1
            month += 12
        A = math.floor(year / 100)
        B = 2 - A + math.floor(A / 4)
        JD = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5
        return JD

    # Calculate sun's declination angle (D)
    def sun_declination(self):
        D = self.julian_date - 2451545.0
        g = math.radians((357.529 + 0.98560028 * D) % 360)
        sun_declination = math.degrees(math.asin(math.sin(math.radians(23.44)) * math.sin(g)))
        return sun_declination

    # Helper function to calculate the arccotangent
    def arccot(self, x):
        return math.atan(1 / x)

    # Calculate Asr time based on Hanafi school
    def compute_asr_hanafi(self):
        sun_decl = self.sun_declination()
        lat_diff = abs(self.latitude - sun_decl)
        G = -self.arccot(2 + self.tan(math.radians(lat_diff)))

        return self.compute_time(G)

    # Helper function to calculate solar time
    def compute_time(self, G):
        # Solar noon calculation based on longitude and timezone
        D = self.julian_date - 2451545.0
        g = math.radians((357.529 + 0.98560028 * D) % 360)
        eq_time = (229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g)))
        
        solar_noon = 12 - ((4 * self.longitude + eq_time) / 60) + self.timezone

        # Calculate Asr time using solar hour angle G
        asr_time = solar_noon + G * 4 / 60  # G is in radians, so we convert it to time
        asr_time = self.adjust_time(asr_time)
        
        return asr_time

    # Adjust time to fit into the 24-hour format
    def adjust_time(self, time):
        if time < 0:
            time += 24
        elif time >= 24:
            time -= 24
        hours = int(time)
        minutes = int((time - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"

    # Tangent function with degrees to radians conversion
    def tan(self, x):
        return math.tan(x)

# Example usage
latitude = 33.6844  # Example latitude (e.g., Mecca)
longitude = -111.0  # Example longitude (e.g., Mecca)
date = datetime.now()

prayer_times = PrayerTimes(latitude, longitude, date)
hanafi_asr_time = prayer_times.compute_asr_hanafi()

print(f"Hanafi Asr time: {hanafi_asr_time}")

