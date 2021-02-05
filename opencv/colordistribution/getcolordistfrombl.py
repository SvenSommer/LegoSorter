import requests
import re
import pymysql


def importhtmlfromUrl(url, filename):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    result = requests.get(url, headers=headers)
    
    f = open(filename, "a")
    f.write(result.content.decode())
    f.close()

def readfile(filename):
    return open(filename, "r").read()

class ColorInformation(object):
    def __init__(self, colorid, partscount, yearFrom, yearTo):
        self.colorid = colorid
        self.partscount = partscount
        self.yearFrom = yearFrom
        self.yearTo = yearTo


class ColorPartCount(object):
    def __init__(self, colorid, partscount):
        self.colorid = colorid
        self.partscount = partscount

class ColorYearTimeSpan(object):
    def __init__(self,colorid, yearFrom, yearTo):
        self.colorid = colorid
        self.yearFrom = yearFrom
        self.yearTo = yearTo


def getColorInformationFromHTML(html):
   # x = re.findall('^(<TR ><TD  ALIGN="RIGHT"><FONT FACE="Tahoma,Arial" SIZE="2">).*(</TD></TR>)$', html)
    #colorids = [i.split('=')[2] for i in re.findall('v=2&colorID=\d{1,3}', html)]
    #print("found " + str(len(colorids)) + " colorids")

    colorInfos = []
    partsnormalfinds = re.findall('&colorPart=\d{1,3}">\d{1,6}', html)
    partsnormalid = [i.split('"')[0] for i in [i.split('=')[1] for i in partsnormalfinds]]
    partsnormal = [i.split('>')[1] for i in partsnormalfinds]

   
    if len(partsnormalid) == len(partsnormal) : 
        for i in range(0,len(partsnormalid)):  
            colorInfos.append(ColorPartCount(partsnormalid[i], partsnormal[i]))
    else:
        print("error: found " + str(len(partsnormal)) + " partsnormal and " + str(len(partsnormalid)) + " partsnormalid. Both must be equal")
   
    partsspecialfinds = re.findall('&colorPart=\d{1,3}&v=3">\d{1,6}', html)
    partsspecialid = [i.split('&')[0] for i in [i.split('=')[1] for i in partsspecialfinds]]
    partsspecial = [i.split('>')[1] for i in partsspecialfinds]
   
    if len(partsspecialid) == len(partsspecial) : 
        for i in range(0,len(partsspecialid)):  
            colorInfos.append(ColorPartCount(partsspecialid[i], partsspecial[i]))
    else:
        print("error: found " + str(len(partsspecial)) + " partsspecial and " + str(len(partsspecialid)) + " partsspecialid. Both must be equal")


    yearsinfos = []
    yearsfinds = re.findall('colorID=\d{1,3}&itemType=P&v=3">\d+</A>&nbsp;</TD><TD ALIGN="RIGHT"><FONT FACE="Tahoma,Arial" SIZE="2">&nbsp;\d{1,5}&nbsp;-&nbsp;\d{1,5}', html)
    yearscolorid = [i.split('&')[0] for i in [i.split('=')[1] for i in yearsfinds]]
    yearsfindsfrom = [i.split('&nbsp;')[2] for i in yearsfinds]
    yearsfindsto = [i.split('&nbsp;')[4] for i in yearsfinds]

    if len(yearscolorid) == len(yearsfindsfrom) : 
        for i in range(0,len(yearscolorid)):  
            yearsinfos.append(ColorYearTimeSpan(yearscolorid[i], yearsfindsfrom[i], yearsfindsto[i]))
    else:
        print("error: found " + str(len(yearscolorid)) + " yearscolorid and " + str(len(yearsfindsfrom)) + " yearsfindsfrom. Both must be equal")

    yearsfinds = re.findall('colorID=\d{1,3}&itemType=P">\d+</A>&nbsp;</TD><TD ALIGN="RIGHT"><FONT FACE="Tahoma,Arial" SIZE="2">&nbsp;\d{1,5}&nbsp;-&nbsp;\d{1,5}', html)
    yearscolorid = [i.split('&')[0] for i in [i.split('=')[1] for i in yearsfinds]]
    yearsfindsfrom = [i.split('&nbsp;')[2] for i in yearsfinds]
    yearsfindsto = [i.split('&nbsp;')[4] for i in yearsfinds]

    if len(yearscolorid) == len(yearsfindsfrom) : 
        for i in range(0,len(yearscolorid)):  
            yearsinfos.append(ColorYearTimeSpan(yearscolorid[i], yearsfindsfrom[i], yearsfindsto[i]))
    else:
        print("error: found " + str(len(yearscolorid)) + " yearscolorid and " + str(len(yearsfindsfrom)) + " yearsfindsfrom. Both must be equal")

    #print(colorids)
    #print(partsnormal)
    #print(partsnormalid)
    #print(partsspecial)
    #print(yearscolorid)
    #print(yearsfindsfrom)
    #print(yearsfindsto)
    colorInfos.sort(key=lambda x: x.colorid)
    yearsinfos.sort(key=lambda x: x.colorid)
    

    return colorInfos, yearsinfos

def UpdateColorPartsCount(colorid, partscount):
	global connection, cursor

	sql = "UPDATE `Colors` SET parts_count = %s WHERE color_id = %s"
	cursor.execute(sql, (partscount, colorid))
	connection.commit()

	return cursor.lastrowid

def UpdateYearImfortmation(colorid, yearfrom, yearto):
	global connection, cursor

	sql = "UPDATE `Colors` SET year_from = %s, year_to = %s WHERE color_id = %s"
	cursor.execute(sql, (yearfrom, yearto, colorid))
	connection.commit()

	return cursor.lastrowid



def main():
    filename = "catalogColors.asp"
    #html = importhtmlfromUrl('https://www.bricklink.com/catalogColors.asp', filename)
    html = readfile(filename)
    colorInfos, yearsinfos = getColorInformationFromHTML(html)

    for colorInfo in colorInfos:
        UpdateColorPartsCount(colorInfo.colorid,colorInfo.partscount)
        print("updated " + colorInfo.colorid + " : " + colorInfo.partscount )  
          
    for yearsinfo in yearsinfos:
        UpdateYearImfortmation(yearsinfo.colorid, yearsinfo.yearFrom, yearsinfo.yearTo)
        print(yearsinfo.colorid + " : " + yearsinfo.yearFrom + " - " + yearsinfo.yearTo)  


    # Todo: Write info to DB
    # Connect to Database

connection = pymysql.connect(host="localhost",    # your host, usually localhost
                    user="WebDBUser",         # your username
                    passwd="qF2J%9a84zU",  # your password
                    db="LegoSorterDB")        # name of the data base
cursor = connection.cursor()    
main()
connection.close()