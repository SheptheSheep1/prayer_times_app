#from enum import Enum

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
#class MethodName(Enum):
#    MUWL = "Muslim World League"
#    ISNA = "Islamic Society of North America"
#    UAQU = "Umm al-Qura"
#    GULF = "Gulf"
#    ALGR = "Algerian"
#    KRCH = "University of Islamic Sciences, Karachi"
#    DYNT = "Diyanet"
#    EGPT = "Egypt"
#    EGPB = "EgyptBis"
#    KMNG = "Kemenag"
#    MUIS = "MUIS"
#    JAKM = "JAKIM"
#    UDIF = "UDIF"
#    FR15 = "France15"
#    FR18 = "France18"
#    TUNS = "Tunisia"
#    THRN = "Tehran"
#    JAFA = "Jafari"

methods = {
    "Muslim World League": CalcMethod("Muslim World League", 18.0, 17.0, False),
    "Islamic Society of North America": CalcMethod("Islamic Society of North America", 15.0, 15.0, False),
    "Umm al-Qura University, Makkah": CalcMethod("Umm al-Qura University, Makkah", 18.5, 0.0, True),
    "Gulf Region": CalcMethod("Gulf Region", 19.5, 0.0, True),
    "Algerian Ministry of Religious Affairs and Waqfs": CalcMethod("Algerian Ministry of Religious Affairs and Waqfs", 18.0, 17.0, False),
    "University of Islamic Sciences, Karachi": CalcMethod("University of Islamic Sciences, Karachi", 18.0, 18.0, False),
    "Diyanet İşleri Başkanlığı": CalcMethod("Diyanet İşleri Başkanlığı", 18.0, 17.0, False),
    "Egyptian General Authority of Survey": CalcMethod("Egyptian General Authority of Survey", 19.5, 17.5, False),
    "Egyptian General Authority of Survey, Bis": CalcMethod("Egyptian General Authority of Survey, Bis", 20.0, 18.0, False),
    "Kementerian Agama Republik Indonesia": CalcMethod("Kementerian Agama Republik Indonesia", 20.0, 18.0, False),
    "Majlis Ugama Islam Singapura": CalcMethod("Majlis Ugama Islam Singapura", 20.0, 18.0, False),
    "Jabatan Kemajuan Islam Malaysia": CalcMethod("Jabatan Kemajuan Islam Malaysia", 20.0, 18.0, False),
    "Union Des Organisations Islamiques De France": CalcMethod("Union Des Organisations Islamiques De France", 12.0, 12.0, False),
    u"France Region 15\N{DEGREE SIGN}": CalcMethod(u"France Region 15\N{DEGREE SIGN}", 15.0, 15.0, False),
    u"France Region 18\N{DEGREE SIGN}": CalcMethod(u"France Region 18\N{DEGREE SIGN}", 18.0, 18.0, False),
    "Tunisian Ministry of Religious Affairs": CalcMethod("Tunisian Ministry of Religious Affairs", 18.0, 18.0, False),
    "Institute of Geophysics at University of Tehran": CalcMethod("Institute of Geophysics at University of Tehran", 17.7, 14.0, False),
    "Jafari: Shia Ithna Ashari": CalcMethod("Jafari: Shia Ithna Ashari", 16.0, 14.0, False)
}
