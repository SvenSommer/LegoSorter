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
import requests

ap = argparse.ArgumentParser()

count = 0
filecounter = 0
numberignoredpictures = 1
minArea = 400
downsampling = 5
fgbg = cv2.createBackgroundSubtractorMOG2()

ap.add_argument("-w", "--write", help="write found images")
ap.add_argument("-cmax", "--countmax", type=int, default=500, help="maximum images to write")
ap.add_argument("-b", "--boxes", help="shoew boxes in images")
args = vars(ap.parse_args())

def apply_mask1(frame):
	mask = np.zeros(frame.shape, dtype=np.uint8)

	roi_corners = np.array([[(750/downsampling,210/downsampling),(1000/downsampling,730/downsampling), (0/downsampling,800/downsampling), (250/downsampling,210/downsampling)]], dtype=np.int32)
	# fill the ROI so it doesn't get wiped out when the mask is applied
	channel_count = frame.shape[2]  # i.e. 3 or 4 depending on your image
	ignore_mask_color = (255,)*channel_count
	cv2.fillPoly(mask, roi_corners, ignore_mask_color)

	# apply the mask
	frame = cv2.bitwise_and(frame, mask)
	return frame

def startLegoSorter():
	requests.put('http://conveyorcontroller/update?clientmode=SCRIPT&motormode=ON&speed=30')
	time.sleep(2.0)
	requests.put('http://vibrationcontroller/update?clientmode=SCRIPT&motormode=ON&speed=30')
	requests.put('http://liftercontroller/update?clientmode=SCRIPT&motormode=ON&speed=10')

def stopLegoSorter():
	requests.put('http://liftercontroller/update?clientmode=SCRIPT&motormode=OFF&speed=10')
	requests.put('http://vibrationcontroller/update?clientmode=SCRIPT&motormode=OFF&speed=30')
	requests.put('http://conveyorcontroller/update?clientmode=SCRIPT&motormode=OFF&speed=30')

def apply_mask2(frame):
	mask = np.zeros(frame.shape, dtype=np.uint8)

	roi_corners = np.array([[(780/downsampling,60/downsampling),(750/downsampling,580/downsampling),(330/downsampling,580/downsampling), (280/downsampling,60/downsampling)]], dtype=np.int32)
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

def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()

def checkcontours(contours,image):
	newcontours = []
	for c in contours:
		include = True  
		# omit this contour if it touches the edge of the image
		x,y,w,h = cv2.boundingRect(c)       
		if x <= 1 or y <=1:
			include = False                 
		if x+w+1 >= image.shape[1] or y+h+1 >= image.shape[0]:
			include = False
		# draw the contour
		if include == True:
			newcontours.append(c)

	return newcontours

def detectmotion(frame):
	# saturate - to get the background suptractor look more for color than for brightnesss
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	h, s, v = cv2.split(hsv)
	s += 60 # 5
	final_hsv = cv2.merge((h, s, v))
	altered_frame = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
	# Mog2 background substraction
	altered_frame = fgbg.apply(altered_frame)

	# morph - eleminate noise
	# Denoising
	kernel = np.ones((5,5), np.uint8) 
	altered_frame = cv2.erode(altered_frame, kernel, iterations=1) 
	altered_frame = cv2.dilate(altered_frame, kernel, iterations=1) 

	_, contours, _ = cv2.findContours(altered_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	return contours

def detectmotion_alt(frame):
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray,(15,15),0)
	lap = cv2.Laplacian(blur,cv2.CV_64F)
	blur = cv2.GaussianBlur(lap,(45,45),0)
	blur[blur<0]=0
	blur = 255.*blur/np.amax(blur)


	cnts,_ = cv2.findContours(blur.astype(np.uint8),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	return cnts

# initialize the video stream and allow the cammera sensor to warmup
vs1 = VideoStream(0).start()
#vs2 = VideoStream(2).start()
#startLegoSorter()
time.sleep(2.0)

fps = FPS().start()

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame1 = vs1.read()
	if frame1 is None:
		break
	frame1 = imutils.rotate(frame1,90) # comment this out -  brings 30 fps
	original_frame1 = np.asarray(frame1)
	small_frame1 = imutils.resize(frame1, int(frame1.shape[1]/downsampling))


	small_frame1 = apply_mask1(small_frame1)
	cnts = detectmotion_alt(small_frame1)
	#cnts = checkcontours(cnts,small_frame1)

	for c in cnts:
			# if the contour is too small, ignore it
			if cv2.contourArea(c) < minArea/downsampling:
				continue
			# compute the bounding box for the contour, draw it on the frame,
			# and update the text
			(x, y, w, h) = cv2.boundingRect(c)
			x = x * downsampling
			y = y * downsampling
			w = w * downsampling
			h = h * downsampling
			if args.get("boxes", None) is not None:
				cv2.rectangle(original_frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
			
			
			if args.get("write", None) is None:
				continue
			else:
				#cherry blurriness of picture
				partimage = original_frame1[y:y+h,x:x+w]
				gray = cv2.cvtColor(partimage, cv2.COLOR_BGR2GRAY)
				fm = variance_of_laplacian(gray)
				if fm < 800:
					continue
					#if not cv2.imwrite(("/home/robert/LegoSorter/partimages/blurred/r_" + "1" +  "image_%d.jpg" % count),partimage):
					#	raise Exception("Could not write images")   
				
				# save the current image of the box
				if filecounter > numberignoredpictures:
					if not cv2.imwrite(("/home/robert/LegoSorter/partimages/r_" + "1" +  "image_%d.jpg" % count),partimage):
							raise Exception("Could not write images")   
					filecounter = 0
				count += 1
				filecounter += 1

	timestamp = datetime.datetime.now()
	original_frame1 = write_timestamp(original_frame1, timestamp)
	# show the frame
	cv2.imshow("Cam 1", original_frame1)
	fps.update()

	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		fps.stop()
		print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
		print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
		break

	if count > args["countmax"]:
		fps.stop()
		print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
		print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
		break

# do a bit of cleanup
#stopLegoSorter()
cv2.destroyAllWindows()
vs1.stop()

#vs2.stop()