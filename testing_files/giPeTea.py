import math
from datetime import datetime, timedelta

def calculate_declination(day_of_year):
    # Approximation for solar declination
    return 23.44 * math.sin(math.radians((360 / 365) * (day_of_year - 81)))

def calculate_solar_noon(longitude, utc_offset):
    # Approximation of solar noon in local time
    return 12 - (longitude / 15) + utc_offset

def calculate_hour_angle(latitude, declination, shadow_factor):
    latitude_rad = math.radians(latitude)
    declination_rad = math.radians(declination)
    
    # Calculate the angle whose tangent is shadow_factor
    angle_rad = math.atan(shadow_factor / (math.tan(latitude_rad - declination_rad)))
    
    # Convert angle to hour angle
    return math.degrees(angle_rad)

def asr_hanafi(latitude, longitude, utc_offset, date_today):
    day_of_year = date_today.timetuple().tm_yday
    declination = calculate_declination(day_of_year)
    solar_noon = calculate_solar_noon(longitude, utc_offset)
    
    # Calculate the hour angle for the shadow factor
    hour_angle = calculate_hour_angle(latitude, declination, 2)
    
    # Calculate Asr time in hours from solar noon
    asr_time_utc = solar_noon + (hour_angle / 15)
    asr_time = datetime.combine(date_today, datetime.min.time()) + timedelta(hours=asr_time_utc)
    
    return asr_time

# Example usage
latitude = 34.0  # Latitude for London
longitude = 69.0  # Longitude for London
utc_offset = 4.5  # UTC offset for London (BST)
date_today = datetime.now().date()

asr_time = asr_hanafi(latitude, longitude, utc_offset, date_today)
print(f"Asr prayer time (Hanafi) is at: {asr_time.strftime('%H:%M:%S')}")

