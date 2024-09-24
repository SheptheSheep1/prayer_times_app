import math
def arccot(x):
    return math.pi / 2 - math.atan(x)
jd = 2460575.311366
d = jd - 2451545.0  # jd is the given Julian date 

g = 357.529 + 0.98560028* d
q = 280.459 + 0.98564736* d
L = q + 1.915* math.sin(math.radians(g)) + 0.020* math.sin(math.radians(2*g))

R = 1.00014 - 0.01671* math.cos(math.radians(g)) - 0.00014* math.cos(math.radians(2*g))
e = 23.439 - 0.00000036* d
RA = math.degrees(math.atan2(math.cos(math.radians(e))* math.sin(math.radians(L)), math.cos(math.radians(L))))/ 15

D = math.degrees(math.asin(math.sin(math.radians(e))* math.sin(math.radians(L))))  # declination of the Sun
Lat = 33.4306  # latitude of the observer
EqT = q/15 - RA  # equation of time

top = math.sin(math.radians(math.degrees(arccot(2+math.tan(math.radians(Lat-D))))-math.degrees((math.sin(math.radians(Lat)))*math.sin(math.radians(D)))))
print(f"top: {top}")
bottom = math.cos(math.radians(Lat))*math.cos(math.radians(D))
print(f"bottom: {bottom}")
asr_del = (1/15)*(math.degrees(math.acos(top/bottom)))
print(f"asr_del: {asr_del}")
dhuhr = 12.3778
asr = dhuhr + asr_del
print(f"asr: {asr}")
print(f"delta: {D}")
print(f"EqT: {EqT}")
