import cv2
import imutils

#cap1 = cv2.VideoCapture(0);
# set the format into MJPG in the FourCC format 
#cap1.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
#cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
#cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4096)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CAP_PROP_FOCUS, 15) 
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE ,0)
cap.set(cv2.CAP_PROP_EXPOSURE,25)
cap.set(cv2.CAP_PROP_WB_TEMPERATURE,4280)
cap.set(cv2.CAP_PROP_AUTO_WB,1)
cap.set(cv2.CAP_PROP_ZOOM, 200)
cap.set(cv2.CAP_PROP_GAIN, 34)


zoom = 200
autofocus = "OFF"
focus = 15


whiteb = "ON"
whitetemp = 4280

exposure_auto = "ON"
exposure = 25

gain = 34

saturation = 115

framecounter= 0


fontheight = 0.8
def downscale_preview(frame):
	return imutils.resize(frame, int(frame.shape[1]/2))

while True:




        
    ret, frame = cap.read()

    #print('Retval cap1: ' ,ret2)
    #print('Retval cap2: ', ret2)

    framecounter += 1
    if ret:
        height, width = frame.shape[:2]
        cv2.putText(frame, "res: " + str(height) + " x " + str(width) + " frame: " + str(framecounter) , (10, 30), cv2.FONT_HERSHEY_SIMPLEX, fontheight, (0, 255, 0), 2)
        cv2.putText(frame, "zoom: " + str(zoom) + " [a-|s+]" , (10, 60), cv2.FONT_HERSHEY_SIMPLEX, fontheight, (0, 255, 0), 2)
        cv2.putText(frame, "autofocus: " + autofocus + " [z|u] focus: " + str(cap.get(cv2.CAP_PROP_FOCUS)) + "/" + str(focus) + " [n-|m+]", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, fontheight, (0, 255, 0), 2)
        cv2.putText(frame, "WhiteBalancing Auto: " + whiteb + " [o|p] temp: " + str(cap.get(cv2.CAP_PROP_WB_TEMPERATURE)) + "/" + str(whitetemp) + " [k-|l+]", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, fontheight, (0, 255, 0), 2)
        cv2.putText(frame, "Exposure Auto: " + exposure_auto + " [d|f] exposure: " + str(cap.get(cv2.CAP_PROP_EXPOSURE)) + "/" + str(exposure) + " [c-|v+]", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, fontheight, (0, 255, 0), 2)
        cv2.putText(frame, "Gain: " + str(cap.get(cv2.CAP_PROP_GAIN)) + "/" + str(gain) + " [h-|j+]", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, fontheight, (0, 255, 0), 2)
        cv2.putText(frame, "Saturation: " + str(cap.get(cv2.CAP_PROP_SATURATION)) + "/" + str(saturation) + " [y-|x+]", (10, 210), cv2.FONT_HERSHEY_SIMPLEX, fontheight, (0, 255, 0), 2)
        cv2.putText(frame, "fps: " + format( cap.get(cv2.CAP_PROP_FPS)), (10, 240), cv2.FONT_HERSHEY_SIMPLEX, fontheight, (0, 255, 0), 2)
        cv2.imshow('cam', downscale_preview(frame))

    k = cv2.waitKey(1)


    if k == ord('q'):
            break
    
    # Zoom
    if k == ord('a'):
        zoom -= 5  
        cap.set(cv2.CAP_PROP_ZOOM, zoom)          
    if k == ord('s'):
        zoom += 5
        cap.set(cv2.CAP_PROP_ZOOM, zoom)

    # Focus
    if k == ord('z'):
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        autofocus = "OFF"
    if k == ord('u'):
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
        autofocus = "ON"
    if k == ord('n'):
        focus -= 5
        cap.set(cv2.CAP_PROP_FOCUS, focus) 
    if k == ord('m'):
        focus += 5
        cap.set(cv2.CAP_PROP_FOCUS, focus) 

    # White Balancing
    if k == ord('o'):
        cap.set(cv2.CAP_PROP_AUTO_WB,0)
        whiteb = "OFF"
    if k == ord('p'):
        cap.set(cv2.CAP_PROP_AUTO_WB,1)
        
        whiteb = "ON"
    if k == ord('k'):
        whitetemp -= 10
        cap.set(cv2.CAP_PROP_WB_TEMPERATURE,whitetemp )
    if k == ord('l'):
        whitetemp += 10
        cap.set(cv2.CAP_PROP_WB_TEMPERATURE,whitetemp)

    # Exposure
    if k == ord('d'):
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE ,0)
        exposure_auto = "OFF"
    if k == ord('f'):
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE ,1)
        exposure_auto = "ON"
    if k == ord('c'):
        exposure -= 5
        cap.set(cv2.CAP_PROP_EXPOSURE,exposure )
    if k == ord('v'):
        exposure += 5
        cap.set(cv2.CAP_PROP_EXPOSURE,exposure)

    # saturation
    if k == ord('y'):
        saturation -= 5
        cap.set(cv2.CAP_PROP_SATURATION,saturation )
    if k == ord('x'):
        saturation += 5
        cap.set(cv2.CAP_PROP_SATURATION,saturation)
     

    # Gain
    if k == ord('h'):
        gain -= 1
        cap.set(cv2.CAP_PROP_GAIN ,gain )
    if k == ord('j'):
        gain += 1
        cap.set(cv2.CAP_PROP_GAIN ,gain)

cap.release()

cv2.destroyAllWindows()