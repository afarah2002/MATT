#----------imports----------#
from pynput.mouse import Button, Controller
import datetime
import imutils
import time
import cv2
import sys
import numpy as np
#----------code starts here!----------#
class FingerTracker(object):

	def __init__(self):
		
		cap = cv2.VideoCapture(2)
		cap.set(3, 2560);
		cap.set(4, 1080);
		mouse = Controller()
		mouse.position = (100, 20)
		while(True):
			# Capture frame-by-frame
			ret, frame = cap.read()

			# Our operations on the frame come here
			# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			# hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
			# lower_red = np.array([0,50,8]) 
			# upper_red = np.array([25,100,100]) 
			# mask = cv2.inRange(hsv, lower_red, upper_red)


			rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
			lower_red = np.array([100,0,0]) 
			upper_red = np.array([250,45,80]) 
			mask = cv2.inRange(rgb, lower_red, upper_red)

			coord_list = cv2.findNonZero(mask)

			if coord_list is not None:
				coord_array = np.array(coord_list)
				CV_coord = np.mean(coord_array, axis=0)[0]
				scaled_coord = np.multiply([CV_coord[0], CV_coord[1]],2)
				mouse_coord = [2560 - scaled_coord[0], scaled_coord[1]]
				mouse.position = (mouse_coord[0], mouse_coord[1])
				# print(mouse_coord)

			# Display the resulting frame
			cv2.imshow('frame',mask)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		# When everything done, release the capture
		cap.release()
		cv2.destroyAllWindows()

FT = FingerTracker()
if __name__ == '__main__':
	try:
		FT
	except KeyboardInterrupt:
		quit()
	