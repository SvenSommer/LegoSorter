import cv2
import imutils

cap1 = cv2.VideoCapture(0);
# set the format into MJPG in the FourCC format 
#cap1.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cap2 = cv2.VideoCapture(2);
cap2.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#cap2.set(cv2.CAP_PROP_AUTOFOCUS, 0)
focus = 0.05
zoom = 200
scale=20

while True:
        cap2.set(cv2.CAP_PROP_FOCUS, focus) 
        cap2.set(cv2.CAP_PROP_ZOOM, zoom)
        ret1, image1 = cap1.read()
        ret2, image2 = cap2.read()

        #print('Retval cap1: ' ,ret2)
        #print('Retval cap2: ', ret2)

        if ret1:
                image1 = imutils.rotate(image1,90)

                cv2.imshow('cam1', image1)    


        if ret2:
                cv2.imshow('cam2', image2)

        k = cv2.waitKey(1)


        if k == ord('q'):
                break
        
        if k == ord('a'):
            zoom += 5
            print('zoom: ' ,zoom)
                
        if k == ord('s'):
            zoom -= 5
            print('zoom: ' ,zoom)    

        if k == ord('n'):
            focus += 0.025
            print('focus: ' ,focus)
        if k == ord('m'):
            focus -= 0.025
            print('focus: ' ,focus)
        if k == ord('z'):
            cap2.set(cv2.CAP_PROP_AUTOFOCUS, 0)
            print('autofocus off')
        if k == ord('u'):
            cap2.set(cv2.CAP_PROP_AUTOFOCUS, 1)
            print('autofocus on')

        fps_cam1 = cap1.get(cv2.CAP_PROP_FPS)
        print("Cam1 fps: {0}".format(fps_cam1))
        fps_cam2 = cap1.get(cv2.CAP_PROP_FPS)
        print("Cam2 fps: {0}".format(fps_cam2))

cap1.release()
cap2.release()
cv2.destroyAllWindows()