import cv2 as cv
import numpy as np

downsampling = 1
minArea = 400
maxArea = 3000
fgbg = cv.createBackgroundSubtractorMOG2()

def nothing(x):
  pass

def set_res(cap, x,y):
    cap.set(cv.CAP_PROP_FRAME_WIDTH, int(x))
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, int(y))
    return str(cap.get(cv.CAP_PROP_FRAME_WIDTH)),str(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

cap = cv.VideoCapture(0)
set_res(cap, 1280, 1024)

cv.namedWindow('Thresholds')
cv.moveWindow('Thresholds', 1400,300)
hh='Max'
hl='Min'
wnd = 'Thresholds'
cv.createTrackbar("minArea", "Thresholds",0,4000,nothing)
cv.createTrackbar("maxArea", "Thresholds",0,10000,nothing)
cv.createTrackbar("Saturation", "Thresholds",0,255,nothing)

while True:

    saturation=cv.getTrackbarPos("Saturation", "Thresholds")
    minArea=cv.getTrackbarPos("minArea", "Thresholds")
    maxArea=cv.getTrackbarPos("maxArea", "Thresholds")

    _, frame = cap.read()
    # CUT Frame
    frame = frame[0:1024,0:944]
    # SATURATE - to get the background suptractor look more for color than for brightnesss
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)
    s += saturation # 5
    final_hsv = cv.merge((h, s, v))
    sat_frame = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)
    # Mog2 background substraction
    background = fgbg.apply(sat_frame)
    # GRAYSCALE thrshold
    #gray_frame = cv.cvtColor(background, cv.COLOR_BGR2GRAY)
    #_, threshold = cv.threshold(gray_frame, treshold1, 255,cv.THRESH_BINARY)
   
    # Contours
    kernel = np.ones((5,5), np.uint8) 
    altered_frame = cv.erode(background, kernel, iterations=1) 
    altered_frame = cv.dilate(altered_frame, kernel, iterations=1) 

    contours, _ = cv.findContours(altered_frame.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for c in contours:
		# if the contour is too small, ignore it
        if cv.contourArea(c) < minArea/downsampling:
            continue
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv.boundingRect(c)
        x = x * downsampling
        y = y * downsampling
        w = w * downsampling
        h = h * downsampling
        if cv.contourArea(c) < maxArea:
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
    #cv.imshow("Camera 1", frame)
    #cv.imshow("belt", belt)
    cv.imshow("original", frame)
    #cv.imshow("sat", sat_frame)
   # cv.imshow("gray", threshold)
    cv.imshow("background", background)
    cv.imshow("altered_frame", altered_frame)
  

    key = cv.waitKey(1)
    if key == 27:
        break

cap.release()
cv.destroyAllWindows()