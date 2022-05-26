import cv2
import numpy as np
import dlib
import mouse

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# switch to 1 after calibration
calibrated = 0

RX = []
RY = []
LX = []
LY = []

right_eye_coordinates = []
left_eye_coordinates = []

def mindetector(arr):
    min_x = 1000
    min_y = 1000
    for x in range(0, 5):
        temp_x = arr[x][0]
        temp_y = arr[x][1]
        if (temp_x < min_x):
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

#이진화된 eye(GrayScale)와 출력할 화면(BGR)을 전달받는다. 동공의 좌표를 반환한다.
def pupildetector(eye):
    x = 0
    y = 0
    radius = 0
    output = cv2.cvtColor(eye,cv2.COLOR_GRAY2BGR)
    cnts, thierarchy = cv2.findContours(eye,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(cnts) != 0:
        c = max(cnts,key = cv2.contourArea)
        (x,y),radius = cv2.minEnclosingCircle(c)
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(output,center,1,(255,0,0),1)
        output = cv2.resize(output,(0,0),fx=10,fy=10,interpolation= cv2.INTER_AREA)
        #print(x,y)
        cv2.imshow("pupil detected",output)
    #동공의 좌표 return
    return x,y,radius

#눈 영역을 검출하여 이진화 후 반환한다.
def eye(img,arr):
    min = mindetector(arr)
    max = maxdetector(arr)
    mask = np.zeros_like(img)

    kernel = np.ones((1,1),np.uint8)
    cv2.rectangle(mask, min, max, (255, 255, 255), -1)
    masked = cv2.bitwise_and(frame, mask)
    masked = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)

    '''if(min[1]+6>=max[1]):
        temp = min[1]
    else:
        temp = min[1]+6'''

    eye = masked[min[1]:max[1],min[0]:max[0]]
    eye = cv2.bitwise_not(eye)

    #cv2.imshow("before binarize", eye)
    #이진화
    _,eye = cv2.threshold(eye,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)

    #침식을 통한 세선화..?

    kernel = np.ones((3,3), np.uint8)
    #cv2.imshow("before erode", eye)
    eye = cv2.erode(eye, kernel, iterations=5)
    eye = cv2.dilate(eye, kernel, iterations=1)
    #cv2.imshow("after erode",eye)
    x,y,r = pupildetector(eye)


    #동공좌표 찍기
    output = eye
    output = cv2.cvtColor(eye, cv2.COLOR_GRAY2BGR)
    #cv2.circle(output, (int(x),int(y)), r, (255, 0, 0), 2)
    cv2.circle(output, (int(x),int(y)), 1, (255, 0, 0), 1)

    masked = cv2.cvtColor(masked, cv2.COLOR_GRAY2BGR)
    masked[min[1]:max[1],min[0]:max[0]] = output

    return masked, int(x), int(y)

def pupil_coordinates():
    global _, frame, key
    RX = []
    RY = []
    LX = []
    LY = []
    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)


        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(grayscale)
        for face in faces:

            landmarks = predictor(grayscale, face)
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
            right_Eye, rx, ry = eye(frame, right_eye)
            left_Eye, lx, ly = eye(frame, left_eye)
            eyes = cv2.bitwise_or(right_Eye, left_Eye)
            temp = cv2.bitwise_or(eyes,frame)
            if calibrated == 0:
                RX.append(rx)
                RY.append(ry)
                LX.append(lx)
                LY.append(ly)
            else:
                i = float(rx) - center_gaze.avgRX
                j = float(ry) - center_gaze.avgRY
                k = float(lx) - center_gaze.avgLX
                l = float(ly) - center_gaze.avgLY

                if((i>0)and(j<0)and(k>0)and(l<0)):
                    print("_____________________________________________________________________________")
                    print("avg LX,LY: ", center_gaze.avgLX, center_gaze.avgLY, "avg RX,RY: ", center_gaze.avgRX,
                          center_gaze.avgRY)
                    print("(LX,LY): ", lx, ly, " (RX,RY): ", rx, ry)
                    print("upper right")
                    mouse.move(1340,270, absolute=True, duration=0)

                elif((i<0)and(j<0)and(k<0)and(l<0)):
                    print("_____________________________________________________________________________")
                    print("avg LX,LY: ", center_gaze.avgLX, center_gaze.avgLY, "avg RX,RY: ", center_gaze.avgRX,
                          center_gaze.avgRY)
                    print("(LX,LY): ", lx, ly, " (RX,RY): ", rx, ry)
                    print("upper left")
                    mouse.move(480,270, absolute=True, duration=0)

                elif  ((i<0)and(j>0)and(k<0)and(l>0)):
                    print("_____________________________________________________________________________")
                    print("avg LX,LY: ", center_gaze.avgLX, center_gaze.avgLY, "avg RX,RY: ", center_gaze.avgRX,
                          center_gaze.avgRY)
                    print("(LX,LY): ", lx, ly, " (RX,RY): ", rx, ry)
                    print("lower left")
                    mouse.move(480,810, absolute=True, duration=0)

                elif ((i>0)and(j>0)and(k>0)and(l>0)):
                    print("_____________________________________________________________________________")
                    print("avg LX,LY: ", center_gaze.avgLX, center_gaze.avgLY, "avg RX,RY: ", center_gaze.avgRX,
                          center_gaze.avgRY)
                    print("(LX,LY): ", lx, ly, " (RX,RY): ", rx, ry)
                    print("lower right")
                    mouse.move(1340,810, absolute=True, duration=0)

            cv2.imshow("frame", frame)
            cv2.imshow("eyes", eyes)
            cv2.imshow("      ",temp)

        key = cv2.waitKey(1)
        if key == 27 or key == 'x':
            break
    return RX, RY, LX, LY

def avg(arr):
    sum = 0
    for i in arr:
        sum += i
    avg = sum/len(arr)
    return avg

class calibrator():
    def __init__(self,RX,RY,LX,LY):
        self.RX = RX
        self.RY = RY
        self.LX = LX
        self.LY = LY
        self.avgRX = avg(RX)
        self.avgRY = avg(RY)
        self.avgLX = avg(LX)
        self.avgLY = avg(LY)


print("CAUTION: don't move your head!")


#input('press any key to start!')
print("gaze center ***************")
input('press any key when you are ready...')
print("calibrating....")
RX, RY, LX, LY = pupil_coordinates()
center_gaze = calibrator(RX, RY, LX, LY)

print("gaze up ***************")
input('press any key when you are ready...')
print("calibrating....")
RX, RY, LX, LY = pupil_coordinates()
up_gaze = calibrator(RX, RY, LX, LY)

print("gaze down ***************")
input('press any key when you are ready...')
print("calibrating....")
RX, RY, LX, LY = pupil_coordinates()
down_gaze = calibrator(RX, RY, LX, LY)

calibrated = 1


print(up_gaze.avgLX," ",up_gaze.avgLY," ",up_gaze.avgRX," ",up_gaze.avgRY)
print(down_gaze.avgLX," ",down_gaze.avgLY," ",down_gaze.avgRX," ",down_gaze.avgRY)

#pupil_coordinates()
