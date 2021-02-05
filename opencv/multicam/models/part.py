import time
from datetime import datetime
from concurrent.futures import as_completed
from collections import Counter


class Part(object):
   def __init__(self, sql, filewriter, controllegosorter, predictController, colorid=0):
      self.sql = sql
      self.filewriter = filewriter
      self.controllegosorter = controllegosorter
      self.predictController = predictController
      self.partid = sql.InsertIntoRecognisedParts()
      
      self.partimages = []
      self.lastseen = None
      self.isPushed = False
      self.predictionRequests = []
      self.predictedPartnos = []
      self.numberOfPredictions = 0
      self.lastpredictionTimestamp = None
      self.partno = None
      self.colorid = colorid
      self.setno = None
      self.weight = 0
      self.bucket = 0
      self.removedimagecounter = 0
      # prediction turned off
      self.numberOfPredirctionsToExecute = 0
      self.minimumSecondsBetweenPredictions = 1

   def addPartimage(self, image):
      self.partimages.append(image)
   
   def saveAndPredictImage(self, image, write):
      if write:
         if self.lastpredictionTimestamp is None:
            self.lastpredictionTimestamp = time.time()-1

         timediff = time.time() - self.lastpredictionTimestamp
         if timediff < self.minimumSecondsBetweenPredictions: 
            return

         imagepath, ts =  self.filewriter.writePartimage(image, str(self.partid))
         # prediction turned off
         # self.predictPart(imagepath, image)

         imageid =  self.sql.InsertIntoPartimages(imagepath, image, ts)
         self.sql.InsertIntoRecognisedImages(self.partid,imageid)
         
   def predictPart(self, imagepath, image):
      if self.numberOfPredictions <= self.numberOfPredirctionsToExecute:
         request = self.predictController.predictPartno(imagepath)
         self.predictionRequests.append(request)
         print(f"{self.getTime()} {self.partid} Added Request for image {self.numberOfPredictions}. Camera {image.camera}")
         self.numberOfPredictions = self.numberOfPredictions + 1
      else:
         print(f"{self.getTime()} {self.partid} Skipping Predictions. Already {self.numberOfPredirctionsToExecute} done.")

   def getBucketDistance(self, bucketnumber):
      if bucketnumber == 1 or bucketnumber == 2:
         return 8600.0
      elif bucketnumber == 3 or bucketnumber == 4:
         return 8900.0
      elif bucketnumber == 5 or bucketnumber == 6:
         return 9200

   def getBucketTravelTimes(self, bucketnumber):
      if bucketnumber == 1 or bucketnumber == 2:
         return 3150
      elif bucketnumber == 3 or bucketnumber == 4:
         return 4000
      elif bucketnumber == 5 or bucketnumber == 6:
         return 5000

   def calculateTravelTime(self, bucketnumber):
      brioimages = []
      if len(self.partimages) <= 1:
        # print("partimages <= 1 : " + str(len(self.partimages)))
         return 0,0

      for image in self.partimages:
        # print("image.camera : " + str(image.camera))
         if image.camera == "BRIO_center":
            brioimages.append(image)

      if len(brioimages) <= 1:
        # print("brioimages <= 1 : " + str(len(brioimages)))
         return 0,0

      firstimage = brioimages[0]
      lastimage = brioimages[-1]
      timedelta = lastimage.timestamp - firstimage.timestamp
      print("timedelta:\t" + str(timedelta))
      lastseen = lastimage.timestamp
      print("lastseen:\t" + str(lastseen))
      distance = lastimage.cy - firstimage.cy
      print("distance:\t" + str(distance))
      speed = distance / timedelta
      print("speed:\t" + str(speed))
      bucketdistance = self.getBucketDistance(bucketnumber)
      print("bucketdistance:\t" + str(bucketdistance))
      traveltime = int(bucketdistance/speed)
      return traveltime

   def sendPushSignal(self, bucketnumber):
      
      traveltime = self.getBucketTravelTimes(bucketnumber) # Bucket 3 & 4 Conveyor 29
      if traveltime is None:
         traveltime = 3000
      print(f"{self.getTime()} {self.partid} traveltime:\t" + str(traveltime))
      pushtime = int(round(time.time() * 1000)) + traveltime
      
      print(f"{self.getTime()} {self.partid} pushtime:\t" + str(pushtime))
      self.controllegosorter.pushBrick(self.partid, bucketnumber, pushtime, self.weight, 200)      

   def pushPart(self):
      # Find most common brickid in predictedPartnos
      print(f"{self.getTime()} {self.partid} Waiting for predictions....")
      for request in as_completed(self.predictionRequests):
         self.predictedPartnos.append(request.result().json().get("predict_partno"))

      if len(self.predictedPartnos) >= self.numberOfPredirctionsToExecute:
         print(f"{self.getTime()} {self.partid} predictedPartnos: " + ' '.join(str(x) for x in self.predictedPartnos))
         # prediction turned off
         #predictedPartno = self.most_common(self.predictedPartnos)
         predictedPartno = 1200
         self.bucket = 2
         #bug: most common if there are all different
         print(f"{self.getTime()} {self.partid} most common predictedPartno: {predictedPartno}" )

         if (self.isPushed == False): 
            self.sendPushSignal(self.bucket)
            self.isPushed = True

   def most_common(self, lst):
      data = Counter(lst)
      return data.most_common(1)[0][0] 

   def getTime(self):
      return datetime.now()