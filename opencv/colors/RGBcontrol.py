# import the necessary packages
from collections import deque
import numpy as np
import imutils
import cv2
import sys

#cap = cv2.VideoCapture(4)
#ret, image = cap.read()

masking = True
tracking = False

def nothing(*arg):
    pass


def onMouse(event, x, y, flags, param):
    # grab references to the global variables

    if event == cv2.EVENT_MOUSEMOVE:
        refPt = [(x, y)]
        (blue, green, red) = event[refPt[0]]
        #cv2.setTrackbarPos('mouseOver - red', 'RGB', red)
        #cv2.setTrackbarPos('mouseOver - green', 'RGB', green)
        #cv2.setTrackbarPos('mouseOver - blue', 'RGB', blue)


def setBlue():
    cv2.setTrackbarPos('lower - red', 'RGB', 86)
    cv2.setTrackbarPos('lower - green', 'RGB', 31)
    cv2.setTrackbarPos('lower - blue', 'RGB', 4)
    cv2.setTrackbarPos('upper - red', 'RGB', 246)
    cv2.setTrackbarPos('upper - green', 'RGB', 96)
    cv2.setTrackbarPos('upper - blue', 'RGB', 57)


cv2.namedWindow('RGB')
#cv2.setMouseCallback('RGB', onMouse)
cv2.createTrackbar('lower - red', 'RGB', 0, 255, nothing)
cv2.createTrackbar('lower - green', 'RGB', 0, 255, nothing)
cv2.createTrackbar('lower - blue', 'RGB', 0, 255, nothing)

cv2.createTrackbar('upper - red', 'RGB', 1, 255, nothing)
cv2.createTrackbar('upper - green', 'RGB', 1, 255, nothing)
cv2.createTrackbar('upper - blue', 'RGB', 1, 255, nothing)

#cv2.createTrackbar('mouseOver - red', 'RGB', 0, 255, nothing)
#cv2.createTrackbar('mouseOver - green', 'RGB', 0, 255, nothing)
#cv2.createTrackbar('mouseOver - blue', 'RGB', 0, 255, nothing)

setBlue()
img_counter = 0
if masking:
    while True:
        # Capture frame-by-frame
        #ret, image = cap.read()
        image = cv2.imread('sample_green.png')

        thrs1 = cv2.getTrackbarPos('lower - red', 'RGB')
        #print("thrs1: " + str(thrs1))
        thrs2 = cv2.getTrackbarPos('lower - green', 'RGB')
        thrs3 = cv2.getTrackbarPos('lower - blue', 'RGB')
        thrs4 = cv2.getTrackbarPos('upper - red', 'RGB')
        thrs5 = cv2.getTrackbarPos('upper - green', 'RGB')
        thrs6 = cv2.getTrackbarPos('upper - blue', 'RGB')
        #thrs7 = cv2.getTrackbarPos('mouseOver - red', 'RGB')
        #thrs8 = cv2.getTrackbarPos('mouseOver - green', 'RGB')
        #thrs9 = cv2.getTrackbarPos('mouseOver - blue', 'RGB')

        if (thrs1 > thrs4):
            cv2.setTrackbarPos('lower - red', 'RGB', thrs4 - 1)
        if (thrs2 > thrs5):
            cv2.setTrackbarPos('lower - green', 'RGB', thrs5 - 1)
        if (thrs3 > thrs6):
            cv2.setTrackbarPos('lower - blue', 'RGB', thrs6 - 1)

        # define the list of boundaries
        boundaries = [
            ([thrs3, thrs2, thrs1], [thrs6, thrs5, thrs4])
        ]

        # loop over the boundaries
        for (lower, upper) in boundaries:
            # create NumPy arrays from the boundaries
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")

            # find the colors within the specified boundaries and apply
            # the mask
            mask = cv2.inRange(image, lower, upper)
            output = cv2.bitwise_and(image, image, mask=mask)

            imageOut = np.hstack([image, output])

        # Display the resulting frame


        cv2.imshow('RGB', imageOut)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            masking = False
            break
        
        
        if key == ord('s'):
            print("s pressed")
            img_name = "sample_color{}.png".format(img_counter)
            cv2.imwrite(img_name, image)
            print("{} written!".format(img_name))
            img_counter += 1

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if tracking:

    # initialize the list of tracked points, the frame counter,
    # and the coordinate deltas
    linelength = 16
    pts = deque(maxlen=linelength)
    counter = 0
    (dX, dY) = (0, 0)
    direction = ""

    count = 0

    while True:
        # Capture frame-by-frame
        (grabbed, image) = cap.read()

        thrs1 = cv2.getTrackbarPos('lower - red', 'RGB')
        thrs2 = cv2.getTrackbarPos('lower - green', 'RGB')
        thrs3 = cv2.getTrackbarPos('lower - blue', 'RGB')
        thrs4 = cv2.getTrackbarPos('upper - red', 'RGB')
        thrs5 = cv2.getTrackbarPos('upper - green', 'RGB')
        thrs6 = cv2.getTrackbarPos('upper - blue', 'RGB')
        #thrs7 = cv2.getTrackbarPos('mouseOver - red', 'RGB')
        #thrs8 = cv2.getTrackbarPos('mouseOver - green', 'RGB')
        #thrs9 = cv2.getTrackbarPos('mouseOver - blue', 'RGB')

        if (thrs1 > thrs4):
            cv2.setTrackbarPos('lower - red', 'RGB', thrs4 - 1)
        if (thrs2 > thrs5):
            cv2.setTrackbarPos('lower - green', 'RGB', thrs5 - 1)
        if (thrs3 > thrs6):
            cv2.setTrackbarPos('lower - blue', 'RGB', thrs6 - 1)

        colourLower = (thrs1, thrs2, thrs3)
        colourUpper = (thrs4, thrs5, thrs6)

        # resize the frame, blur it, and convert it to the HSV
        # color space
        image = imutils.resize(image, width=600)
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # construct a mask for the object colour, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(image, colourLower, colourUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(image, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(image, center, 5, (0, 0, 255), -1)
                pts.appendleft(center)

        # loop over the set of tracked points
        for i in np.arange(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(linelength / float(i + 1)) * 2.5)
            cv2.line(image, pts[i - 1], pts[i], (0, 0, 255), thickness)

        # show the frame to our screen and increment the frame counter
        cv2.imshow("RGB", image)
        #cv2.imwrite("new_image" + "-" + str(count)+ ".jpg", image)
        count = count + 1
        key = cv2.waitKey(1) & 0xFF
        counter += 1



        if key == ord('q'):
            tracking = False
            break   

       

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()