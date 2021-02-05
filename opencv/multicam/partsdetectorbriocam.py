from basicpartsdetector import BasicPartsDetector
from models.partimage import Partimage
from models.sqlmodel import SQLModel
from geometry.geometry import Geometry
import time
import cv2
from tracking.centroidtracker import CentroidTracker
import numpy as np

class PartsDetectorBrioCam:
	def __init__(self, run_id, folder, cameraname, saturation=120, minArea= 100, downsampling = 2, drawBoxes = True, writeImages = False, min_sharpness = 200, learningRate = 0.001, debug = False):
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
		self.bpd = BasicPartsDetector(cameraname = self.cameraname, saturation=self.saturation, downsampling=self.downsampling, drawBoxes = self.drawBoxes, writeImages = self.writeImages, min_sharpness = self.min_sharpness, learningRate = self.learningRate, debug = self.debug)
		self.geometry = Geometry(debug=self.debug)
		self.boundary_left, self.boundary_right = self.geometry.getCameraNameBoundaries()
		
		self.writeImages = writeImages
		self.newPartCounter = 1
		self.count = 1
		self.part_id = None
		self.sql = SQLModel(run_id)

		self.ct = CentroidTracker()
		self.calibrated = False

	def warmup(self, webcamBRIO) :
		webcamBRIO.stream.set(cv2.CAP_PROP_AUTO_WB,0)
		webcamBRIO.stream.set(cv2.CAP_PROP_WB_TEMPERATURE,4230)
		time.sleep(1)
		webcamBRIO.stream.set(cv2.CAP_PROP_AUTO_WB,1)
		#webcamBRIO.stream.set(cv2.CAP_PROP_WB_TEMPERATURE,4230)

	def mask(self,frame):
		#print("self.calibrated:" + str(self.calibrated))
		
		height, width = frame.shape[:2]
		mask = np.zeros(frame.shape, dtype=np.uint8)
	
		x1 = int(width/(2048/1474))
		y1 = int(height/(1080/1))
		x2 = int(width/(2048/1473))
		y2 = int(height/(1080/173))
		x3 = int(width/(2048/1852))
		y3 = int(height/(1080/1))
		x4 = int(width/(2048/2048))
		y4 = int(height/(1080/1))
		x5 = int(width/(2048/2048))
		y5 = int(height/(1080/1080))
		x6 = int(width/(2048/1630))
		y6 = int(height/(1080/1075))
		x7 = int(width/(2048/1474))
		y7 = int(height/(1080/950))
		x8 = int(width/(2048/1473))
		y8 = int(height/(1080/1080))
		x9 = int(width/(2048/573))
		y9 = int(height/(1080/1080))
		x10 = int(width/(2048/570))
		y10 = int(height/(1080/962))
		x11 = int(width/(2048/442))
		y11 = int(height/(1080/1080))
		x12 = int(width/(2048/1))
		y12 = int(height/(1080/1080))
		x13 = int(width/(2048/1))
		y13 = int(height/(1080/1))
		x14 = int(width/(2048/542))
		y14 = int(height/(1080/191))
		x15 = int(width/(2048/520))
		y15 = int(height/(1080/1))

		roi_corners = np.array([[(x1,y1),(x2,y2), (x3,y3), (x4,y4), (x5,y5), (x6,y6), (x7,y7), (x8,y8), (x9,y9), (x10,y10), (x11,y11), (x12,y12), (x13,y13), (x14,y14), (x15,y15)]], dtype=np.int32)
		channel_count = frame.shape[2]  # i.e. 3 or 4 depending on your image
		ignore_mask_color = (255,)*channel_count
		cv2.fillPoly(mask, roi_corners, ignore_mask_color)

		# apply the mask
		frame = cv2.bitwise_and(frame, mask)
		return frame

	def getPartimages(self, frame):
		frame, partimages = (self.bpd.getPartimages(self.mask(frame), frame, self.minArea, self.cameraname, self.boundary_left,self.boundary_right))
		return frame, partimages

	def trackObjects(self, partimages):
		# This cam is not used for object tracking
		return []

	def drawTreshholds(self, frame):
		height, width = frame.shape[:2]
		cv2.putText(frame, "res: " + str(height) + " x " + str(width), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
		frame = self.geometry.drawTreshholds(frame)
		return frame

	def checkImage(self, image, frame):
		return self.geometry.checkboundaries(image, frame)

	def getCameraName(self):
		return self.cameraname
		
	