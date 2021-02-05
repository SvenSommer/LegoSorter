import rebrickable_config
import argparse
import requests
from requests.auth import HTTPDigestAuth
import json
import os
from PIL import Image
from io import BytesIO


def getPartsList(url):

    myResponse = requests.get(url,params={'key':rebrickable_config.key, 'inc_part_details': '1'})

    if(myResponse.ok):
        jData = json.loads(myResponse.content)

    else:
        myResponse.raise_for_status()
    
    return jData

def partsImportLDRAW(setNo):

    url = rebrickable_config.mainurl + 'sets/' + setNo + '-1/parts/'
    parts = []
    partsList = getPartsList(url)
    for piece in partsList['results']:
        parts.append(piece['part']['part_num'])
    print("Parts from Rebrickable api received.")
    return parts

def makeLDRDrawfile(setNo):
    # Create SetNo folder
    if not os.path.exists(setNo):
        os.makedirs(setNo)
        print("Created folder: " + setNo)

    # Create image folder
    imagesfolder = os.path.join(setNo,"unlabeled_images")
    if not os.path.exists(imagesfolder):
        os.makedirs(imagesfolder)
        print("Created folder: " + imagesfolder)


    filename = os.path.join(setNo, setNo + ".ldr")
    LDRAW_file = open(filename,"w")
    parts = partsImportLDRAW(setNo)
    partscounter = 0
    for piece in parts:
        line = '1 4 0 0 0 1 0 0 0 1 0 0 0 1 ' + str(piece) + '.dat'
        LDRAW_file.write(line)
        LDRAW_file.write("\n")
        partscounter += 1
    LDRAW_file.close()
    print("Created File " + filename + " with " + str(partscounter) + " different parts\n")

def run():
    parser = argparse.ArgumentParser(description='Writes a file with included LDRAW parts for a given SetNo')
    parser.add_argument('-s','--setNo', help='SetNo the LDRAW-file is created for.', required=True)
    args = vars(parser.parse_args())
    makeLDRDrawfile(args['setNo'])


run()