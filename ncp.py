"""
Copyright 2021 Lütfi Ilgaz Cengiz

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from math import sin, cos, asin, acos, atan
import math
import datetime
import time
import urllib.request
import webbrowser

#Yukarıda gereken kütüphaneler eklendi.

def dateConvTenK(t):
    return (float(t)-2000)/10000

#dateConvTenK(t) fonksiyonu içine ondalık yıl olarak girilen tarihi J2000 eşiğinden itibaren ondalık 10 bin yıl olarak geri döndürür.

def dateConvCentury(t):
    return (float(t)-2000)/100

#dateConvCentury(t) fonksiyonu içine ondalık yıl olarak girilen tarihi J2000 eşiğinden itibaren ondalık yüzyıllar olarak geri döndürür.

def obliquity(t):
    y = dateConvTenK(t)
    return 23.43929-(4680.93/3600)*y-(1.55/3600)*y**2+(1999.25/3600)*y**3-(51.38/3600)*y**4-(249.67/3600)*y**5-(39.05/3600)*y**6+(7.12/3600)*y**7+(27.87/3600)*y**8+(5.79/3600)*y**9+(2.45/3600)*y**10

#obliquity fonksiyonu(t) içine girilen ondalık yıl olarak girilen tarihteki eksen eğikliğini hesaplayıp geri döndürür.

def precession(t):
    y = dateConvCentury(t)
    return (5028.796195/3600)*y+(1.1054348/3600)*y**2+(0.00007964/3600)*y**3-(0.000023857/3600)*y**4-(0.0000000383/3600)*y**5

#obliquity(t) fonksiyonu içine girilen ondalık yıl olarak girilen tarihteki devinimi J2000 eşiğinden itibaren hesaplayıp geri döndürür.

def sortByVmag(x):
    return float(x[3].strip())

#sortByVmag(x) fonksiyonu SIMBAD'dan alınan obje verilerini kadirlerine göre sıralamak için .sort() fonksiyonunun key parametresinde kullanılır.

def nep(t):
    return "18h0m0s " + str(round((90-obliquity(t)), 2))

#nep(t) fonksiyonu ondalık yıl olarak girilen tarihteki ekliptik noktasının kordinatlarını, fonksiyonun çalıştırıldığı tarihteki göksel kordinat sistemine göre döndürür.

def ddtodms(x):
    deg = int(x//1)
    minute = int(((x % 1)*60)//1)
    seconds = round(60*(((x % 1)*60) % 1), 2)
    return str(deg) + "d " + str(minute) + "m " + str(seconds) + "s "

#ddtodms(x) fonksiyonu içine girilen ondalık dereceyi derece dakika saniye formatında döndürür.

def ddtohms(x):
    x = (x % 360)
    hour = int(x//15)
    minute = int((x % 15)*4)
    seconds = round((x % 0.25)*240, 2)
    return str(hour) + "h " + str(minute) + "m " + str(seconds) + "s "

#ddtohms(x) fonksiyonu içine girilen ondalık dereceyi saat dakika saniye formatında döndürür.

def degtorad(x):
    return x*(math.pi/180)

#degtorad(x) fonksiyonu içine girilen ondalık dereceyi radyan derece olarak döndürür.

def radtodeg(x):
    return x*(180/math.pi)

#degtorad(x) fonksiyonu içine girilen radyan dereceyi ondalık derece olarak döndürür.

#----------------------------------------------------------------------------------------------------

vmag=float(input("\nKutup Yıldızı adayı seçimi için bir kadir limiti giriniz: "))
sensitivity=float(input("\nKutup Yıldızı adayının eksenlerden kaç derece sapmaya kadar tolere edilebileceğini derece cinsinden giriniz: "))
t = input("\nOndalık yıl olarak bir tarih giriniz: ")
#Bu bölümde kullanıcının belirleyeceği yıldız belirlenirkenki kadir limiti, eksenlerden kaçar derece sapmaya tolerans gösterilebileceği ve tarih kriterler alındı.
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

print(f"\n\nEksen Eğikliği: {round(o,2)} derece / {ddtodms(o)}\nDevinim: {round(p-pNow,2)} derece / {ddtodms(p-pNow)}\nEkliptik Noktası: {n}")
#Bu bölümde programın çalıştırıldığı tarihteki ve girilen tarihteki eksen eğikliği, devinim ve ekliptik noktası hesaplandı; girilen tarihteki eksen eğikliği, devinim ve ekliptik noktasının koordinatları yazdırıldı.
#----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------

ra = radtodeg(atan((-1*(sin(degtorad(p-pNow))*sin(degtorad(o)))/(cos(degtorad(oNow))*cos(degtorad(p-pNow))*sin(degtorad(o))-sin(degtorad(oNow))*cos(degtorad(o)))))) + 270
dec = radtodeg(asin((sin(degtorad(oNow))*cos(degtorad(p-pNow)) *
                     sin(degtorad(o)))+cos(degtorad(oNow))*cos(degtorad(o))))


print(
    f"\n{t} yılındaki Göksel Kutup Noktası'nın şuanki göksel koordinat sistemine göre koordinatları:\nSağ Açıklık: {ddtohms(ra)}\nDik Açıklık: {ddtodms(dec)}\n")
#Bu bölümde girilen tarihteki Göksel Kutup Noktası'nın, programın çalıştırıldığı tarihteki göksel koordinat sistemine göre koordinatları hesaplanıp yazdırıldı.
#----------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------

print("\nVeritabanı taranıyor...\n")

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

    print(f"Kriterlere uygun {objcount} aday bulundu.\nAdaylar kadirlerine göre sıralanmış şekilde:\n\n#|            isim                   |tip|       koord  (ICRS,J2000/2000)        |Kadir |\n-|-----------------------------------|---|---------------------------------------|------|")
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

    
    print(f"Kriterlere uygun 1 aday bulundu:\n\n            isim                   |       koord  (ICRS,J2000/2000)        |Kadir |\n-----------------------------------|---------------------------------------|------|\n{identifier:<35}|{objcoordinates:<39}|{vmag:<6}|")

else:
    print("Kriterlere uygun Kutup Yıldızı adayı bulunamadı.")
#Bu bölümde SIMBAD veritabanından kriterlere uygun yıldızlar seçildi, kadir sırasına dizildi ve formatlanarak yazdırıldı.
#----------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------

print("\nGöksel Kutup Noktası SKY-MAP.org'da açılıyor...")

skymap = f"http://www.sky-map.org/?ra={((ra)%360)/15}&de={dec}&zoom=5&show_box=1"
webbrowser.open(skymap)
#Bu bölümde girilen tarihteki göksel kutup noktası programın çalıştırıldığı tarihteki göksel koordinat sisteminde görsel olarak SKY-MAP.org gök haritasında tarayıcıda gösterildi.
#----------------------------------------------------------------------------------------------------
