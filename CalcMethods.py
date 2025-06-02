from enum import Enum

# contains individual calc methods
class CalcMethod:
    def __init__(self, name="MWL", fajr_angle=18.0, isha_angle=17.0, fixed=False):
        self.name = name
        self.fajr_angle = fajr_angle
        self.isha_angle = isha_angle
        self.fixed = fixed

    def __str__(self):
        return (self.name)

# defines Enums containing calc methods
class MethodName(Enum):
    MUWL = "Muslim World League"
    ISNA = "Islamic Society of North America"
    UAQU = "Umm al-Qura"
    GULF = "Gulf"
    ALGR = "Algerian"
    KRCH = "University of Islamic Sciences, Karachi"
    DYNT = "Diyanet"
    EGPT = "Egypt"
    EGPB = "EgyptBis"
    KMNG = "Kemenag"
    MUIS = "MUIS"
    JAKM = "JAKIM"
    UDIF = "UDIF"
    FR15 = "France15"
    FR18 = "France18"
    TUNS = "Tunisia"
    THRN = "Tehran"
    JAFA = "Jafari"

methods = {
    "MWL": CalcMethod("MWL", 18.0, 17.0, False),
    "ISNA": CalcMethod("ISNA", 15.0, 15.0, False),
    "Umma al-Qura": CalcMethod("Umm al-Qura", 18.5, 90, True),
    "Gulf": CalcMethod("Gulf", 19.5, 90, True),
    "Algerian": CalcMethod("Algerian", 18.0, 17.0, False),
    "Karachi ": CalcMethod("Karachi", 18.0, 18.0, False),
    "Diyanet": CalcMethod("Diyanet", 18.0, 17.0, False),
    "Egypt": CalcMethod("Egypt", 19.5, 17.5, False),
    "EgyptBis": CalcMethod("EgyptBis", 20.0, 18.0, False),
    "Kemenag": CalcMethod("Kemenag", 20.0, 18.0, False),
    "MUIS": CalcMethod("MUIS", 20.0, 18.0, False),
    "JAKIM": CalcMethod("JAKIM", 20.0, 18.0, False),
    "UDIF": CalcMethod("UDIF", 12.0, 12.0, False),
    "France15": CalcMethod("France15", 15.0, 15.0, False),
    "France18": CalcMethod("France18", 18.0, 18.0, False),
    "Tunisia": CalcMethod("Tunisia", 18.0, 18.0, False),
    "Tehran": CalcMethod("Tehran", 17.7, 14.0, False),
    "Jafari": CalcMethod("Jafari", 16.0, 14.0, False)
}
