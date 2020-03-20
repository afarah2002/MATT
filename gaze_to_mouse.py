#----------imports----------#
import cv2
import numpy as np
from pynput.mouse import Button, Controller
import sys
import time
from simple_pid import PID
#----------code starts here!----------#
from eye_tracker import EyeTracker
from face_tracker import FaceTracker
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

			# cv2.imshow("Demo", frame)

			# EyeTracker()
			# eye_coord = EyeTracker().trackeyes(frame)
			# if eye_coord is not None:
			# 	print(eye_coord)
			# 	self.fine_eyeCenter = eye_coord


			if left_pupil is not None and right_pupil is not None:
				self.coarse_eyeCenter = np.average([left_pupil, right_pupil], axis=0)
				print(self.coarse_eyeCenter)

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
		# mouse.position = tuple(screenCenter)
		scaleFactor = 1.2
		pid = PID(.2, .2, 0.01, setpoint=1)
		eyeStateLIST = []

		scaledChange = [0,0]

		while True:
			# print(changeX)
			controlChangeX = pid((mouse.position[0] - screenCenter[0]) - scaledChange[0])
			controlChangeY = pid((screenCenter[1] - mouse.position[1]) - scaledChange[1])
			# We get a new frame from the webcam
			_, webcam_frame = webcam.read()

			FaceTracker()
			face_center = FaceTracker().trackface(webcam_frame)
			# print(face_center)
			# FaceTracker()
			# face_frame = FaceTracker().trackeyes(webcam_frame)
			# face_frame = FaceTracker().get_face_frame()
			frame = cv2.flip(webcam_frame, 1)

			# We send this frame to GazeTracking to analyze it
			gaze.refresh(frame)

			frame = gaze.annotated_frame()
			text = ""
			eyeState = ""
			if gaze.is_blinking():
				eyeState = "Blinking"
				eyeStateNum = 1
			else:
				eyeStateNum = 0

			eyeStateLIST.append(eyeStateNum)
			if len(eyeStateLIST) > 6:
				eyeStateAvg = np.rint(np.mean(eyeStateLIST[-5:-1]))
				del eyeStateLIST[0]
			else:
				eyeStateAvg = 0

			# elif gaze.is_right():
			# 	text = "Looking right"
			# elif gaze.is_left():
			# 	text = "Looking left"
			# elif gaze.is_center():
			# 	text = "Looking center"
			# print(eyeStateLIST)
			# print(eyeStateAvg)
			cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

			left_pupil = gaze.pupil_left_coords()
			right_pupil = gaze.pupil_right_coords()
			cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
			cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

			cv2.imshow("Demo", frame)

			if left_pupil is not None:
				coarse_newCoord = left_pupil
			if right_pupil is not None:
				coarse_newCoord = right_pupil

			if left_pupil is not None or right_pupil is not None:
				# coarse_newCoord = np.average([left_pupil, right_pupil], axis=0)
				changeX = coarse_newCoord[0]-self.imageCenter[0]
				changeY = coarse_newCoord[1]-self.imageCenter[1]

				# if changex > changeBuffer or changey > changeBuffer:
				change = [changeX, changeY]
				# else:
				scaledChange = np.average([[controlChangeX, controlChangeY], [change[0]*25, change[1]*10]], axis=0)

				newPos = np.add(screenCenter, np.multiply(scaledChange,1))

				# print(newPos)
				if newPos[0] > 10 and newPos[0] < 2550 and newPos[1] > 10 and newPos[1] < 1070:
					mouse.position = newPos	
				else:
					break
					# pass

				if eyeStateAvg == 1:					
					mouse.click(Button.left, 1)
				print(mouse.position) 
			else:
				########################3
				# fine control pupil follower


				pass
				# EyeTracker()
				# fine_newCoord = EyeTracker().trackeyes(frame)
				# print(fine_newCoord)

			if cv2.waitKey(1) == 27:
				break



GTM = GazeToMouse()

if __name__ == '__main__':
	GTM
	while True:
		GTM.MoveMouse()


