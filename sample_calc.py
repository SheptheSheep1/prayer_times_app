## sample calculations to serve as framework for other calculations
import math
LAT = 35 ## latitude
LONG = 69 ## longitude
H = 1787 ## elevation
## H = 0
Z = 4.5 ## utc timezone
SF = 2 ## Hanafi asr
## University of Islamic Sciences, Karachi Angle for Afghanistan
FAJR_ANGLE = 18 
ISHA_ANGLE = 18

## Calculate Julian days at local time
Y = 2024
M = 7
D = 14
H_jd = 16.000
m = 0 
s = 0
Z = 4.5

A = int(Y/100)

B = 2 + math.floor(A/4) - A
## Julian days
JD = 1720994.5 + int(365.25*Y) + int(30.6001*(M + 1)) + B + D + (((H_jd*3600) + (m*60) + s) / 86400) - (Z / 24)
print("%s converted to %s"%((365.25*Y),(int(365.25*Y))))
print("JD: %f"%JD)

## Calculate Sun declination
T = (2 * math.pi * (JD - 2451545)) / 365.25
print("T: %f"%T)
DELTA = 0.37877 + (23.264 * math.sin(math.radians((57.297*T) - 79.547))) + (0.3812 * math.sin(math.radians((2*57.297*T) - 82.682))) + (0.17132 * math.sin(math.radians((3*57.297*T) - 59.722)))
print("DELTA: %f"%DELTA)

## Eq. of time
U = (JD - 2451545) / 36525
print("U: %f"%U)
L0 = 280.46607 + 36000.7698*U
print("L0: %f"%L0)
ET1000 = -(1789 + 237*U) * math.sin(math.radians(L0)) - (7146 - 62*U) * math.cos(math.radians(L0)) + (9934 - 14*U) * math.sin(math.radians(2*L0)) - (29 + 5*U) * math.cos(math.radians(2*L0)) + (74 + 10*U) * math.sin(math.radians(3*L0)) + (320 - 4*U) * math.cos(math.radians(3*L0)) - 212*math.sin(math.radians(4*L0))
ET = ET1000 / 1000
print("ET: %f"%ET)

## Calculate sun transit time
TT = 12 + Z - (LONG / 15) - (ET / 60)
print("TT: %f"%TT)

## Calculate Sun altitudes
SA_FAJR = -(FAJR_ANGLE)
SA_MAGHRIB = 0.8333 + (0.0347 * math.sqrt(H))
SA_SUNRISE = SA_MAGHRIB
print("SA_SUNRISE: ", SA_SUNRISE)
SA_ASR = math.degrees(math.pow((1/math.tan(math.radians(SF + math.tan(math.radians(abs(DELTA - LAT)))))), -1))
SA_ISHA = -(ISHA_ANGLE)

## Calculate hour angle
cos_HA_FAJR = (math.sin(math.radians(SA_FAJR)) - math.sin(math.radians(LAT)) * math.sin(math.radians(DELTA))) / (math.cos(math.radians(LAT)) * math.cos(math.radians(DELTA)))
print("cos_HA_FAJR: %f"%cos_HA_FAJR)
cos_HA_MAGHRIB = (math.sin(math.radians(SA_SUNRISE))) - math.sin(math.radians(LAT)) * math.sin(math.radians(DELTA)) / (math.sin(math.radians(LAT)) * math.cos(math.radians(DELTA)))
cos_HA_SUNRISE = cos_HA_MAGHRIB


HA_FAJR = math.degrees(math.acos(cos_HA_FAJR))
print("HA_FAJR: %f"%HA_FAJR)
HA_MAGHRIB = math.degrees(math.acos(cos_HA_SUNRISE))
HA_SUNRISE = HA_MAGHRIB

FAJR = TT - (HA_FAJR / 15)
SUNRISE = TT - (HA_SUNRISE / 15)
MAGHRIB = TT + (HA_MAGHRIB / 15)
DHUHR = TT + 2/60

print("FAJR TIME: %f"%FAJR)
print("SUNRISE TIME: %f"%SUNRISE)
print("DHUHR TIME: %f"%DHUHR)
print("MAGHRIB TIME: %f"%MAGHRIB)
