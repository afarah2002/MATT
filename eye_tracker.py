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
			frame = img[y:y + h, x:x + w]

		face_center = ((y+y+h)/2, (x+x+h)/2)
		print(face_center)
		return frame

	def detect_eyes(self, img, cascade):
		gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		eyes = cascade.detectMultiScale(gray_frame, 1.3, 5) # detect eyes
		width = np.size(img, 1) # get face frame width
		height = np.size(img, 0) # get face frame height
		left_eye = None
		right_eye = None
		for (x, y, w, h) in eyes:
			if y > height / 2:
				pass
			eyecenter = x + w / 2  # get the eye center
			if eyecenter < width * 0.5:
				left_eye = img[y:y + h, x:x + w]
			else:
				right_eye = img[y:y + h, x:x + w]

		return left_eye, right_eye

	def cut_eyebrows(self, img):
		height, width = img.shape[:2]
		eyebrow_h = int(height / 4)
		img = img[eyebrow_h:height, 0:width]  # cut eyebrows out (15 px)
		return img

	def blob_process(self, img, threshold, detector):
		gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		_, img = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
		img = cv2.erode(img, None, iterations=2)
		img = cv2.dilate(img, None, iterations=4)
		img = cv2.medianBlur(img, 5)
		keypoints = detector.detect(img)
		# print(keypoints)
		return keypoints

class EyeTracker(object):

	def __init__(self):
		pass

	def trackeyes(self, frame):

		eye_coord = None
		face_frame = Process().detect_faces(frame, face_cascade)
		if face_frame is not None:
			cv2.imshow('face', face_frame)
			eyes = Process().detect_eyes(face_frame, eye_cascade)
			for eye in eyes:
				if eye is not None:
					threshold = 30
					eye = Process().cut_eyebrows(eye)
					# print("eye")
					keypoints = Process().blob_process(eye, threshold, detector)
					eye = cv2.drawKeypoints(eye, keypoints, eye, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
					for keyPoint in keypoints:
						eye_x = keyPoint.pt[0] #i is the index of the blob you want to get the position
						eye_y = keyPoint.pt[1]
						eye_coord = [eye_x, eye_y]
						return eye_coord


if __name__ == '__main__':

	cap = cv2.VideoCapture(0)
	cv2.namedWindow('image')
	cv2.createTrackbar('threshold', 'image', 0, 255, Process().nothing)
	while True:
		_, frame = cap.read()
		EyeTracker()
		eye_coord = EyeTracker().trackeyes(frame)
		# print(eye_coord)

		cv2.imshow('image', frame)
						# return eye_coord
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	cap.release()
	cv2.destroyAllWindows()