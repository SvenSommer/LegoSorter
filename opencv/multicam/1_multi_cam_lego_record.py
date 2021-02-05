# import the necessary packages
from __future__ import print_function
from partsdetectorbriocam import PartsDetectorBrioCam
from partsdetectorusbcam import PartsDetectorUsbCam
from models.controllegosorter import Controllegosorter
from video.videostream import VideoStream
from models.sqlmodel import SQLModel
from models.part import Part

import datetime
import imutils
import time
import cv2
import argparse
import os

def downscale_preview(frame):
	return imutils.resize(frame, int(frame.shape[1]/2))

def deleteFile(filename):
	if os.path.exists(filename):
		os.remove(filename)

def init():
	deleteFile(filenameBrio)
	deleteFile(filenameUSB)
	global total, downsampling 
	total = 0
	downsampling = 2

	ap = argparse.ArgumentParser()
	return vars(ap.parse_args())

filenameBrio = 'outputUSB.avi'
filenameUSB = 'outputBrio.avi'
camMotionUSB = PartsDetectorUsbCam(1,  "", filenameUSB)
camMotionBRIO = PartsDetectorBrioCam(1, "", filenameBrio)
control = Controllegosorter
args = init()

print("[INFO] starting cameras...!")
webcamBRIO = VideoStream(src=2).start()
webcamUSB = VideoStream(src=0).start()

fourcc = cv2.VideoWriter_fourcc(*'XVID')
outBrio = cv2.VideoWriter(filenameBrio,fourcc, 30.0, (1920,1080))
outUSB = cv2.VideoWriter(filenameUSB, fourcc, 30.0, (4096,2160))

write = False
#control.startLegoSorter(2.0,speedconveyor = 5)
while True:
	frames = []

	for (stream, partdetector) in zip((webcamBRIO, webcamUSB), (camMotionUSB, camMotionBRIO)):
		frame = stream.read()

		if total < 32:
			frames.append(frame)
			total += 1
			continue
		frames.append(frame)

	

	for (frame, name, out) in zip(frames, (filenameUSB, filenameBrio), (outUSB, outBrio)):
		
		if write:
			out.write(frame)
		cv2.imshow(name, downscale_preview(frame))

	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
	if key == ord("w"):
		write = True

	 # White Balancing
	if key == ord('o'):
		webcamBRIO.stream.set(cv2.CAP_PROP_AUTO_WB,0)
		whiteb = "OFF"
	if key == ord('p'):
		webcamBRIO.stream.set(cv2.CAP_PROP_AUTO_WB,1)
		webcamBRIO.stream.set(cv2.CAP_PROP_WB_TEMPERATURE,4230)
	
	
	# White Balancing
	if key == ord('k'):
		webcamUSB.stream.set(cv2.CAP_PROP_AUTO_WB,0)
		whiteb = "OFF"

	if key == ord('l'):
		webcamUSB.stream.set(cv2.CAP_PROP_AUTO_WB,1)

# do a bit of cleanup
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
webcamBRIO.stop()
webcamUSB.stop()
control.stopLegoSorter(2.0)