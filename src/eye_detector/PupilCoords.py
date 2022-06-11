from src.eye_detector.Calculator import Calculator
import cv2
import numpy as np
import dlib
#import mediapipe as mp

class PupilCoords():
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.lx = 0
        self.ly = 0
        self.rx = 0
        self.ry = 0
    def pupil_detector(self, eye):
        x = 0
        y = 0
        radius = 0
        output = cv2.cvtColor(eye, cv2.COLOR_GRAY2BGR)
        cnts, thierarchy = cv2.findContours(eye, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(cnts) != 0:
            c = max(cnts, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(c)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(output, center, 1, (255, 0, 0), 1)
            output = cv2.resize(output, (0, 0), fx=10, fy=10, interpolation=cv2.INTER_AREA)
            # (x,y)
            #cv2.imshow("pupil detected", output)
            #print(center)
            #print(x,y)
        # 동공의 좌표 return
        return x, y

    def eye_detector(self, img, arr):
        Cal = Calculator()
        max = Cal.maximum(arr)
        min = Cal.minimum(arr)
        mask = np.zeros_like(img)

        cv2.rectangle(mask, min, max, (255, 255, 255), -1)

        masked = cv2.bitwise_and(img,mask)
        masked = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)

        eye = masked[min[1]:max[1], min[0]:max[0]]
        eye = cv2.bitwise_not(eye)

        _, eye = cv2.threshold(eye, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        kernel = np.ones((3, 3), np.uint8)
        eye = cv2.erode(eye, kernel, iterations=1)
        #eye = cv2.dilate(eye, kernel, iterations=1)

        #cv2.imshow("detected eye",eye)
        x, y = self.pupil_detector(eye)

        return int(x),int(y)

    def pupil_coords(self,f):
        # mp_drawing = mp.solutions.drawing_utils
        # mp_drawing_styles = mp.solutions.drawing_styles
        # mp_face_mesh = mp.solutions.face_mesh
        #
        # drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        #
        # with mp_face_mesh.FaceMesh(
        #     static_image_mode=True,
        #     max_num_faces=1,
        #     refine_landmarks=True,
        #     min_detection_confidence=0.5 ) as face_mesh:
        #     IMG = f
        #     results = face_mesh.process(cv2.cvtColor(IMG,cv2.COLOR_BGR2RGB))
        #
        #     annotated_image = IMG.copy()
        #     for face_landmarks in results.multi_face_landmarks:
        #         print('face_landmarks:',face_landmarks)
        #         mp_drawing.draw_landmarks(
        #             image=annotated_image,
        #             landmark_list=face_landmarks,
        #             connections=mp_face_mesh.FACEMESH_TESSELATION,
        #             landmark_drawing_spec=None,
        #             connection_drawing_spec=mp_drawing_styles
        #                 .get_default_face_mesh_tesselation_style())
        #         mp_drawing.draw_landmarks(
        #             image=annotated_image,
        #             landmark_list=face_landmarks,
        #             connections=mp_face_mesh.FACEMESH_CONTOURS,
        #             landmark_drawing_spec=None,
        #             connection_drawing_spec=mp_drawing_styles
        #                 .get_default_face_mesh_contours_style())
        #         mp_drawing.draw_landmarks(
        #             image=annotated_image,
        #             landmark_list=face_landmarks,
        #             connections=mp_face_mesh.FACEMESH_IRISES,
        #             landmark_drawing_spec=None,
        #             connection_drawing_spec=mp_drawing_styles
        #                 .get_default_face_mesh_iris_connections_style())
        #cv2.imshow(annotated_image)

        cv2.imshow("face",f)
        self.frame = f
        self.grayscale = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)
        face_coords = self.detector(self.grayscale)



        for coord in face_coords:
            landmarks = self.predictor(self.grayscale,coord)

            left_eye = np.array([[landmarks.part(36).x, landmarks.part(36).y],
                             [landmarks.part(37).x, landmarks.part(37).y],
                             [landmarks.part(38).x, landmarks.part(38).y],
                             [landmarks.part(39).x, landmarks.part(39).y],
                             [landmarks.part(40).x, landmarks.part(40).y],
                             [landmarks.part(41).x, landmarks.part(41).y],
                             ], np.int32)
            right_eye = np.array([[landmarks.part(42).x, landmarks.part(42).y],
                              [landmarks.part(43).x, landmarks.part(43).y],
                              [landmarks.part(44).x, landmarks.part(44).y],
                              [landmarks.part(45).x, landmarks.part(45).y],
                              [landmarks.part(46).x, landmarks.part(46).y],
                              [landmarks.part(47).x, landmarks.part(47).y],
                              ], np.int32)

            if(len(left_eye)<1):
                print("no face found!")
                return(self.grayscale)

            self.lx, self.ly = self.eye_detector(self.frame, arr = left_eye)
            self.rx, self.ry = self.eye_detector(self.frame, arr = right_eye)

        return(self.grayscale,[self.lx,self.ly,self.rx,self.ry])
