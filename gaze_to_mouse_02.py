#----------imports----------#
import cv2
import numpy as np
from pynput.mouse import Button, Controller
import sys
import time
from simple_pid import PID
#----------code starts here!----------#
from eye_tracker import EyeTracker
sys.path.insert(0, '/home/nasa01/Documents/MATT/GazeTracking')
from GazeTracking.gaze_tracking import GazeTracking


class GazeToMouse(object):

	def __init__(self):

		'''
		calibrate: get center
		'''
		print("Calibrating: look at center of screen")
		time.sleep(2)
		timeout_start = time.time()
		print("Calibrating...")
		gaze = GazeTracking()
		webcam = cv2.VideoCapture(0)
		# EyeTracker(webcam)
		# webcam.set(3, 2560);
		# webcam.set(4, 1080);

		imageWidth  = webcam.get(3) # float
		imageHeight = webcam.get(4) # float

		self.imageCenter = (imageWidth/2, imageHeight/2)
		print("image center", self.imageCenter)
		
		mouse = Controller()
		screenCenter = [2560/2, 1080/2]
		mouse.position = tuple(screenCenter)

		while True:
			# We get a new frame from the webcam
			_, frame = webcam.read()

			# We send this frame to GazeTracking to analyze it
			gaze.refresh(frame)

			frame = gaze.annotated_frame()

			left_pupil = gaze.pupil_left_coords()
			right_pupil = gaze.pupil_right_coords()

			cv2.imshow("Demo", frame)

			if left_pupil is not None and right_pupil is not None:
				self.eyeCenter = np.average([left_pupil, right_pupil], axis=0)
				print(self.eyeCenter)

				break

			if cv2.waitKey(1) == 27:
				break

	def MoveMouse(self):
		gaze = GazeTracking()
		webcam = cv2.VideoCapture(0)
		# webcam.set(3, 2560);
		# webcam.set(4, 1080);
		mouse = Controller()
		screenCenter = [2560/2, 1080/2]
		mouse.position = tuple(screenCenter)
		scaleFactor = 1.2
		pid = PID(.5, .5, 0.05, setpoint=1)
		eyeStateLIST = []

		scaledChange = [0,0]

		while True:
			# print(changeX)
			controlChangeX = pid((mouse.position[0] - screenCenter[0]) - scaledChange[0])
			controlChangeY = pid((screenCenter[1] - mouse.position[1]) - scaledChange[1])
			# We get a new frame from the webcam
			_, frame = webcam.read()
			frame = cv2.flip(frame, 1)

			eye_coord = EyeTracker().trackeyes(frame)


			# We send this frame to GazeTracking to analyze it

			# text = ""
			# eyeState = ""
			# if gaze.is_blinking():
			# 	eyeState = "Blinking"
			# 	eyeStateNum = 1
			# else:
			# 	eyeStateNum = 0

			# eyeStateLIST.append(eyeStateNum)
			# if len(eyeStateLIST) > 6:
			# 	eyeStateAvg = np.rint(np.mean(eyeStateLIST[-5:-1]))
			# 	del eyeStateLIST[0]
			# else:
			# 	eyeStateAvg = 0



			if eye_coord is not None:
				newCoord = np.average([eye_coord[0], eye_coord[1]], axis=0)
				changeX = newCoord[0]-self.imageCenter[0]
				changeY = newCoord[1]-self.imageCenter[1]

				# if changex > changeBuffer or changey > changeBuffer:
				change = [changeX, changeY]
				# else:
				scaledChange = np.average([[controlChangeX, controlChangeY], [change[0]*40, change[1]*10]], axis=0)

				newPos = np.add(screenCenter, np.multiply(scaledChange,1))

				# print(newPos)
				if newPos[0] > 0 and newPos[0] < 2560 and newPos[1] > 0 and newPos[1] < 1080:
					mouse.position = newPos	
				else:
					break

				# if eyeStateAvg == 1:					
				# 	mouse.click(Button.left, 1)
			print(mouse.position) 

			if cv2.waitKey(1) == 27:
				break



GTM = GazeToMouse()

if __name__ == '__main__':
	GTM
	while True:
		GTM.MoveMouse()


