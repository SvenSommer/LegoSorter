
import os
import argparse
from shutil import copyfile

#LDR_FILE = "./"+ setNo +"/LDRAW_file_7633.ldr"
#IMAGE_FILE_DIRECTORY = "./"+ setNo +"/unlabeled_images"
FRAMECOUNT = 25
TRAINING_DIR =  './../training_images_all'
imagecounter = 0

def readLabel_ids(setNo):
    with open("./"+ setNo +"/" + setNo +".ldr") as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x[28:-5].strip() for x in content] 
    return content

def getImages(setNo):
    fileNames = [fileName for fileName in os.listdir("./"+ setNo +"/unlabeled_images") if fileName.endswith(".png")]
    fileNames.sort()
    return fileNames

def moveImages(setNo, label, imageFiles, framecount,labelscount):
    global imagecounter
    #create folder if not exisiting
    newfolder = os.path.join(TRAINING_DIR,label) 
    folder_existed = 1
    if not os.path.exists(newfolder):
        print("Creating Folder: " + newfolder + "\n")
        os.makedirs(newfolder)
        folder_existed = 0
    print("moving " + str(framecount) + " images from partno " + label)
    for _ in range(framecount):
        #save the next x files into the label-folder corresponding to this image
        try:
            filefrom = os.path.join("./"+ setNo +"/unlabeled_images",imageFiles[imagecounter])
            fileto = os.path.join(newfolder,imageFiles[imagecounter])
            #print("moving file: " +  filefrom + " to \n" + fileto)
            
            if os.path.getsize(filefrom) > 1945 and folder_existed == 0:
                copyfile(filefrom, fileto)
                #os.rename(filefrom,fileto)
            else:
                print("File '" + filefrom + "' is no valid file and will be ignored.") 
                
            imagecounter += 1
        except IndexError:
            print("Not enough images in the folder to copy. Only found " + str(imagecounter) + " but exspected " + str(framecount * labelscount-1) + "!" )
            return

def run():
    parser = argparse.ArgumentParser(description='Moves files from a specific set into the subfolders of the training_images folder')
    parser.add_argument('-s','--setNo', help='SetNo the images needs to be labeled', required=True)
    args = vars(parser.parse_args())
    setNo = args['setNo']

    imageFiles = getImages(setNo)
    labels = readLabel_ids(setNo)

    # First part has on epicture less
    moveImages(setNo, labels[0], imageFiles, FRAMECOUNT-1, len(labels))

    for label in labels[1:]:
        moveImages(setNo, label, imageFiles, FRAMECOUNT, len(labels))


run()
