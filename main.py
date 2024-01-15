from math import sin, cos, asin, acos, atan
import math
import datetime
import time
import urllib.request
import webbrowser

#Imported required libraries.

def dateConvTenK(t):
    return (float(t)-2000)/10000

#dateConvTenK(t) function returns decimal years to decimal 10 thousand years since J2000 epoch.

def dateConvCentury(t):
    return (float(t)-2000)/100

#dateConvCentury(t) function returns decimal years to decimal hundred years since J2000 epoch.

def obliquity(t):
    y = dateConvTenK(t)
    return 23.43929-(4680.93/3600)*y-(1.55/3600)*y**2+(1999.25/3600)*y**3-(51.38/3600)*y**4-(249.67/3600)*y**5-(39.05/3600)*y**6+(7.12/3600)*y**7+(27.87/3600)*y**8+(5.79/3600)*y**9+(2.45/3600)*y**10

#obliquity(t) function returns the obliquity at given decimal year.

def precession(t):
    y = dateConvCentury(t)
    return (5028.796195/3600)*y+(1.1054348/3600)*y**2+(0.00007964/3600)*y**3-(0.000023857/3600)*y**4-(0.0000000383/3600)*y**5

#precession(t) function returns the precession at given decimal year.

def sortByVmag(x):
    return float(x[3].strip())

def nep(t):
    return "18h0m0s " + str(round((90-obliquity(t)), 2))

#nep(t) function returns the coordinates of the ecliptic pole at given decimal year, relative to the current coordinate system.

