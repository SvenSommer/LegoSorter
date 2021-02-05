
import imutils
import cv2
import numpy as np
from models.partimage import Partimage
from sobelcontours.sobelcontours import SobelContours
from simplecontours.simplecontours import SimpleContours


class BasicPartsDetector:
	def __init__(self, cameraname, saturation, downsampling, drawBoxes, writeImages, min_sharpness, learningRate, debug):
		self.cameraname = cameraname
		self.downsampling = downsampling
		self.saturation = saturation
		self.drawBoxes = drawBoxes
		self.writeImages = writeImages
		self.min_sharpness = min_sharpness
		self.learningRate = learningRate
		self.debug = debug
		self.fgbg = cv2.createBackgroundSubtractorMOG2(history=400, detectShadows=True)
		#self.simplecontours = SimpleContours(delta_thresh = 7)
		#self.sobel = SobelContours()


	def getPartimages(self, masked_frame, original_frame, minArea, cameraname, division_left=0, division_right=0):
		contour_margin = 10
		images = []
		original_frame = np.asarray(original_frame)
		small_frame = imutils.resize(masked_frame, int(masked_frame.shape[1]/self.downsampling))
		if self.saturation > 0:
			hsv = cv2.cvtColor(small_frame, cv2.COLOR_BGR2HSV)
			h, s, v = cv2.split(hsv)
			s += self.saturation # 5
			final_hsv = cv2.merge((h, s, v))
			small_frame = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
			#if self.debug:
			#	cv2.imshow("saturated_frame "+ self.cameraname , small_frame)

		contours = self.findContoursviaBackGroundSubstaraction(small_frame,self.learningRate)
		#contours = self.sobel.findContoursWithSobel(small_frame)
		#contours = self.simplecontours.getContoursfromAvg(small_frame)
		# loop over the contours
		for c in contours:
			# only add the contour to the locations list if it
			# exceeds the minimum area

			
			#print("found " + str(len(c)) + " contours")
			#(x, y, w, h) = cv2.boundingRect(c)
			#print("c:" + str(c))
			x = int(c[0])
			y =  int(c[1])
			w =  int(c[2])
			h =  int(c[3])
			area = w * h
			x = (x - contour_margin) * self.downsampling
			y = (y - contour_margin) * self.downsampling
			w = (w + contour_margin*2) * self.downsampling
			h = (h + contour_margin*2) * self.downsampling
			if area > minArea:				
				partimage = original_frame[y:y+h,x:x+w]
				avg_color = self.getMeanColorFromCenter(partimage, w, h)
				if (cameraname.startswith("BRIO") and x < division_left):
					images.append(Partimage(partimage, x, y, w, h, 0, "BRIO_left"))
				elif (cameraname == "BRIO" and x > division_left and x < division_right):
					images.append(Partimage(partimage, x, y, w, h, 0, "BRIO_center"))
				elif (cameraname == "BRIO" and x > division_right):
					images.append(Partimage(partimage, x, y, w, h, 0, "BRIO_right"))
				else:
					images.append(Partimage(partimage, x, y, w, h, 0, cameraname))
				#color recogniotion should start here for each image on the inner contours with a confidence!
				

				if self.debug:
					cv2.rectangle(masked_frame,[x, y , w, h], (int(avg_color[0]), int(avg_color[1]), int(avg_color[2])), 20)
					cv2.putText(masked_frame, "area " + str(area), (x + 20, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 255, 180), 2)
					cv2.putText(masked_frame, "P1:" + str(x) + ", " + str(y), (x -20, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
					cv2.putText(masked_frame, "P2:" + str(x + w) + ", " + str(y + h), (x + w - 80, y + h - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
			else:
				if self.debug:
					cv2.rectangle(masked_frame,[x, y , w, h], (0, 0, 255), 6)
					cv2.putText(masked_frame, "area " + str(area), (x + 20, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

		# return the set of locations
		return masked_frame, images

	def getMeanColorFromCenter(self, image, width, height):
		m = 30
		cx = width / 2
		cy = height / 2
		upper_left = (int(cx - m), int(cy - m))
		bottom_right = (int(cx + m), int(cy + m))
		rect_img = image[upper_left[1] : bottom_right[1], upper_left[0] : bottom_right[0]]
		avg_color = np.array(cv2.mean(rect_img)).astype(np.uint8)
		
		return avg_color

	def findContoursviaBackGroundSubstaraction(self, frame, learningRate):
		if self.saturation != 0:
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			h, s, v = cv2.split(hsv)
			s += self.saturation
			final_hsv = cv2.merge((h, s, v))
			altered_frame = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
		else:
			altered_frame = frame

		# Mog2 background substraction
		background_frame = self.fgbg.apply(altered_frame,None, learningRate)

		# Denoising
		denoised_frame = self.denoise(background_frame)
		#Remove shadows
		denoised_frame[denoised_frame==127]=0
		#if self.debug: 
		#	cv2.imshow("background_frame " + self.cameraname, denoised_frame)
		contours, _ = cv2.findContours(denoised_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		rects =[]
		#print("len(contours): " + str(len(contours)))
		for c in contours:
			(x,y,w,h) = cv2.boundingRect(c)
			cv2.rectangle(frame,[x, y , w, h], (255, 255, 180), 1)
			rects.append(cv2.boundingRect(c))
			rects.append(cv2.boundingRect(c))
			#print("cv2.boundingRect(c): " + str(cv2.boundingRect(c)) )

		newrects,weights = cv2.groupRectangles(rects, 1, 1.4)
		rs = []
		for r in newrects:
			x = int(r[0])
			y = int(r[1])
			w = int(r[2])
			h = int(r[3])
			cv2.rectangle(frame,[x, y , w, h], (20, 255, 180), 1)
			i = [int(r[0]),int(r[1]),int(r[2]),int(r[3])]
			
			rs.append(i)
			rs.append(i)
			
			#print("rs" + str(rs) )
		rs = rs + rects + rects
		rects,weights = cv2.groupRectangles(rs, 1, 1.4)
		#cv2.imshow("groupRectangles", frame)
		return rects

	def denoise(self, frame):
		kernel = np.ones((8,8), np.uint8) 
		denoised_frame = cv2.erode(frame, kernel, iterations=1) 
		denoised_frame = cv2.dilate(denoised_frame, kernel, iterations=2)
		return denoised_frame

	def denoise2(self, frame):

		se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
		se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
		mask = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, se1)
		mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se2)

		mask = np.dstack([mask, mask, mask]) / 255
		out = frame * mask

		return out