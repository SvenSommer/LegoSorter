#!/usr/bin/python
import pymysql
import os
from shutil import copyfile
from pathlib import Path


db = pymysql.connect(host="localhost",    # your host, usually localhost
                     user="WebDBUser",         # your username
                     passwd="qF2J%9a84zU",  # your password
                     db="LegoSorterDB")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()
imagecounter = 0
imageskipped = 0
def moveImage(imagepath, destinationfolder, partno):
    global imagecounter, imageskipped
    #create sourcefolder if not exisiting
    partdestfolder = os.path.join(destinationfolder,partno) 
    if not os.path.exists(partdestfolder):
        print("    Creating partdestfolder: " + partdestfolder)
        os.makedirs(partdestfolder)
   
    fileto = os.path.join(partdestfolder,os.path.basename(imagepath))
    if not Path(fileto).is_file():
        copyfile(imagepath, fileto)
        print("    Writing file: " + fileto)    
        imagecounter += 1
    else:
        print("    File already exists: " + fileto)
        imageskipped += 1


# Use all the SQL you like
cur.execute("""SELECT rp.no, path FROM LegoSorterDB.Partimages pi 
LEFT JOIN LegoSorterDB.Recognisedimages ri ON pi.id = ri.image_id
LEFT JOIN LegoSorterDB.Recognisedparts rp ON ri.part_id = rp.id
WHERE ri.score IS NOT NULL AND pi.deleted IS NULL""")

destinationfolder = "/home/robert/LegoSorter/sorted_partimages"
# print all the first cell of all the rows
for row in cur.fetchall():
    moveImage(row[1],destinationfolder,row[0])
    partno = row[0]
    path = row[1]
    
print("Wrote "  + str(imagecounter) + " image files. Skipped " + str(imageskipped) + " Files")
db.close()