def ddtodms(x):
    deg = int(x//1)
    minute = int(((x % 1)*60)//1)
    seconds = round(60*(((x % 1)*60) % 1), 2)
    return str(deg) + "d " + str(minute) + "m " + str(seconds) + "s "

#ddtodms(x) function returns decimal degrees in degrees, minutes, seconds format.

def ddtohms(x):
    x = (x % 360)
    hour = int(x//15)
    minute = int((x % 15)*4)
    seconds = round((x % 0.25)*240, 2)
    return str(hour) + "h " + str(minute) + "m " + str(seconds) + "s "

#ddtohms(x) function returns the decimal degrees in hours, minutes, seconds format.

def degtorad(x):
    return x*(math.pi/180)

#degtorad(x) function returns the decimal degrees in radians.

def radtodeg(x):
    return x*(180/math.pi)

#degtorad(x) fonksiyonu içine girilen radyan dereceyi ondalık derece olarak döndürür.
#degtorad(x) function returns the radians in decimal degrees.

#----------------------------------------------------------------------------------------------------

vmag=float(input("\nEnter a magnitude limit for the polar star candidates: "))
sensitivity=float(input("\nEnter how much can the polar star candidate can deviate from the north celestial pole in degrees: "))
t = input("\nEnter the date in decimal years which you want to calculate the north celestial pole: ")
#In this section, the user is asked criterias for the polar star candidates.
#----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------

now = datetime.datetime.today()

timepast = time.mktime(now.timetuple()) - \
    time.mktime(datetime.date(now.year, 1, 1).timetuple())
year = time.mktime(datetime.date(now.year+1, 1, 1).timetuple()) - \
    time.mktime(datetime.date(now.year, 1, 1).timetuple())

yearindecimal = now.year+(timepast/year)

oNow = obliquity(yearindecimal)
pNow = precession(yearindecimal)
o = obliquity(t)
p = precession(t)
n = nep(t)

print(f"\n\nObliquity: {round(o,2)} degrees / {ddtodms(o)}\nPrecession: {round(p-pNow,2)} degrees / {ddtodms(p-pNow)}\nEcliptic pole: {n}")
#In this section, required parameters are calculated and printed.
#----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------

ra = radtodeg(atan((-1*(sin(degtorad(p-pNow))*sin(degtorad(o)))/(cos(degtorad(oNow))*cos(degtorad(p-pNow))*sin(degtorad(o))-sin(degtorad(oNow))*cos(degtorad(o)))))) + 270
dec = radtodeg(asin((sin(degtorad(oNow))*cos(degtorad(p-pNow)) *
                     sin(degtorad(o)))+cos(degtorad(oNow))*cos(degtorad(o))))


print(f"\nCoordinates of the north celestial pole in year {t} relative to current celestial coordinates:\nRight ascension: {ddtohms(ra)}\nDeclination: {ddtodms(dec)}\n")
#In this section, coordinates of the north celestial pole at the given date are calculated relative to current celestial coordinates.
#----------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------

print("\nSearching Database...\n")

outputMode="COUNT"

stardb = f"http://simbad.u-strasbg.fr/simbad/sim-sam?Criteria=ra%3E{ra-sensitivity}%26ra%3C{ra+sensitivity}%26dec%3E{dec-sensitivity}%26dec%3C{dec+sensitivity}%26vmag%3C{vmag}%0D%0A&submit=submit+query&OutputMode={outputMode}&maxObject=50000&CriteriaFile=&output.format=ASCII&list.spsel=off&list.bibsel=off&list.notesel=off&obj.coo3=off&obj.coo4=off&obj.pmsel=off&obj.plxsel=off&obj.rvsel=off&obj.spsel=off&obj.mtsel=off&obj.sizesel=off&obj.bibsel=off&obj.messel=off&obj.notesel=off"
stardbresponsecount=urllib.request.urlopen(stardb).read().decode("utf-8")
objcount=int(stardbresponsecount.split(" ")[-1])

outputMode="LIST"

if (objcount>1):
    stardb = f"http://simbad.u-strasbg.fr/simbad/sim-sam?Criteria=ra%3E{ra-sensitivity}%26ra%3C{ra+sensitivity}%26dec%3E{dec-sensitivity}%26dec%3C{dec+sensitivity}%26vmag%3C{vmag}%0D%0A&submit=submit+query&OutputMode={outputMode}&maxObject=50000&CriteriaFile=&output.format=ASCII&list.spsel=off&list.bibsel=off&list.notesel=off&obj.coo3=off&obj.coo4=off&obj.pmsel=off&obj.plxsel=off&obj.rvsel=off&obj.spsel=off&obj.mtsel=off&obj.sizesel=off&obj.bibsel=off&obj.messel=off&obj.notesel=off"
    stardbresponse=urllib.request.urlopen(stardb).read().decode("utf-8")
    responseinlines=stardbresponse.split("\n")[9:-3]
    basicdata=[]
    for i in responseinlines:
        newline=i.split("|")[1:7]
        del newline[3]
        del newline[3]
        basicdata.append(newline)

    basicdata.sort(key=sortByVmag)

    print(f"{objcount} candidates found.\nCandidates sorted by magnitudes:\n\n#|            name                   |typ|       coord  (ICRS,J2000/2000)        |Mag   |\n-|-----------------------------------|---|---------------------------------------|------|")
    t=1
    for i in basicdata:
        line=str(t)+"|"
        for j in i:
            line+=j+"|"
        print(line)
        t+=1

elif (objcount==1):
    stardb = f"http://simbad.u-strasbg.fr/simbad/sim-sam?Criteria=ra%3E{ra-sensitivity}%26ra%3C{ra+sensitivity}%26dec%3E{dec-sensitivity}%26dec%3C{dec+sensitivity}%26vmag%3C{vmag}%0D%0A&submit=submit+query&OutputMode={outputMode}&maxObject=50000&CriteriaFile=&output.format=ASCII&list.spsel=off&list.bibsel=off&list.notesel=off&obj.coo3=off&obj.coo4=off&obj.pmsel=off&obj.plxsel=off&obj.rvsel=off&obj.spsel=off&obj.mtsel=off&obj.sizesel=off&obj.bibsel=off&obj.messel=off&obj.notesel=off&otypedisp=off"
    stardbresponse=urllib.request.urlopen(stardb).read().decode("utf-8")
    responseinlines=stardbresponse.split("\n")[5:-16]
    identifier=responseinlines[0][7:-59]
    objcoordinateslist=responseinlines[2][36:75].split(" ")
    objcoordinates=f"{objcoordinateslist[0]} {objcoordinateslist[1]} {objcoordinateslist[2]}  {objcoordinateslist[4]} {objcoordinateslist[5]} {objcoordinateslist[6]}"
    vmag=responseinlines[5].split(" ")[3]

    
    print(f"1 candidate found:\n\n            name                   |       coord  (ICRS,J2000/2000)        |Mag   |\n-----------------------------------|---------------------------------------|------|\n{identifier:<35}|{objcoordinates:<39}|{vmag:<6}|")

else:
    print("No candidates found.")
#In this section, suitable candidates are selected from the SIMBAD database and printed.
#----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------

print("\nLaunching celestial map in SKY-MAP.org...")

skymap = f"http://www.sky-map.org/?ra={((ra)%360)/15}&de={dec}&zoom=5&show_box=1"
webbrowser.open(skymap)
#In this section, north celestial pole on the given date is shown in the current celestial map.
#----------------------------------------------------------------------------------------------------
