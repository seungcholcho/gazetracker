import cv2
import numpy as np
import dlib

class face_detector:

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    def __init__(self,frame):
        self.frame = frame
        self.gray_scale_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.face = detector(gray_scale_img)

    def showFace(frame):
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)