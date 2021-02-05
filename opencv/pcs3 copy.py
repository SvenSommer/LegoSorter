from ownmutils.imutils.video import VideoStream
import datetime
import argparse
from ownmutils import imutils
from ownmutils.imutils.video import FPS
import time
import argparse
import cv2
import numpy as np
import requests
import os
import pymysql

def nothing(x):
  pass

ap = argparse.ArgumentParser()

count = 1
filecounter = 0
minArea = 500
saturation = 120
min_sharpness =  200
downsampling = 2
additional_box_size= 10
fgbg = cv2.createBackgroundSubtractorMOG2()


def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()

def detectmotion(frame):
	saturation=cv2.getTrackbarPos("Saturation", "Thresholds")
	# saturate - to get the background suptractor look more for color than for brightnesss
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	h, s, v = cv2.split(hsv)
	s += saturation # 5
	final_hsv = cv2.merge((h, s, v))
	saturated_frame = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
	cv2.imshow("saturated_frame", saturated_frame)
	# Mog2 background substraction
	saturated_frame = fgbg.apply(saturated_frame)

	# morph - eleminate noise
	# Denoising
	kernel = np.ones((5,5), np.uint8) 
	denoised_frame = cv2.erode(saturated_frame, kernel, iterations=1) 
	denoised_frame = cv2.dilate(denoised_frame, kernel, iterations=1) 
	cv2.imshow("denoised_frame", denoised_frame)
	contours, _ = cv2.findContours(denoised_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	return contours


part_id = 1
newPartCounter = 1
x_last = y_last = w_last = h_last = ts_last = None


def detectPartFromImageAndSave(partimage, color, x, y, w, h):
	global part_id, newPartCounter, count, x_last, y_last, w_last, h_last, ts_last, args
	ts = time
	st = ts.strftime('%Y-%m-%d %H:%M:%S')
	# init if not set
	if x_last is None:
		x_last = x
		y_last = y
		w_last = w
		h_last = h
		ts_last = ts.time()
		part_id = InsertIntoRecognisedParts()

	# calculate the difference of current parameters to parameters of last image
	x_diff = x - x_last
	y_diff = y - y_last
	#w_diff = w - w_last
	#h_diff = h - h_last
	#ts_diff = ts.time() - ts_last
	

	if y_diff > 100:
		print("y_diff = " + str(y_diff) + " > 100 -> cancel image" )
		return

	# decide if deviation is to big, so it's probably a different part
	if y_diff < -25:
		#print("y_diff = " + str(y_diff) + " < -25 -> new Part")
		part_id = InsertIntoRecognisedParts()
		newPartCounter += 1
	elif abs(x_diff) > 150 :
		#print("abs(x_diff) = " + str(abs(x_diff)) + " > 150 -> new Part")
		part_id = InsertIntoRecognisedParts()
		newPartCounter += 1

	# Done- Set variables for next image
	x_last = x
	y_last = y
	w_last = w
	h_last = h
	ts_last = ts.time()

	st = ts.strftime('%Y-%m-%d %H:%M:%S')
	#Write file in folder
	filename = (args["folder"] + "/"+ str(part_id) + "_" + str(count) + "_" + str(st).replace(":","_").replace(" ","_") + "_x" + str(x) + "_y" + str(y) + ".jpg")
	
	if not cv2.imwrite(filename,partimage):
		raise Exception("Could not write image " + filename) 
	else:
		count += 1
		# save imagespecs in Partimages-Table
		image_id = InsertIntoPartimages(filename,color, x, y, w, h, ts)
		#print("image_id:" + str(image_id))
		#print("filename " + filename)
		#print("x_diff: " + str(x_diff)  + "\n" 	+ "y_diff: " + str(y_diff)  + "\n" 	+ "w_diff: " + str(w_diff) + "\n"	+ "h_diff: " + str(h_diff) + "\n"	+ "ts_diff: " + str(ts_diff) + "\n")
		# Write a Line in RecognisedImages with the current Part_id
		InsertIntoRecognisedImages(part_id,image_id)


# initialize the video stream and allow the cammera sensor to warmup
vs1 = VideoStream(0).start()
if args.get("run", None) is not None:
	startLegoSorter()
time.sleep(2.0)

fps = FPS().start()
# loop over the frames from the video stream
while True:
	frame1 = vs1.read()
	nowTime = time.time()

	frame1 = frame1[0:1080,800:1280]
	if frame1 is None:
		break
	frame1 = imutils.rotate_bound(frame1,-90) # comment this out -  brings 30 fps
	original_frame1 = np.asarray(frame1)
	small_frame1 = imutils.resize(frame1, int(frame1.shape[1]/downsampling))


	#small_frame1 = apply_mask1(small_frame1)
	cnts = detectmotion(small_frame1)
	#cnts = checkcontours(cnts,small_frame1)

	for c in cnts:
			# Ignore the first whole picture
			if cv2.contourArea(c) > 150000:
				continue
			# compute the bounding box for the contour, draw it on the frame,
			# and update the text
			(x, y, w, h) = cv2.boundingRect(c)
			x = x * downsampling
			y = y * downsampling
			w = w * downsampling
			h = h * downsampling
			if args.get("boxes", None) is not None:
				if cv2.contourArea(c) > minArea:
					cv2.rectangle(original_frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
				else:
					cv2.rectangle(original_frame1, (x, y), (x + w, y + h), (0, 0, 255), 1)

			if args.get("write", None) is None:
				continue
			else:
				partimage = original_frame1[y:y+h,x:x+w] 
				gray = cv2.cvtColor(partimage, cv2.COLOR_BGR2GRAY)
				fm = variance_of_laplacian(gray)
				if fm < min_sharpness:
					continue
				if cv2.contourArea(c) > minArea:
					partimage = original_frame1[y:y+h,x:x+w]
					
					# save the current image of the box
					detectPartFromImageAndSave(partimage,color, x, y, w, h)
					
	# show the frame
	cv2.imshow("Cam 1", original_frame1)
	fps.update()

	key = cv2.waitKey(20) & 0xFF
	if key == ord("q"):
		fps.stop()
		print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
		print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
		break

	if newPartCounter > args["countmax"]:
		fps.stop()
		print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
		print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
		break
		

# do a bit of cleanup
if args.get("run", None) is not None:
	stopLegoSorter()

cv2.destroyAllWindows()
vs1.stop()
connection.close()
#vs2.stop()