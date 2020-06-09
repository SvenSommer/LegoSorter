import os
import argparse
from shutil import copyfile

#LDR_FILE = "./"+ folder +"/LDRAW_file_7633.ldr"
#IMAGE_FILE_DIRECTORY = "./"+ folder +"/unlabeled_images"
FRAMECOUNT = 25
TRAINING_DIR =  './../training_images_all'
imagecounter = 0

def readLabel_ids(folder):
    with open("./"+ folder +"/" + folder +".ldr") as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x[28:-5].strip() for x in content] 
    return content

def getImages(folder):
    fileNames = [fileName for fileName in os.listdir("./"+ folder +"/unlabeled_images") if fileName.endswith(".png")]
    fileNames.sort()
    return fileNames

def moveImages(folder, label, imageFiles, framecount,labelscount):
    global imagecounter
    #create folder if not exisiting
    newfolder = os.path.join(TRAINING_DIR,label) 
    folder_existed = 1
    if not os.path.exists(newfolder):
        print("    Creating Folder: " + newfolder)
        os.makedirs(newfolder)
        folder_existed = 0
    for _ in range(framecount):
        #save the next x files into the label-folder corresponding to this image
        try:
            filefrom = os.path.join("./"+ folder +"/unlabeled_images",imageFiles[imagecounter])
            fileto = os.path.join(newfolder, label + "_" + imageFiles[imagecounter])
            #print("moving file: " +  filefrom + " to \n" + fileto)
            if folder_existed == 0:
                copyfile(filefrom, fileto)
            else:
                print("    Folder '" + newfolder + "' already existed, will not copy file.\n") 
            #os.rename(filefrom,fileto)
                
            imagecounter += 1
        except IndexError:
            print("WARNING: Not enough images in the folder to copy. Only found " + str(imagecounter) + " but exspected " + str(framecount * labelscount-1) + "!\n" )
            return 0

def run():
    parser = argparse.ArgumentParser(description='Moves files from a specific set into the subfolders of the training_images folder')
    parser.add_argument('-f','--folder', help='folder the images needs to be labeled', required=True)
    args = vars(parser.parse_args())
    folder = args['folder']

    imageFiles = getImages(folder)
    labels = readLabel_ids(folder)

    # First part has on epicture less
    moveImages(folder, labels[0], imageFiles, FRAMECOUNT-1, len(labels))
    foldercounter = 1
    for label in labels[1:]:
        print("\n" + str(foldercounter) + ". Moving " + str(FRAMECOUNT) + " images from partno " + label)
        ret = moveImages(folder, label, imageFiles, FRAMECOUNT, len(labels))
        foldercounter =  foldercounter + 1
        if ret == 0:
            break


run()
