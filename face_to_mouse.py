#----------imports----------#
import cv2
import numpy as np
from pynput.mouse import Button, Controller
import sys
import time
from simple_pid import PID
from face_tracker import FaceTracker
sys.path.insert(0, '/home/nasa01/Documents/MATT/GazeTracking')
from GazeTracking.gaze_tracking import GazeTracking

#----------code starts here!----------#
class FaceToMouse(object):

	def __init__(self):

		'''
		calibrate: get center
		'''
		print("Calibrating: look at center of screen")
		time.sleep(2)
		print("Calibrating...")
		webcam = cv2.VideoCapture(0)

		imageWidth  = webcam.get(3) # float
		imageHeight = webcam.get(4) # float

		self.imageCenter = (imageWidth/2, imageHeight/2)
		print("image center", self.imageCenter)
		
		mouse = Controller()
		screenCenter = [2560/2, 1080/2]
		mouse.position = tuple(screenCenter) # set mouse to center of screen
		while True:
			# We get a new frame from the webcam
			_, frame = webcam.read()			
			self.coarse_faceCenter = FaceTracker().trackface(frame)
			if self.coarse_faceCenter is not None:
				print(self.coarse_faceCenter)
				break

			if cv2.waitKey(1) == 27:
				break

	def move_mouse(self):

		mouse = Controller()
		screenCenter = [2560/2, 1080/2]
		# mouse.position = tuple(screenCenter)
		scaleFactor = 1.2
		pid = PID(.2, .2, 0.05, setpoint=1)
		eyeStateLIST = []

		scaledChange = [0,0]

		webcam = cv2.VideoCapture(0)
		while True:
			# set pid controls
			controlChangeX = pid((mouse.position[0] - screenCenter[0]) - scaledChange[0])
			controlChangeY = pid((screenCenter[1] - mouse.position[1]) - scaledChange[1])

			_, frame = webcam.read()
			FaceTracker()
			face_center = FaceTracker().trackface(frame)
			print(face_center)

			if face_center is not None:

				############# YAAAAAAASSSSSS THE PID WORKS ON MULTIPLE FILES ###############33

				coarse_newCoord = face_center

				changeX = self.imageCenter[0]-coarse_newCoord[0]
				changeY = coarse_newCoord[1]-self.imageCenter[1]

				# if changex > changeBuffer or changey > changeBuffer:
				change = [changeX, changeY]
				# else:
				scaledChange = np.average([[controlChangeX, controlChangeY], [change[0]*35, change[1]*20]], axis=0)

				newPos = np.add(screenCenter, np.multiply(scaledChange,1))

				# print(newPos)
				if newPos[0] > 10 and newPos[0] < 2550 and newPos[1] > 10 and newPos[1] < 1070:
					mouse.position = newPos	
				else:
					break
					


			# show full view
			cv2.imshow('full', frame)

			#close up
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		webcam.release()
		cv2.destroyAllWindows()



if __name__ == '__main__':
	FTM = FaceToMouse()
	# cap = cv2.VideoCapture(0)
	while True:

		FTM.move_mouse()

