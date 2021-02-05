import os
import math

PARTS_PER_FILE = 200 

def getPartNames(folder):
    fileNames = [fileName for fileName in os.listdir(folder) if fileName.endswith(".dat")]
    fileNames.sort()
    return fileNames

def makeLDRDrawfile(folder):
    parts = getPartNames("./parts")
    
    partlists = divide_chunks(parts,PARTS_PER_FILE)
    filecounter = 1
    totalfilenumber = math.ceil(len(parts)/PARTS_PER_FILE)
    print("Will write " + str(totalfilenumber) + " files in batches of " + str(PARTS_PER_FILE) +" parts per file.")
    for partlist in partlists:
        writeFileWithParts(partlist, filecounter, totalfilenumber)
        filecounter += 1

def divide_chunks(partlist, n):   
    for i in range(0, len(partlist), n):  
        yield partlist[i:i + n] 

def writeFileWithParts(parts, actualfilenumber, totalfilenumber):
     # Create subfolder
    subfoldername = "unlabeled_parts_" + str(actualfilenumber) + "_of_" + str(totalfilenumber)
    if not os.path.exists(subfoldername):
        os.makedirs(subfoldername)
        print("Created folder: " + subfoldername)

    # Create image folder
    imagesfolder = os.path.join(subfoldername,"unlabeled_images")
    if not os.path.exists(imagesfolder):
        os.makedirs(imagesfolder)
        print("Created folder: " + imagesfolder)

    filename =  os.path.join(subfoldername, "unlabeled_parts_" + str(actualfilenumber) + "_of_" + str(totalfilenumber) + ".ldr")
    LDRAW_file = open(filename,"w")
    partscounter = 0
    for piece in parts:
        line = '1 9 0 0 0 1 0 0 0 1 0 0 0 1 ' + str(piece)
        LDRAW_file.write(line)
        LDRAW_file.write("\n")
        partscounter += 1
    LDRAW_file.close()
    print("Created File " + filename + " with " + str(partscounter) + " different parts\n")

def run():
    makeLDRDrawfile("./parts")

run()