# import the necessary packages
from imutils.video import VideoStream
import os
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np

#global variables
path = '/home/robert/LegoSorter/partimages/'
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())
# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
        vs = VideoStream(src=0).start()
        time.sleep(2.0)
# otherwise, we are reading from a video file
else:
        vs = cv2.VideoCapture(args["video"])
# initialize the first frame in the video stream
firstFrame = None
count = 0
print("path:" + path)
# loop over the frames of the video
while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        frame = vs.read()
        frame = frame if args.get("video", None) is None else frame[1]
        text = "Emtpy"
        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if frame is None:
                break
        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        frame = imutils.rotate(frame,90)
       
       
        # mask
        mask = np.zeros(frame.shape, dtype=np.uint8)
        roi_corners = np.array([[(300,10),(490,310), (10,290), (210,10)]], dtype=np.int32)
        # fill the ROI so it doesn't get wiped out when the mask is applied
        channel_count = frame.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,)*channel_count
        cv2.fillPoly(mask, roi_corners, ignore_mask_color)

        # apply the mask
        frame = cv2.bitwise_and(frame, mask)
        
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        greenMask = cv2.inRange(hsv, (26, 10, 30), (255, 255, 255))

        hsv[:,:,1] = greenMask 


        back = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        # if the first frame is None, initialize it
        if firstFrame is None:
                firstFrame = gray
                continue
        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
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
                if cv2.contourArea(c) < args["min_area"]:
                        continue
                # compute the bounding box for the contour, draw it on the frame,
                # and update the text
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # save the current image of the box
                if not cv2.imwrite(('/home/robert/LegoSorter/partimages/legopart%d.jpg' % count), frame[y:y+h,x:x+w]):
                        raise Exception("Could not write images")
                text = "filled"   
                count += 1    
        # draw the text and timestamp on the 

        
        #success,image = vs.read()
        #cv2.putText(frame, "Conveyor Status: {}".format(text), (10, 20),
        #        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        #cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        #        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        # show the frame and record if the user presses a key
        cv2.imshow("Conveyor Feed", frame)
        #cv2.imshow("Thresh", thresh)
        #cv2.imshow("Frame Delta", frameDelta)
        #cv2.imshow('test', back)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
                break
# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()