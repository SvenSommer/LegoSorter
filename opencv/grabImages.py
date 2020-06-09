# USAGE
# python videostream_demo.py
# python videostream_demo.py --picamera 1

# import the necessary packages
from ownmutils.imutils.video import VideoStream
import datetime
import argparse
from ownmutils import imutils
from ownmutils.imutils.video import FPS
import time
import argparse
import cv2
import numpy as np

ap = argparse.ArgumentParser()

count = 0
fgbg = cv2.createBackgroundSubtractorMOG2()

ap.add_argument("-w", "--write", help="write found images")
ap.add_argument("-cmax", "--countmax", type=int, default=500, help="maximum images to write")
args = vars(ap.parse_args())

def apply_mask1(frame):
	mask = np.zeros(frame.shape, dtype=np.uint8)

	roi_corners = np.array([[(750,210),(1000,730), (0,800), (250,210)]], dtype=np.int32)
	# fill the ROI so it doesn't get wiped out when the mask is applied
	channel_count = frame.shape[2]  # i.e. 3 or 4 depending on your image
	ignore_mask_color = (255,)*channel_count
	cv2.fillPoly(mask, roi_corners, ignore_mask_color)

	# apply the mask
	frame = cv2.bitwise_and(frame, mask)
	return frame

def apply_mask2(frame):
	mask = np.zeros(frame.shape, dtype=np.uint8)

	roi_corners = np.array([[(780,60),(750,580),(330,580), (280,60)]], dtype=np.int32)
	# fill the ROI so it doesn't get wiped out when the mask is applied
	channel_count = frame.shape[2]  # i.e. 3 or 4 depending on your image
	ignore_mask_color = (255,)*channel_count
	cv2.fillPoly(mask, roi_corners, ignore_mask_color)

	# apply the mask
	frame = cv2.bitwise_and(frame, mask)
	return frame

def write_timestamp(frame, timestamp):
	ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
	cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)

	return frame

def detectmotion(run,cam, frame, fFrame, minarea, timestamp):
	global count
	global args
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	greenMask = cv2.inRange(hsv, (26, 10, 30), (255, 255, 255))

	hsv[:,:,1] = greenMask 

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)


	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(fFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	# loop over the contours

	for c in cnts:
			# if the contour is too small, ignore it
			if cv2.contourArea(c) < minarea:
					continue
			# compute the bounding box for the contour, draw it on the frame,
			# and update the text
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			if args.get("write", None) is None:
				continue
			else:
				# save the current image of the box
				if not cv2.imwrite(("/home/robert/LegoSorter/partimages/r_" + run +  "image_%d.jpg" % count), frame[y:y+h,x:x+w]):
						raise Exception("Could not write images")   
				count += 1
	return frame

# initialize the video stream and allow the cammera sensor to warmup
vs1 = VideoStream(0).start()
#vs2 = VideoStream(2).start()

time.sleep(2.0)
fps = FPS().start()

frame1 = vs1.read()
#frame1 = imutils.resize(frame1, width=500)
frame1 = imutils.rotate(frame1,90)
frame1 = apply_mask1(frame1)
# if the first frame is None, initialize it
gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (21, 21), 0)
firstFrame1 = gray
# if the average frame is None, initialize it

#frame2 = vs2.read()
#frame2 = apply_mask2(frame2)
# if the first frame is None, initialize it
#gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
#gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)
#firstFrame2 = gray2

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame1 = vs1.read()
	if frame1 is None:
		break
	#frame1 = imutils.resize(frame1, width=500)
	frame1 = imutils.rotate(frame1,90)
	timestamp = datetime.datetime.now()

	frame1 = apply_mask1(frame1)
	frame1 = write_timestamp(frame1, timestamp)
	frame1 = detectmotion("1", "cam1", frame1, firstFrame1, 500, timestamp)

	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	#frame2 = vs2.read()
	#if frame2 is None:
	#	break

	#frame2 = apply_mask2(frame2)
	#frame2 = write_timestamp(frame2, timestamp)
	#frame2 = detectmotion("1", "cam2", frame2, firstFrame2, 300, timestamp)

	# show the frame
	cv2.imshow("Cam 1", frame1)
	#cv2.imshow("Cam 2", frame2)
	fps.update()

	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		fps.stop()
		print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
		print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
		break

	if count > args["countmax"]:

		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs1.stop()
#vs2.stop()