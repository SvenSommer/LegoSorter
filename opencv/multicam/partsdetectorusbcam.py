from basicpartsdetector import BasicPartsDetector
from models.partimage import Partimage
from models.sqlmodel import SQLModel
import time
import cv2
from tracking.centroidtracker import CentroidTracker
import numpy as np



class PartsDetectorUsbCam:
	def __init__(self, run_id, folder, cameraname, saturation=120, minArea= 200, downsampling = 2, drawBoxes = True, writeImages = False, min_sharpness = 200, learningRate = 0.001, debug = False):
		self.run_id = run_id
		self.folder = folder
		self.cameraname = cameraname
		
		self.saturation = saturation
		self.minArea = minArea
		self.downsampling = downsampling
		self.drawBoxes = drawBoxes
		self.writeImages = writeImages
		self.min_sharpness = min_sharpness
		self.learningRate = learningRate
		self.debug = debug
		#print("self.saturation : "  + str(self.saturation))
		#print("self.downsampling : "  + str(self.downsampling))
		self.bpd = BasicPartsDetector(cameraname = self.cameraname, saturation=self.saturation, downsampling=self.downsampling, drawBoxes = self.drawBoxes, writeImages = self.writeImages, min_sharpness = self.min_sharpness, learningRate = self.learningRate, debug = self.debug)

		self.writeImages = writeImages
		self.newPartCounter = 1
		self.count = 1
		self.part_id = None
		self.sql = SQLModel(run_id)

		self.threshold_minx1 = (1920/334)
		self.threshold_minx2 = (1920/1568)	
		self.threshold_miny = (1080/252)		

		self.threshold_maxx1 = (1920/1)
		self.threshold_maxx2 = (1920/1920)
		self.threshold_maxy = (1080/1030)
		self.ct = CentroidTracker()

	def calibrate(self, frame):
		pass

	def mask(self,frame):
		height, width = frame.shape[:2]
		mask = np.zeros(frame.shape, dtype=np.uint8)

		x1 = int(width/(1920/1553))
		y1 = int(height/(1080/215))
		x12 = int(width/(1920/1920))
		y12 = int(height/(1080/1080))
		x2 = int(width/(1920/1))
		y2 = int(height/(1080/1080))
		x3 = int(width/(1920/345))
		y3 = int(height/(1080/215))
		

		roi_corners = np.array([[(x1,y1),(x12,y12), (x2,y2), (x3,y3)]], dtype=np.int32)
		channel_count = frame.shape[2]  # i.e. 3 or 4 depending on your image
		ignore_mask_color = (255,)*channel_count
		cv2.fillPoly(mask, roi_corners, ignore_mask_color)

		# apply the mask
		frame = cv2.bitwise_and(frame, mask)
		return frame

	def getPartimages(self, frame):
		frame, partimages = (self.bpd.getPartimages(self.mask(frame), frame, self.minArea, self.cameraname))
		return frame, partimages

	def trackObjects(self, partimages):
		rects = []
		if len(partimages) > 0:
			#print("len(partimages) : " + str(len(partimages)))
			for image in partimages:
				#print("len(partimage) : " + str(len(partimage)))
				box = np.array([image.x, image.y ,image.x + image.w, image.y + image.h, image.color])
				rects.append(box)
							
		objects = self.ct.update(rects)
		return objects
	
	def drawTreshholds(self, frame):
		height, width = frame.shape[:2]
		cv2.putText(frame, "res: " + str(height) + " x " + str(width), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
		cv2.putText(frame, "ymin = " + str(int(height/self.threshold_miny)), (int(width/self.threshold_minx1) + 10, int(height/self.threshold_miny) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
		cv2.line(frame,(int(width/self.threshold_minx1), int(height/self.threshold_miny)),(int(width/self.threshold_minx2), int(height/self.threshold_miny)),(255,0,0),1)
		cv2.putText(frame, "ymax = " + str(int(height/self.threshold_maxy)), (int(width/self.threshold_maxx1) + 10, int(height/self.threshold_maxy) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
		cv2.line(frame,(int(width/self.threshold_maxx1), int(height/self.threshold_maxy)),(int(width/self.threshold_maxx2), int(height/self.threshold_maxy)),(255,0,0),1)
		return frame

	def drawColoredBox(self, frame, image, color):
		if self.debug:
			cv2.rectangle(frame,[image.x, image.y,  image.w, image.h], color, 5)
		return frame

	def checkImage(self, image, frame):
		return self.checkboundaries(image, frame)
	
	def checkboundaries(self, image, frame):
		#return frame, False
		height, _ = frame.shape[:2]

		if self.checkPoint(height, image.y) and self.checkPoint(height, image.y + image.h):

			
			frame = self.drawColoredBox(frame, image, (0, 255, 0))
			return frame, True
		else :
			frame = self.drawColoredBox(frame, image, (0, 0, 255))
			return frame, False


	def checkPoint(self, height, y):
		if (y > int(height/self.threshold_miny) and y < int(height/self.threshold_maxy)) :
			#if self.debug:
				#print("usb: image in boundaries, y = " + str(y))
			return True
		else : 
			#if self.debug:
				#if y < int(height/self.threshold_miny):
				#	print("usb: y < self.threshold_miny :" + str(y) + " < " + str(int(height/self.threshold_miny)))
				#if y > int(height/self.threshold_maxy):
				#	print("usb: y > self.threshold_maxy :" + str(y) + " > " + str(int(height/self.threshold_maxy)))
			return False

	def getCameraName(self):
		return self.cameraname