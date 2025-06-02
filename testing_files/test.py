import math
import datetime

# Function to calculate the Julian Day
def calculate_julian_day(year, month, day):
    # Formula to calculate Julian Day Number
    if month <= 2:
        year -= 1
        month += 12
    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    JD = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5
    return JD

# Function to calculate solar noon (approximation)
def calculate_solar_noon(lon, jd):
    n = jd - 2451545.0 + 0.0008  # days since J2000.0
    j_star = n - lon / 360.0  # mean solar time
    solar_noon_utc = (j_star - math.floor(j_star)) * 24.0  # in UTC hours
    return solar_noon_utc

# Function to estimate sunrise and sunset times (approximation)
def calculate_sun_times(latitude, jd):
    # This is a very rough estimation using basic astronomical formulas for sun angle
    # Sunrise and sunset estimation using 90 degrees angle (more complex calculations would give a better result)
    declination = -23.44 * math.cos(math.radians(360 / 365 * (jd + 10)))
    hour_angle = math.degrees(math.acos(math.cos(math.radians(90.833)) / (math.cos(math.radians(latitude)) * math.cos(math.radians(declination))) - math.tan(math.radians(latitude)) * math.tan(math.radians(declination))))
    return hour_angle / 15.0  # in hours

# Function to calculate Asr Hanafi time
def calculate_asr_hanafi(solar_noon, latitude):
    # Approximation: Asr Hanafi occurs approximately 2 hours after solar noon at this latitude
    asr_hanafi = 12.377814199444966 + (2.0 * latitude / 15.0)  # approximate time offset in hours
    return asr_hanafi

# Given data for Tempe, Arizona, on September 21, 2024
latitude = 33.4306
longitude = -111.9256
date = datetime.date(2024, 9, 21)

# Calculate the Julian Day for the given date
jd = calculate_julian_day(date.year, date.month, date.day)

# Calculate solar noon (UTC) and adjust for timezone
solar_noon_utc = calculate_solar_noon(longitude, jd)
timezone_offset = -7  # Arizona is UTC-7
solar_noon_local = solar_noon_utc + timezone_offset

# Estimate sunrise and sunset times (approximate calculation)
sun_hour_angle = calculate_sun_times(latitude, jd)
sunrise_local = solar_noon_local - sun_hour_angle  # sunrise is before solar noon
sunset_local = solar_noon_local + sun_hour_angle  # sunset is after solar noon

# Calculate Asr Hanafi time (approximately 2 hours after solar noon)
asr_hanafi_local = calculate_asr_hanafi(solar_noon_local, latitude)

# Output the results
print(f"Location: Tempe, Arizona")
print(f"Date: {date}")
print(f"Sunrise (approx): {sunrise_local:.2f} hours local time")
print(f"Solar Noon: {solar_noon_local:.2f} hours local time")
print(f"Sunset (approx): {sunset_local:.2f} hours local time")
print(f"Asr (Hanafi) (approx): {asr_hanafi_local} hours local time")

