from models.partimage import Partimage
from models.sqlmodel import SQLModel
import time
import cv2

class DetectPartsFromImages:
    def __init__(self, run_id, folder, writeImages = False):
        self.run_id = run_id
        self.folder = folder
        self.writeImages = writeImages
        self.newPartCounter = 1
        self.count = 1
        self.x_last = None
        self.y_last = None
        self.w_last = None
        self.h_last = None
        self.ts_last = None
        self.part_id = None
        self.sql = SQLModel(run_id)


    def detect(self, partimage):
        ts = time
        st = ts.strftime('%Y-%m-%d %H:%M:%S')
        # init if not set
        if self.x_last is None:
            self.x_last = partimage.x
            self.y_last = partimage.y
            self.w_last = partimage.w
            self.h_last = partimage.h
            self.ts_last = ts.time()
            self.part_id = self.sql.InsertIntoRecognisedParts()
        
        # calculate the difference of current parameters to parameters of last image
        x_diff = partimage.x - self.x_last
        y_diff = partimage.y - self.y_last

        if y_diff > 100:
            print("y_diff = " + str(y_diff) + " > 100 -> cancel image" )
            return
        
        # decide if deviation is to big, so it's probably a different part
        if y_diff < -25:
            #print("y_diff = " + str(y_diff) + " < -25 -> new Part")
            if self.writeImages:
                self.part_id =  self.sql.InsertIntoRecognisedParts()
            self.newPartCounter += 1
        elif abs(x_diff) > 150 :
            #print("abs(x_diff) = " + str(abs(x_diff)) + " > 150 -> new Part")
            if self.writeImages:
                self.part_id =  self.sql.InsertIntoRecognisedParts()
            self.newPartCounter += 1
        
        # Done- Set variables for next image
        self.x_last = partimage.x
        self.y_last = partimage.y
        self.w_last = partimage.w
        self.h_last = partimage.h
        self.ts_last = ts.time()

        st = ts.strftime('%Y-%m-%d %H:%M:%S')
        #Write file in folder
        filename = (self.folder+ "/"+ str(self.part_id) + "_" + str(self.count) + "_" + str(st).replace(":","_").replace(" ","_") + "_x" + str(partimage.x) + "_y" + str(partimage.y) + ".jpg")
        if self.writeImages:
            if not cv2.imwrite(filename,partimage.image):
                raise Exception("Could not write image " + filename) 
            else:
                self.count += 1
                # save imagespecs in Partimages-Table
                image_id =  self.sql.InsertIntoPartimages(filename,partimage.color, partimage.x, partimage.y, partimage.w, partimage.h, ts)
                #print("image_id:" + str(image_id))
                #print("filename " + filename)
                #print("x_diff: " + str(x_diff)  + "\n" 	+ "y_diff: " + str(y_diff)  + "\n" 	+ "w_diff: " + str(w_diff) + "\n"	+ "h_diff: " + str(h_diff) + "\n"	+ "ts_diff: " + str(ts_diff) + "\n")
                # Write a Line in RecognisedImages with the current Part_id
                self.sql.InsertIntoRecognisedImages(self.part_id,image_id)