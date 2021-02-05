from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import cv2

class Geometry:
    def __init__(self, debug = False, width=4096, height=2160):
        self.debug = debug
        self.width = width
        self.height = height

        # Divisions
        self.division_left_min_x = (2048/555)
        self.division_left_min_y = (1080/193)
        self.division_left_max_x = (2048/555)
        self.division_left_max_y = (1080/978)
        
        self.division_right_min_x = (2048/1473)
        self.division_right_min_y = (1080/177)
        self.division_right_max_x = (2048/1473)
        self.division_right_max_y = (1080/958)

        # Prediction Line
        self.lower_y = 960
        self.prediction_y = (1080/self.lower_y)

        # Tresholds - left
       
        self.threshold_left_min_x1 = (2048/22)
        self.threshold_left_min_y1 = (1080/37)	
        self.threshold_left_min_x2 = (2048/535)
        self.threshold_left_min_y2 = (1080/212)
        
        self.threshold_left_max_x1 = (2048/22)
        self.threshold_left_max_y1 = (1080/self.lower_y)	
        self.threshold_left_max_x2 = (2048/535)
        self.threshold_left_max_y2 = (1080/self.lower_y)

        # Tresholds - center
        self.threshold_center_min_x1 = (2048/570)
        self.threshold_center_min_y1 = (1080/193)	
        self.threshold_center_min_x2 = (2048/1466)
        self.threshold_center_min_y2 = self.threshold_center_min_y1
        
        self.threshold_center_max_x1 = (2048/570)
        self.threshold_center_max_y1 = (1080/self.lower_y)	
        self.threshold_center_max_x2 = self.threshold_center_min_x2
        self.threshold_center_max_y2 = (1080/self.lower_y)
        
        # Tresholds - right
        self.threshold_right_min_x1 = (2048/2018)
        self.threshold_right_min_y1 = (1080/8)	
        self.threshold_right_min_x2 = (2048/1486)
        self.threshold_right_min_y2 = (1080/203)
        
        self.threshold_right_max_x1 = (2048/2025)
        self.threshold_right_max_y1 = (1080/self.lower_y)	
        self.threshold_right_max_x2 = self.threshold_right_min_x2
        self.threshold_right_max_y2 = (1080/self.lower_y)

    def drawTreshholds(self, frame):
        #devision lines
        cv2.line(frame,(int(self.width/self.division_left_min_x), int(self.height/self.division_left_min_y)),(int(self.width/self.division_left_max_x),  int(self.height/self.division_left_max_y)),(255,0,0),2)
        cv2.line(frame,(int(self.width/self.division_right_min_x), int(self.height/self.division_right_min_y)),(int(self.width/self.division_right_max_x),  int(self.height/self.division_right_max_y)),(255,0,0),2)
        
        #Tresholds right
        cv2.line(frame,(int(self.width/self.threshold_left_min_x1), int(self.height/self.threshold_left_min_y1)),(int(self.width/self.threshold_left_min_x2),  int(self.height/self.threshold_left_min_y2)),(255,0,0),1)
        cv2.line(frame,(int(self.width/self.threshold_left_max_x1), int(self.height/self.threshold_left_max_y1)),(int(self.width/self.threshold_left_max_x2),  int(self.height/self.threshold_left_max_y2)),(255,0,0),1)
        cv2.line(frame,(int(self.width/self.threshold_left_min_x1), int(self.height/self.threshold_left_min_y1)),(int(self.width/self.threshold_left_max_x1),  int(self.height/self.threshold_left_max_y1)),(255,0,0),1)
        cv2.line(frame,(int(self.width/self.threshold_left_min_x2), int(self.height/self.threshold_left_min_y2)),(int(self.width/self.threshold_left_max_x2),  int(self.height/self.threshold_left_max_y2)),(255,0,0),1)
        
        #Tresholds center
        cv2.line(frame,(int(self.width/self.threshold_center_min_x1), int(self.height/self.threshold_center_min_y1)),(int(self.width/self.threshold_center_min_x2),  int(self.height/self.threshold_center_min_y2)),(255,0,0),1)
        cv2.line(frame,(int(self.width/self.threshold_center_max_x1), int(self.height/self.threshold_center_max_y1)),(int(self.width/self.threshold_center_max_x2),  int(self.height/self.threshold_center_max_y2)),(255,0,0),1)
        cv2.line(frame,(int(self.width/self.threshold_center_min_x1), int(self.height/self.threshold_center_min_y1)),(int(self.width/self.threshold_center_max_x1),  int(self.height/self.threshold_center_max_y1)),(255,0,0),1)
        cv2.line(frame,(int(self.width/self.threshold_center_min_x2), int(self.height/self.threshold_center_min_y2)),(int(self.width/self.threshold_center_max_x2),  int(self.height/self.threshold_center_max_y2)),(255,0,0),1)
        
        #Tresholds right
        cv2.line(frame,(int(self.width/self.threshold_right_min_x1), int(self.height/self.threshold_right_min_y1)),(int(self.width/self.threshold_right_min_x2),  int(self.height/self.threshold_right_min_y2)),(255,0,0),1)
        cv2.line(frame,(int(self.width/self.threshold_right_max_x1), int(self.height/self.threshold_right_max_y1)),(int(self.width/self.threshold_right_max_x2),  int(self.height/self.threshold_right_max_y2)),(255,0,0),1)
        cv2.line(frame,(int(self.width/self.threshold_right_min_x1), int(self.height/self.threshold_right_min_y1)),(int(self.width/self.threshold_right_max_x1),  int(self.height/self.threshold_right_max_y1)),(255,0,0),1)
        cv2.line(frame,(int(self.width/self.threshold_right_min_x2), int(self.height/self.threshold_right_min_y2)),(int(self.width/self.threshold_right_max_x2),  int(self.height/self.threshold_right_max_y2)),(255,0,0),1)
        
        return frame
    
    def getCameraNameBoundaries(self):
        return int(self.width/self.division_left_min_x), int(self.width/self.division_right_min_x)

    def checkboundaries(self, image, frame):
        if self.checkPoint(image.x, image.y) and self.checkPoint(image.x + image.w, image.y + image.h):
            frame = self.drawColoredBox(frame, image, (0, 255, 0))
            return frame, 1
        elif (image.y + image.h > int(self.height/self.prediction_y)):
            frame = self.drawColoredBox(frame, image, (255, 255, 0))
            return frame, 2
        else :
            frame = self.drawColoredBox(frame, image, (0, 0, 255))
            return frame, 0

    def checkPoint(self,x,y):
        if (y > int(self.height/self.threshold_center_min_y1) and y < int(self.height/self.threshold_center_max_y1) ):
            #center
            if (x > int(self.width/self.threshold_center_min_x1) and x < int(self.width/self.threshold_center_max_x2)) :
                return True
            #left
            elif (x > int(self.width/self.threshold_left_min_x1) and x < int(self.width/self.threshold_left_max_x2)) : 
                return True             
            #right
            elif (x > int(self.width/self.threshold_right_min_x2) and x < int(self.width/self.threshold_right_min_x1)) : 
                 return True   
            else :
                return False

    def drawColoredBox(self, frame, image, color):
        if self.debug:
            cv2.rectangle(frame,[image.x, image.y,  image.w, image.h], color, 5)
        return frame
