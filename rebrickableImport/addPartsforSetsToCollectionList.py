import rebrickable_config
import argparse
import requests
from requests.auth import HTTPDigestAuth
import json
import os
from io import BytesIO
import math
#  python addPartsforSetsToCollectionList.py -c 1 -s 70748,9526,60182,7065,7633,7686,7685,7248,7733,8060,7737,7631,4439,7647,8059,7632,7693,9479,70005,75015,9675,7929,7877


PARTS_PER_FILE = 200 

def getAvailableParts(folder):
    fileNames = [fileName[:-4] for fileName in os.listdir(folder) if fileName.endswith(".dat")]
    fileNames.sort()
    return fileNames

def getPartsList(url):

    myResponse = requests.get(url,params={'key':rebrickable_config.key, 'inc_part_details': '1'})

    if(myResponse.ok):
        jData = json.loads(myResponse.content)

    else:
        myResponse.raise_for_status()
    
    return jData

def importSetPartsFromRebrickable(setNo):
    url = rebrickable_config.mainurl + 'sets/' + setNo + '-1/parts/?page_size=1000'
    parts = []
    partsList = getPartsList(url)
    for piece in partsList['results']:
        parts.append(piece['part']['part_num'])
    print(str(len(parts)) + " parts from Rebrickable api for set "  + str(setNo) + " received.")
    return parts

def makeLDRDrawfile(colNo, setNos):
    print("-IMPORT-")
    uniqueParts = []
    for setNo in setNos.split(","): 
        setParts = importSetPartsFromRebrickable(setNo)
        setParts = set(setParts) - set(uniqueParts)
        print(str(len(setParts)) + " unique new parts in set " + setNo + " identified.")
        uniqueParts.extend(setParts)
    print("-SUMMARY-")
    print(str(len(uniqueParts)) + " unique parts identified.")

    availableParts = getAvailableParts("./parts")
    uniqueAndAvailableParts = [x for x in uniqueParts if x in availableParts]
    partlists = divide_chunks(list(uniqueAndAvailableParts), PARTS_PER_FILE)
    print(str(len(uniqueAndAvailableParts)) + " of those are available in LDraw database at the moment.")
    print("---------")
    print(str(len(uniqueParts) - len(uniqueAndAvailableParts)) + " parts are missing and will be ignored.")

    print("-WRITING-")   
    filecounter = 1
    totalfilenumber = math.ceil(len(uniqueAndAvailableParts)/PARTS_PER_FILE)
    print("Will write " + str(totalfilenumber) + " files in batches of " + str(PARTS_PER_FILE) +" parts per file.")
    for partlist in partlists:
        writeFileWithParts(colNo, partlist, filecounter, totalfilenumber)
        filecounter += 1
    print("-DONE-")  
    
def divide_chunks(partlist, n):   
    n = max(1, n)
    return (partlist[i:i+n] for i in range(0, len(partlist), n))
    
def writeFileWithParts(colNo, parts, actualfilenumber, totalfilenumber):
     # Create subfolder
    collectionfolder = "collection" + colNo + "_part_" + str(actualfilenumber) + "_of_" + str(totalfilenumber)
    if not os.path.exists(collectionfolder):
        os.makedirs(collectionfolder)
        print("Created folder: " + collectionfolder)

    # Create image folder
    imagesfolder = os.path.join(collectionfolder,"unlabeled_images")
    if not os.path.exists(imagesfolder):
        os.makedirs(imagesfolder)
        print("Created folder: " + imagesfolder)

    filename =  os.path.join(collectionfolder, collectionfolder + ".ldr")
    
    LDRAW_file = open(filename, "w")

    partscounter = 0
    for piece in parts:
        line = '1 9 0 0 0 1 0 0 0 1 0 0 0 1 ' + str(piece) + ".dat"
        LDRAW_file.write(line)
        LDRAW_file.write("\n")
        partscounter += 1
    LDRAW_file.close()
    print("Created/added to '" + filename + "' " + str(partscounter) + " new parts\n")

def run():
    parser = argparse.ArgumentParser(description='Writes a file with included LDRAW parts for a given SetNos')
    parser.add_argument('-c','--colNo', help='Collection the LDRAW-file is created for.', required=True)
    parser.add_argument('-s','--setNos', help='SetNos for the parts that will be added.', required=True)
    args = vars(parser.parse_args())
    makeLDRDrawfile(args['colNo'], args['setNos'])

run()