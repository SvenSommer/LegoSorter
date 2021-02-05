import time

class Partimage(object):
     def __init__(self, image, x, y, w, h, color, camera):
         self.image = image
         self.x = x 
         self.y = y
         self.w = w
         self.h = h
         self.cx = x + (w / 2)
         self.cy = y + (h / 2)
         self.area = w * h
         self.color = color
         self.camera = camera
         self.timestamp = int(round(time.time() * 1000))