#----------imports----------#
import cv2
import numpy as np
from pynput.mouse import Button, Controller
import sys
import time
from simple_pid import PID
import psychopy

# GazeParser imports
from GazeParser.TrackingTools import getController

#----------code starts here!----------#
class EyeTracker(object):

	def __init__(self):
		pass

	def get_eye_coord(self):
		# myWin = psychopy.visual.Window()
		webcam = cv2.VideoCapture(0)
		tracker = getController(backend='PsychoPy',dummy=webcam)
		eyePos= tracker.getEyePosition()



if __name__ == '__main__':
	ET = EyeTracker()
	ET.get_eye_coord()