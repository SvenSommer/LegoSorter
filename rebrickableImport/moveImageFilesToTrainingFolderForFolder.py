
#usage 
import os
import argparse
from shutil import copyfile

FRAMECOUNT = 25
imagecounter = 0

def readLabel_ids(sourcefolder):
    with open("./"+ sourcefolder +"/" + sourcefolder +".ldr") as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x[28:-5].strip() for x in content] 
    return content

def getImages(sourcefolder):
    fileNames = [fileName for fileName in os.listdir("./"+ sourcefolder +"/unlabeled_images") if fileName.endswith(".png")]
    fileNames.sort()
    return fileNames

def moveImages(sourcefolder, destinationfolder, label, imageFiles, framecount,labelscount):
    global imagecounter
    #create sourcefolder if not exisiting
    newsourcefolder = os.path.join(destinationfolder,label) 
    sourcefolder_existed = 1
    if not os.path.exists(newsourcefolder):
        print("    Creating sourcefolder: " + newsourcefolder)
        os.makedirs(newsourcefolder)
        sourcefolder_existed = 0
    for _ in range(framecount):
        #save the next x files into the label-sourcefolder corresponding to this image
        try:
            filefrom = os.path.join("./"+ sourcefolder +"/unlabeled_images",imageFiles[imagecounter])
            fileto = os.path.join(newsourcefolder, label + "_" + imageFiles[imagecounter])
            #print("moving file: " +  filefrom + " to \n" + fileto)
            if sourcefolder_existed == 0:
                copyfile(filefrom, fileto)
            else:
                print("    sourcefolder '" + newsourcefolder + "' already existed, will not copy file.\n") 
            #os.rename(filefrom,fileto)
                
            imagecounter += 1
        except IndexError:
            print("WARNING: Not enough images in the sourcefolder to copy. Only found " + str(imagecounter) + " but exspected " + str(framecount * labelscount-1) + "!\n" )
            return 0

def run():
    parser = argparse.ArgumentParser(description='Moves files from a specific set into the subsourcefolders of the training_images sourcefolder')
    parser.add_argument('-s','--source', help='sourcefolder the images come from.', required=True)
    parser.add_argument('-d','--destination', help='destinationfolder the images are written to.', required=True)
    args = vars(parser.parse_args())
    sourcefolder = args['source']
    destinationfolder = args['destination']

    imageFiles = getImages(sourcefolder)
    labels = readLabel_ids(sourcefolder)

    # First part has one picture less
    moveImages(sourcefolder, destinationfolder, labels[0], imageFiles, FRAMECOUNT-1, len(labels))
    sourcefoldercounter = 1
    for label in labels[1:]:
        print("\n" + str(sourcefoldercounter) + ". Moving " + str(FRAMECOUNT) + " images from partno " + label)
        ret = moveImages(sourcefolder, destinationfolder, label, imageFiles, FRAMECOUNT, len(labels))
        sourcefoldercounter =  sourcefoldercounter + 1
        if ret == 0:
            break


run()
