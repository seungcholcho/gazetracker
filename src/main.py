import cv2
import numpy as np
import dlib

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def mindetector(arr):
    min_x = 1000
    min_y = 1000
    for x in range(0, 5):
        temp_x = arr[x][0]
        temp_y = arr[x][1]
        if (temp_x <min_x):
            min_x = temp_x
        elif (temp_y < min_y):
            min_y = temp_y
    return (min_x,min_y)

def maxdetector(arr):
    max_x = 0
    max_y = 0
    for x in range(0, 5):
        temp_x = arr[x][0]
        temp_y = arr[x][1]
        if (temp_x > max_x):
            max_x = temp_x
        elif (temp_y > max_y):
            max_y = temp_y

    return (max_x,max_y)


def grassfire(eye):
    return eye

#눈 영역을 검출하여 이진화 후 반환한다.
def eye(img,arr):
    val = 255
    min = mindetector(arr)
    max = maxdetector(arr)
    mask = np.zeros_like(img)
    kernel = np.ones((1,1),np.uint8)
    cv2.rectangle(mask, min, max, (255, 255, 255), -1)
    masked = cv2.bitwise_and(frame, mask)
    masked = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    eye = masked[min[1]:max[1],min[0]:max[0]]
    eye2 = eye
    #cv2.imshow("nonblur",eye)
    #eye = cv2.GaussianBlur(eye,(7,7),0)
    #cv2.imshow("blur",eye)
    eye = cv2.bitwise_not(eye)
    eye = cv2.erode(eye,kernel,iterations=2)
    eye = cv2.bitwise_not(eye)

    _,eye = cv2.threshold(eye,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)

    #eye =  cv2.adaptiveThreshold(eye,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,333,25)
    #cv2.imshow("     ",eye )
    cnts, hierarchy = cv2.findContours(eye,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) != 0:
        c = max(cnts, key = cv2.contourArea)
        (x,y),radius = cv2.minEnclosingCircle(c)
        center =(int(x),int(y))
        radius = int(radius)
        cv2.circle(eye2,center,radius,(0,0,255),2)

    masked[min[1]:max[1],min[0]:max[0]] = eye2
    cv2.imshow("",eye)
    return masked

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(grayscale)

    for face in faces:
        landmarks = predictor(grayscale,face)

        #rightline = cv2.line(frame,left_top,left_bottom,(0,255,0),2)
        #leftline = cv2.line(frame, right_top, right_bottom, (0, 255, 0), 2)

        left_eye = np.array([ [landmarks.part(36).x , landmarks.part(36).y],
                                        [landmarks.part(37).x, landmarks.part(37).y],
                                        [landmarks.part(38).x, landmarks.part(38).y],
                                        [landmarks.part(39).x, landmarks.part(39).y],
                                        [landmarks.part(40).x, landmarks.part(40).y],
                                        [landmarks.part(41).x, landmarks.part(41).y],
                                        ],np.int32)
        right_eye = np.array([ [landmarks.part(42).x , landmarks.part(42).y],
                                        [landmarks.part(43).x, landmarks.part(43).y],
                                        [landmarks.part(44).x, landmarks.part(44).y],
                                        [landmarks.part(45).x, landmarks.part(45).y],
                                        [landmarks.part(46).x, landmarks.part(46).y],
                                        [landmarks.part(47).x, landmarks.part(47).y],
                                        ],np.int32)

        right_Eye = eye(frame,right_eye)
        left_Eye = eye(frame,left_eye)
        cv2.imshow("frame",frame)
        cv2.imshow("r",right_Eye)
        cv2.imshow("l",left_Eye)
    key = cv2.waitKey(1)
    if key == 27:
        break