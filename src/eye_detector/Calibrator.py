from src.eye_detector.Calculator import Calculator

# 단위 시간동안의 좌표배열을 받아와 평균을 낸다.
#* outlier를 제거해야한다 *#

class Calibrator():
    def __init__(self):
        self.isCalibrated = False
        self.RX = []
        self.RY = []
        self.LX = []
        self.LY = []
        self.avgRX = -1.0
        self.avgRY = -1.0
        self.avgLX = -1.0
        self.avgLY = -1.0

    def calibrate(self,coords):
        cal = Calculator()
        if (self.isCalibrated == True):
            return True
        elif (coords[0] == 0 or coords[1] == 0 or coords[2] == 0 or coords[3] == 0):
            print("no eyes detected!")
            return
        else:

            self.RX.append(coords[0])
            self.RY.append(coords[1])
            self.LX.append(coords[2])
            self.LY.append(coords[3])

            if(len(self.LY) > 100):
                self.avgRX = cal.avg(self.RX)
                self.avgRY = cal.avg(self.RY)
                self.avgLX = cal.avg(self.LX)
                self.avgLY = cal.avg(self.LY)
                self.isCalibrated = True
                return False

    def reset(self):
        self.isCalibrated = False