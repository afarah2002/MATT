#----------imports----------#
import cv2
import numpy as np
from pynput.mouse import Button, Controller
import sys
import time
from simple_pid import PID
#----------code starts here!----------#
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
		webcam.set(3, 2560);
		webcam.set(4, 1080);

		# while time.time < timeout_start + time.time():
			# # timer
			# test = 0
		 #    if test == 5:
		 #        break
		 #    test -= 1

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
		webcam.set(3, 2560);
		webcam.set(4, 1080);
		mouse = Controller()
		screenCenter = [2560/2, 1080/2]
		mouse.position = tuple(screenCenter)
		scaleFactor = 10
		eyeStateLIST = []

		while True:
			# We get a new frame from the webcam
			_, frame = webcam.read()

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
			if len(eyeStateLIST) > 10:
				eyeStateAvg = np.rint(np.mean(eyeStateLIST[-9:-1]))
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

			if left_pupil is not None and right_pupil is not None:
				newCoord = np.average([left_pupil, right_pupil], axis=0)
				changeX = self.eyeCenter[0]-newCoord[0]
				changeY = newCoord[1]-self.eyeCenter[1]

				# if changex > changeBuffer or changey > changeBuffer:
				change = [changeX, changeY]
				# else:
				scaledChange = np.multiply(change, scaleFactor)
				newPos = np.add(screenCenter, scaledChange)
				mouse.position = tuple(newPos)
				# print(newPos)

				if eyeState == "Blinking":					
					mouse.click(Button.left, 1)

			if cv2.waitKey(1) == 27:
				break



GTM = GazeToMouse()

if __name__ == '__main__':
	GTM
	GTM.MoveMouse()

