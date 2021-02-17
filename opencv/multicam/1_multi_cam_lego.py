# import the necessary packages
from __future__ import print_function
from requests_futures.sessions import FuturesSession
from partsdetectorbriocam import PartsDetectorBrioCam
from partsdetectorusbcam import PartsDetectorUsbCam

from video.videostream import VideoStream
from video.filevideostream import FileVideoStream

from models.sqlmodel import SQLModel
from models.part import Part
from models.filewriter import FileWriter
from models.controllegosorter import Controllegosorter
from models.predictcontroller import PredictController

from datetime import datetime
import imutils
import time
import cv2
import argparse

learningRateBrio = 0.01
write = True
debug = True
downsampling = 4
preview_downscaling = 2

def init():
	global total
	total = 0
	

	ap = argparse.ArgumentParser()
	ap.add_argument("-rf", "--read_folder", help="Source folder for videos")
	ap.add_argument("-w", "--write", help="write found images")
	ap.add_argument("-cmax", "--countmax", type=int, default=500, help="maximum images to write")
	ap.add_argument("-b", "--boxes", help="show boxes in images")
	ap.add_argument("-r", "--run", help="run LegoSorter")
	ap.add_argument("-wf", "--write_folder", help="folder the images are written to go", default="/home/robert/LegoSorter/partimages/")
	ap.add_argument("-id", "--run_id", help="run_id", required=True)
	
	return vars(ap.parse_args())


args = init()
readfolder = args["read_folder"]
webcamBRIO = None
webcamUSB = None
FileMode = False
readNextFrame = False
print("readfolder: " + str(readfolder))

if readfolder is not None :
	webcamBRIO = FileVideoStream('outputBrio_example1.avi').start()
	webcamUSB = FileVideoStream('outputUSB_example1.avi').start()
	FileMode = True
	print("[INFO] reading files...!")

else:
	webcamBRIO = VideoStream(src=2).start()
	webcamUSB = VideoStream(src=0).start()
	readNextFrame = True
	print("[INFO] starting cameras...!")
print("FileMode: " + str(FileMode))


run_id = int(args["run_id"])
folder = args["write_folder"]

camMotionUSB = PartsDetectorUsbCam(run_id,  folder,"USB", saturation=30, debug = debug, downsampling = downsampling, writeImages = write, learningRate = 0.01)
camMotionBRIO = PartsDetectorBrioCam(run_id, folder,"BRIO", saturation=20, debug = debug, downsampling = downsampling,  writeImages = write, learningRate = learningRateBrio)
sql = SQLModel(run_id)
filewriter = FileWriter(write, folder)
futureSession = FuturesSession()
control = Controllegosorter(futureSession)
predict = PredictController(futureSession)

if FileMode is False:
	control.startConveyor()
camMotionBRIO.warmup(webcamBRIO)

def downscale_preview(frame, cameraname, downscaling):
	if cameraname == "USB":
		return imutils.resize(frame, int(frame.shape[1]/downscaling))
	elif cameraname == "BRIO":
		return imutils.resize(frame, int(frame.shape[1]/(downscaling*2)))

def drawobjectInfo(frame, objectID, centroid) :
	text = "ID " + format(objectID) + " color " + format(centroid[6])
	cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
	cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
	return frame

objectids = []	
currentPart = None
overallimagecounter = 0

innercounter = 0
if FileMode is False:
	control.startLegoSorter()
while True:
	frames = []

	for (stream, partdetector) in zip((webcamUSB, webcamBRIO), (camMotionUSB, camMotionBRIO)):
		if readNextFrame or total < 4 or FileMode is False:
			frame = stream.read()
			if frame is None:
				continue
			innercounter += 1
			if innercounter == 2:
				total += 1
				readNextFrame = False
				innercounter = 0
				overallimagecounter += 1
			
			if total < 4:
				frames.append(downscale_preview(frame,partdetector.getCameraName(), preview_downscaling))
				total += 1
				continue
			
			frame, partimages = partdetector.getPartimages(frame)

			objects = partdetector.trackObjects(partimages)

			if(len(objects) > 0):
				# loop over the tracked objects
				for (objectID, centroid) in objects.items():
					# check if an object with this objectid is already existing
					if objectID not in objectids:
						objectids.append(objectID)
						
						if currentPart is None:
							currentPart = Part(sql, filewriter,control, predict, centroid[6])
						#check if the currentpart had already images, before creating a new "empty" one
						elif len(currentPart.partimages) != 0:
							# create an new part
							print("__________________________________")
							print(f"{datetime.now()} New Part detected...")
							currentPart = Part(sql, filewriter, control, predict, centroid[6])
							print(f"{datetime.now()} Created new Partid " + format(currentPart.partid))
							if FileMode is False:
								control.haltSupplyChain()
							
							
					# draw both the ID of the object and the centroid of the
					# object on the output frame
					if debug:
						frame = drawobjectInfo(frame, currentPart.partid, centroid)	
			
			
			if currentPart is not None:
				if len(partimages) > 0:
					for image in partimages:
						if overallimagecounter > (20):
							frame, checkresult = partdetector.checkImage(image, frame)
							if checkresult == 1:
								currentPart.addPartimage(image)
								currentPart.saveAndPredictImage(image, write) 
							elif checkresult ==2:
								if FileMode is False:
									currentPart.pushPart()
									control.resumeSupplyChain()
			if debug:			
				cv2.putText(frame, "Frame: " + str(total) + ", oc: " + str(overallimagecounter), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
				if currentPart is not None:
					cv2.putText(frame, "Part: " + str(currentPart.partid), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)			
				frame = partdetector.drawTreshholds(frame)

			frames.append(downscale_preview(frame,partdetector.getCameraName(), preview_downscaling))
			
			
		else:
			continue
		
	for (frame, name) in zip(frames, ("webcamUSB", "webcamBRIO")):
			cv2.imshow(name, frame)

	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

	if FileMode and total < 50:
		readNextFrame = True

	if key == ord("r") and FileMode:
		readNextFrame = True


# do a bit of cleanup
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
webcamBRIO.stop()
webcamUSB.stop()
if FileMode is False:
	control.stopLegoSorter(2.0)