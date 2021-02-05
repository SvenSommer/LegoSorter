# import the necessary packages
from threading import Thread
import cv2

class WebcamVideoStream:
	def __init__(self, src=0, name="WebcamVideoStream"):
		# initialize the video camera stream and read the first frame
		# from the stream

		cap = cv2.VideoCapture(src)			
		cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
		
		if src == 2:
			cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4096)
			cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
			cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
			cap.set(cv2.CAP_PROP_FOCUS, 15) 
			cap.set(cv2.CAP_PROP_AUTO_EXPOSURE ,0)
			cap.set(cv2.CAP_PROP_EXPOSURE,10)
			cap.set(cv2.CAP_PROP_WB_TEMPERATURE,4230)
			cap.set(cv2.CAP_PROP_AUTO_WB,1)
			cap.set(cv2.CAP_PROP_ZOOM, 0)
			cap.set(cv2.CAP_PROP_GAIN, 34)
		else :
			cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
			cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
			cap.set(cv2.CAP_PROP_AUTO_EXPOSURE ,0)
			cap.set(cv2.CAP_PROP_EXPOSURE,10)

		self.stream = cap
		(self.grabbed, self.frame) = self.stream.read()

		# initialize the thread name
		self.name = name

		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False

	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, name=self.name, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return

			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		# return the frame most recently read
		return self.frame

	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
