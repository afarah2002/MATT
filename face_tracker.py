import cv2 
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
detector_params = cv2.SimpleBlobDetector_Params()
detector_params.filterByArea = True
detector_params.maxArea = 1500
detector = cv2.SimpleBlobDetector_create(detector_params)

class Process(object):

	def __init__(self):
		pass

	def nothing(self, x):
		pass

	def detect_faces(self, img, cascade):
		gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		coords = cascade.detectMultiScale(gray_frame, 1.3, 5)
		if len(coords) > 1:
			biggest = (0, 0, 0, 0)
			for i in coords:
				if i[3] > biggest[3]:
					biggest = i
			biggest = np.array([i], np.int32)
		elif len(coords) == 1:
			biggest = coords
		else:
			return None
		for (x, y, w, h) in biggest:
			self.frame = img[y:y + h, x:x + w]

		face_center = ((x+x+h)/2, (y+y+h)/2)
		# print(face_center)
		cv2.imshow('face', self.frame)
		return face_center



class FaceTracker(object):

	def __init__(self):
		pass

	def trackface(self, frame):
		face_center = Process().detect_faces(frame, face_cascade)
		if face_center is not None:
			return face_center

if __name__ == '__main__':

	cap = cv2.VideoCapture(0)
	while True:
		_, frame = cap.read()
		FaceTracker()
		face_center = FaceTracker().trackface(frame)
		print(face_center)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	cap.release()
	cv2.destroyAllWindows()