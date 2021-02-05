import cv2
import time

class FileWriter(object):
   def __init__(self, writeImages, folder):
      self.writeImages = writeImages
      self.folder = folder
      self.count = 0

   def writePartimage(self, partimage, part_id):
      ts = time
      st = ts.strftime('%Y-%m-%d %H:%M:%S')
      #Write file in folder

      filename = (self.folder + "/" + str(part_id) + "_" + str(self.count) + "_" + str(st).replace(":","_").replace(" ","_") + "_x" + str(partimage.x) + "_y" + str(partimage.y) + "_" + partimage.camera + ".jpg")
      if self.writeImages:
         if not cv2.imwrite(filename,partimage.image):
            raise Exception("Could not write image " + filename) 
         else:
            self.count += 1
            return filename, ts
           