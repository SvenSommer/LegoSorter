import cv2
import imutils

cap1 = cv2.VideoCapture(0)
# set the format into MJPG in the FourCC format 
cap1.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cap2 = cv2.VideoCapture(2)
cap2.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#cap2.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(cv2.CV_CAP_PROP_SETTINGS, 1)
focus = 0.05
zoom = 200
scale=20

count = 0
static_back1 = None
static_back2 = None

while True:
        cap2.set(cv2.CAP_PROP_FOCUS, focus) 
        cap2.set(cv2.CAP_PROP_ZOOM, zoom)
        ret1, image1 = cap1.read()
        ret2, image2 = cap2.read()

        #print('Retval cap1: ' ,ret2)
        #print('Retval cap2: ', ret2)
             
        if ret1:
            fps_cam1 = cap1.get(cv2.CAP_PROP_FPS)
            image1 = imutils.rotate(image1,90)
            cv2.putText(image1,"Cam1 fps: {0}".format(fps_cam1), 
            (10,20),  # bottomLeftCornerOfText 
            cv2.FONT_HERSHEY_SIMPLEX, # font
            1, # fontScale
            (255,255,255), #fontColor
            2) # lineType  

            motion1 = 0
            # Converting color image to gray_scale image 
            gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY) 
            gray1 = cv2.GaussianBlur(gray1, (21, 21), 0) 

            if static_back1 is None: 
                static_back1 = gray1 
                continue

            # Difference between static background  
            # and current image1(which is GaussianBlur) 
            diff_frame1 = cv2.absdiff(static_back1, gray1) 

            # If change in between static background and 
            # current frame is greater than 30 it will show white color(255) 
            thresh_frame1 = cv2.threshold(diff_frame1, 20, 255, cv2.THRESH_BINARY)[1] 
            thresh_frame1 = cv2.dilate(thresh_frame1, None, iterations = 2) 

             # Finding contour of moving object 
            _,cnts,_ = cv2.findContours(thresh_frame1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

            for contour in cnts: 
                if cv2.contourArea(contour) < 10000: 
                    continue
                motion1 = 1

                (x, y, w, h) = cv2.boundingRect(contour) 
                # making green rectangle arround the moving object 
                cv2.rectangle(image1, (x, y), (x + w, y + h), (0, 255, 0), 3) 

                if not cv2.imwrite(('/home/robert/LegoSorter/partimages/%d_cam1.jpg' % count), image1[y:y+h,x:x+w]):
                    raise Exception("Could not write images")
                count+=1
            cv2.imshow('cam1', image1)       

        if ret2:
            fps_cam2 = cap2.get(cv2.CAP_PROP_FPS)
            cv2.putText(image2,"Cam2 fps: {0}".format(fps_cam2), 
            (10,20),  # bottomLeftCornerOfText 
            cv2.FONT_HERSHEY_SIMPLEX, # font
            1, # fontScale
            (255,255,255), #fontColor
            2) # lineType  

            motion2 = 0
            # Converting color image to gray_scale image 
            gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY) 
            gray2 = cv2.GaussianBlur(gray2, (21, 21), 0) 

            if static_back2 is None: 
                static_back2 = gray2 
                continue

            # Difference between static background  
            # and current image1(which is GaussianBlur) 
            diff_frame2 = cv2.absdiff(static_back2, gray2) 

            # If change in between static background and 
            # current frame is greater than 10 it will show white color(255) 
            thresh_frame2 = cv2.threshold(diff_frame2, 10, 255, cv2.THRESH_BINARY)[1] 
            thresh_frame2 = cv2.dilate(thresh_frame2, None, iterations = 2) 

             # Finding contour of moving object 
            _,cnts,_ = cv2.findContours(thresh_frame2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

            for contour in cnts: 
                if cv2.contourArea(contour) < 10000: 
                    continue
                motion2 = 1

                (x, y, w, h) = cv2.boundingRect(contour) 
                # making green rectangle arround the moving object 
                cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 255, 0), 3) 

                if not cv2.imwrite(('/home/robert/LegoSorter/partimages/%d_cam2.jpg' % count), image2[y:y+h,x:x+w]):
                    raise Exception("Could not write images")
                count+=1

            cv2.imshow('cam2', image2) 

        if count > 255:
            break

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

       


cap1.release()
cap2.release()
cv2.destroyAllWindows()