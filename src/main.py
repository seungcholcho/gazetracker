from src.eye_detector.Calculator import Calculator
from src.eye_detector.Calibrator import Calibrator
from src.eye_detector.PupilCoords import PupilCoords

import cv2
import dlib
import mouse
import os
import pandas as pd
import random

try:
    import Tkinter as tk
    from Tkinter import *
except:
    import tkinter as tk
    from tkinter import *

from PIL import Image, ImageTk


centerCalibrate = Calibrator()
leftCalibrate = Calibrator()
rightCalibrate = Calibrator()

topLeft = Calibrator()
top = Calibrator()
topRight = Calibrator()
left = Calibrator()
center = Calibrator()
bottomLeft = Calibrator()
bottom =Calibrator()
bottomRight = Calibrator()

calc = Calculator()
fd = PupilCoords()
cap = cv2.VideoCapture(0)

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None

        # 초기화면 설정..
        #     화면 목록
                # 0. StartPage: 시작 화면
                # 1. CameraCheck: 주의사항 및 카메라 확인
                # 2. CalibratingCenter
                # 3. CalibratingLeft
                # 4. CalibratingRight
                # 5. MouseControlPage: 마우스 제어 페이지 // 데이터 불러오기 잘 되는지 확인 하고 싶으면 self.switch_frame(MouseControlPage) 이용할 것.

        self.switch_frame(StartPage)
        # self.switch_frame(MouseControlPage)          #<<<< 데이터 불러오기 잘 되는지 확인 하고 싶으면 self.switch_frame(MouseControlPage) 이용할 것.
        #self.switch_frame(EndingPage)
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        frame = tk.Frame.__init__(self, master)
        tk.Label(self, text="ThinkMouse", width= 1920,font=('Helvetica', 50, "bold")).pack(side="top", fill= 'x',pady=50)
        self.image = Image.open('thinkmouse.png')
        self.image = self.image.resize((500,500))
        self.tkimg = ImageTk.PhotoImage(self.image)
        _label = tk.Label(self, text="thinkmouse", image=self.tkimg).pack()
        startbutton = tk.Button(self, text="Start!",font=('Helvetica', 30, "bold"),
                  command=lambda: master.switch_frame(CameraCheck)).pack(side="bottom",pady=50)

class CameraCheck(tk.Frame):
    def __init__(self, master):
        frame = tk.Frame.__init__(self, master)

        tk.Label(self, height = 5, width = 1920).pack(side ="top",fill='x')
        title = tk.Label(self, text = "주의사항!", font=("나눔고딕", 30, "bold")).pack()
        tk.Label(self, height=2, width=1920).pack(side="top", fill='x')
        text1 = tk.Label(self, text = "1. 머리를 움직이지 마세요!",font=("나눔고딕", 15)).pack()
        tk.Label(self, height=2, width=1920).pack(side="top", fill='x')
        text2 = tk.Label(self,font=("나눔고딕", 15), text = "2. etc...").pack()
        tk.Label(self, height=20, width=1920).pack(side="top", fill='x')
        endbutton = tk.Button(self, text="goto calibrating page",font=('Helvetica', 30, "bold"),
                  command=lambda: master.switch_frame(CalibratingCenter)).pack(side="bottom")

        #endbutton.place(x= 100,y=100)
        self.show_frames()

    def Camera(self):
        frame = cap.read()[1]
        frame = cv2.flip(frame, 1)
        eye_frame, coords = fd.pupil_coords(frame)

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        img = Image.fromarray(cv2image)
        # Convert image to PhotoImage
        imgtk = ImageTk.PhotoImage(image=img)
        return imgtk, coords

    def show_frames(self):
        label = tk.Label(self)
        img,coords = self.Camera()
        label.imgtk = img
        label.configure(image=img)
        print(coords)
        #label.pack()
        label.after(10, self.show_frames)
        #Repeat after an interval to capture continiously

class CalibratingCenter(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, height = 5, width = 1920).pack(side ="top",fill='x')
        tk.Label(self, text="Gaze Center", font=('Helvetica', 18, "bold")).pack(side="top", fill="x")
        tk.Label(self, height = 23, width = 1920).pack(side ="top",fill='x')

        self.center_text = tk.Button(self, text="X", font=('Helvetica', 50, "bold") ,command = lambda: self.Calibrate())
        self.center_text.pack()


    def Calibrate(self):
        while(centerCalibrate.isCalibrated == False):
            frame = cap.read()[1]
            frame = cv2.flip(frame, 1)
            eye_frame, coords = fd.pupil_coords(frame)
            centerCalibrate.calibrate(coords)

        print("calibration Complete!")
        print(centerCalibrate.avgLX, centerCalibrate.avgLY, centerCalibrate.avgRX, centerCalibrate.avgRY)
        self.newbutton = tk.Button(self, text="Calibration Done! continue to Left control your Cursor!", font=('Helvetica', 30, "bold") ,command=lambda: self.master.switch_frame(CalibratingLeft))
        self.newbutton.pack()

class CalibratingLeft(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, height = 5, width = 1920).pack(side ="top",fill='x')
        tk.Label(self, text="Gaze Left", font=('Helvetica', 18, "bold")).pack(side="top", fill="x")
        tk.Label(self, height = 23, width = 1920).pack(side ="top",fill='x')

        self.center_text = tk.Button(self, text="X", font=('Helvetica', 30, "bold") ,command = lambda: self.Calibrate())
        self.center_text.pack(side="left")

    def Calibrate(self):
        while (leftCalibrate.isCalibrated == False):
            frame = cap.read()[1]
            frame = cv2.flip(frame, 1)
            eye_frame, coords = fd.pupil_coords(frame)
            leftCalibrate.calibrate(coords)

        print("calibration Complete!")
        print(leftCalibrate.avgLX, leftCalibrate.avgLY, leftCalibrate.avgRX, leftCalibrate.avgRY)
        self.newbutton = tk.Button(self, text="Calibration Done! continue to Right Calibration!",
                                   font=('Helvetica', 30, "bold"),
                                   command=lambda: self.master.switch_frame(CalibratingRight))
        self.newbutton.pack(side="left",anchor = "center")

class CalibratingRight(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, height=5, width=1920).pack(side="top", fill='x')
        tk.Label(self, text="Gaze Right", font=('Helvetica', 18, "bold")).pack(side="top", fill="x")
        tk.Label(self, height=23, width=1920).pack(side="top", fill='x')

        self.center_text = tk.Button(self, text="X", font=('Helvetica', 50, "bold"), command=lambda: self.Calibrate())
        self.center_text.pack(side="right")

    def Calibrate(self):
        while (rightCalibrate.isCalibrated == False):
            frame = cap.read()[1]
            frame = cv2.flip(frame, 1)
            eye_frame, coords = fd.pupil_coords(frame)
            rightCalibrate.calibrate(coords)

        print("calibration Complete!")
        print(rightCalibrate.avgLX, rightCalibrate.avgLY, rightCalibrate.avgRX, rightCalibrate.avgRY)
        self.newbutton = tk.Button(self, text="Calibration Done! continue to control your Cursor!!",
                                   font=('Helvetica', 50, "bold"),
                                   command=lambda: self.master.switch_frame(MouseControlPage))
        self.newbutton.pack()

condition = True
clicks = 0
initial = 0
iter = 0

class MouseControlPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.resizable=(False,False)
        self.after(1000, self.getPupil())

    def click(self):
        global clicks
        clicks = clicks + 1
        print(clicks)

    def start(self):
        global condition
        condition = True

    def stop(self):
        global condition
        condition = False

    def moveMouse(self, coords):
        LX = coords[0]
        LY = coords[1]
        RX = coords[2]
        RY = coords[3]

        dist_left = abs(LX - leftCalibrate.avgLX) + abs(RX - leftCalibrate.avgRX)
        dist_center = abs(LX - centerCalibrate.avgLX) + abs(RX-centerCalibrate.avgRX)
        dist_right = abs(LX - rightCalibrate.avgLX) + abs(RX-rightCalibrate.avgRX)

        dist = [dist_left,dist_center,dist_right]
        temp = min(dist)
        gazewhere = dist.index(temp)
        print(dist)
        if gazewhere == 0:
            print("looking left")
            mouse.move(200, 800, absolute=True, duration=0.2)
        elif gazewhere ==1:
            print("looking center")
            mouse.move(960, 800, absolute=True, duration=0.2)
        elif gazewhere ==2:
            print("looking right")
            mouse.move(1800, 800, absolute=True, duration=0.2)


    def getPupil(self):
        global initial
        global clicks

        master_width = 90
        master_height = 20
        random_list = [1,3,5]
        random.shuffle(random_list)

        if clicks > 0:
            self.master.switch_frame(EndingPage)

        if initial == 0:
            tk.Label(self, height = 5).grid(row = 0, column=0)
            tk.Label(self, height =5,text="과목명", font=("나눔고딕", 15, "bold")).grid(row=1, column=0)
            tk.Label(self, width= 10).grid(row=1, column=0)
            tk.Label(self, text="세계신화의\n이해", font=("나눔고딕", 15, "bold")).grid(row=1, column=1)
            tk.Label(self, width = master_width-20).grid(row=1, column=2)
            tk.Label(self, text="사고와표현", font=("나눔고딕", 15, "bold")).grid(row=1, column=3)
            tk.Label(self, width = master_width).grid(row=1, column=4)
            tk.Label(self, text="신경공학", font=("나눔고딕", 15, "bold")).grid(row=1, column=5)

            tk.Label(self, text="학수번호", font=("나눔고딕", 15, "bold")).grid(row=2, column=0)
            tk.Label(self, text="HALF0302", font=("나눔고딕", 15, "bold")).grid(row=2, column=1)
            tk.Label(self, text="HALR1032", font=("나눔고딕", 15, "bold")).grid(row=2, column=3)
            tk.Label(self, text="HAIE0019", font=("나눔고딕", 15, "bold")).grid(row=2, column=5)


            tk.Label(self, text="학년", font=("나눔고딕", 15, "bold")).grid(row=3, column=0)
            tk.Label(self, text="전체", font=("나눔고딕", 15, "bold")).grid(row=3, column=1)
            tk.Label(self, text="1학년", font=("나눔고딕", 15, "bold")).grid(row=3, column=3)
            tk.Label(self, text="3학년", font=("나눔고딕", 15, "bold")).grid(row=3, column=5)

            tk.Label(self, text="학점", font=("나눔고딕", 15, "bold")).grid(row=4, column=0)
            tk.Label(self, text="3학점", font=("나눔고딕", 15, "bold")).grid(row=4, column=1)
            tk.Label(self, text="3학점", font=("나눔고딕", 15, "bold")).grid(row=4, column=3)
            tk.Label(self, text="3학점", font=("나눔고딕", 15, "bold")).grid(row=4, column=5)

            tk.Label(self, text="수업내용", height = master_height, font=("나눔고딕", 15, "bold")).grid(row=5, column=0)
            tk.Label(self, text="본 교과목의 대표\n핵심 역량은'다양성\n존중 역량'이다.\n인문학의 원형인 신화를\n통해 다양한 학문과 예술,\n그리고 제반 문화 현상을\n살펴봄으로써, 다양성의\n가치를 존중하고\n자신과 다른 사람이나\n문화에 대해 배려하고\n존중하는 역량 함양을\n목표로 한다.", height=master_height, font=("나눔고딕", 13)).grid(row=5, column=1)
            tk.Label(self, text="1. <사고와 표현>\n 수업에서는 학생들이\n현대 사회의 지식인,\n전문인으로서 필요한\n비판적 사고력과 표현력을\n갖출 수 있도록 한다.\n곧 주어진 정보를 있는\n그대로 수용하지 않고\n비판적으로 논리적으로\n사고하여 문제 해결에\n필요한 정보를 선별하는\n능력을 기르고, 목적에\n부합하는 올바른 형식과\n표현을 갖춘 글을\n쓸 수 있고 그것을\n말로 표현할 수 있는\n능력을 기르도록 한다.\n\n2. 본 교과목의 대표\n핵심역량은 전문지식 탐구\n역량으로 본 교과에서는\n전문적인 자료나 지식을\n조사하고 학습할 수\n있는 지식 습득, 지식의\n핵심 원리나 의미를\n명확히 이해할 수\n있는 지식 이해, 학습한\n지식을 글과 말로 표현할\n수 있는 지식 활동,\n수업에서 배운 지식을\n전공이나 사회문제를 해결하는\n데 활용할 수 있는 현실\n문제 적용 등의 역량을\n강화하고자 한다.", height=master_height, font=("나눔고딕", 13)).grid(row=5, column=3)
            tk.Label(self, text="인공지능의 주가 되는\n인간의 뇌 정보처리를\n실증적으로 체험하고\n뇌-컴퓨터 인터페이스에\n기초한 휴먼지능시스템\n구현을 통한 인공지능의\n기초 및 응용지식 습득을\n목적으로 함.  ", height=master_height, font=("나눔고딕", 13)).grid(row=5, column=5)

            tk.Button(self, text="수강신청", font=("나눔고딕", 15, "bold"), command=lambda: self.click()).grid(row=6, column=random_list[0])
            tk.Label(self, text="", font=("나눔고딕", 15, "bold")).grid(row=6, column=random_list[1])
            tk.Label(self, text="", font=("나눔고딕", 15, "bold")).grid(row=6, column=random_list[2])

        initial = 1

        global condition
        if condition:
            frame = cap.read()[1]
            frame = cv2.flip(frame, 1)
            eye_frame, coords = fd.pupil_coords(frame)

            self.moveMouse(coords)
            self.clicker()
            self.after(100,self.getPupil)


    def clicker(self):

        import winsound
        global iter
        iter = iter + 1

        if(iter == 20):
            winsound.PlaySound("beep.wav", winsound.SND_FILENAME)
            print("BEEP!")

        if(iter > 40):
            self.master.switch_frame(FailurePage)

        if self.ERDERS() ==True :
            winsound.PlaySound("click.wav", winsound.SND_FILENAME)
            print("BEEP!")
            mouse.click()


    def ERDERS(self):
        print("hello")

        # 마지막 x 행 만큼의 데이터를 불러옴
        latest_data = self.getData()

        # read real time data
        # read trained data

        # data preprocessing
        latest_data['mu8-12'] = 0
        latest_data['theta4-8'] = 0
        latest_data['beta12-40'] = 0
        for i in range(1, len(latest_data.columns) - 4):  # df.columns[i][:-2] -> 헤르츠 정보
            # 마지막 컬럼 세개가 mu,theta,beta 여서 그거 제외한거(-4)
            if float(latest_data.columns[i][:-2]) >= 8 and float(latest_data.columns[i][:-2]) < 12:  # 뮤파
                latest_data['mu8-12'] += latest_data[latest_data.columns[i]]
            elif float(latest_data.columns[i][:-2]) >= 4 and float(latest_data.columns[i][:-2]) < 8:  # 세타파
                latest_data['theta4-8'] += latest_data[latest_data.columns[i]]
            elif float(latest_data.columns[i][:-2]) >= 12 and float(latest_data.columns[i][:-2]) < 40:  # 베타파
                latest_data['beta12-40'] += latest_data[latest_data.columns[i]]

        # latest_data[latest_data.columns[-3:]] # 제일 끝 4초 동안의 mu8-12 / theta8-12 / beta 12-40
        df_clean = latest_data[latest_data.columns[-3:]]

        # 뮤 증감율/세타 증감율/베타 증감율 구하기
        ref_mu = df_clean[0:2].mean()[0]
        after_mu = df_clean[2:4].mean()[0]
        ratio_mu = (after_mu - ref_mu) / ref_mu

        ref_theta = df_clean[0:2].mean()[1]  # 앞에 3초 데이터
        after_theta = df_clean[2:4].mean()[1]  # 클릭 포함 데이터
        ratio_theta = (after_theta - ref_theta) / ref_theta

        ref_beta = df_clean[0:2].mean()[2]  # 앞에 3초 데이터
        after_beta = df_clean[2:4].mean()[2]  # 클릭 포함 데이터
        ratio_beta = (after_beta - ref_beta) / ref_beta
        print(ratio_mu,ratio_beta, ratio_theta)

        #check threshhold
        if ratio_mu < 0 and ratio_theta < 0 and ratio_beta > 0:
            # 조건을 일단은 크게 mu는 감소, theta는 감소, beta는 증가하면 이걸 클릭으로 판단하겠다고 정해놓은것.
            # 보면서 조건이 수정되면 여기 값들을 바꿔주면 됨.
            print('True')
            return True
        else:
            print('False')
            return False

    def getData(self):
        path = 'C:/MAVE_RawData/'
        file_list = os.listdir(path)

        # 디렉토리에 파일이 저장되어있는 순서에 따라서 file_list의 순서가 바뀜
        # 실제 파일에 정렬되어있는 순서와 다를 수 있으니 file_list 출력 확인할 것
        # 가장 최근 데이터의 인덱스를 찾을 것.

        print(file_list)
        # 보통 마지막 인덱스에 가장 최근 파일이 저장되어있음.
        latest_file = file_list[len(file_list)-1]

        data_list = os.listdir(path+latest_file+'/')
        data_path = path + latest_file + '/' + 'Fp1_FFT.txt'

        df = pd.read_table(data_path, sep='\t',
                           encoding='cp949')

        # df.tail(int x)  마지막 x 행만큼의 데이터를 불러옴.
        latest_data = df.tail(4)
        return latest_data

class FailurePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        global condition
        global clicks
        global initial

        condition = False
        clicks = 0
        initial = 0

        master_x = 20
        master_y = 20
        tk.Label(self, width = master_x, height= master_y, font=("나눔고딕", 50, "bold"),text="실패!").pack(side="top", fill= 'x',pady=50)

class EndingPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        global condition
        global clicks
        global initial

        condition = False
        clicks = 0
        initial = 0

        master_x = 20
        master_y = 20
        tk.Label(self, width = master_x, height= master_y, font=("나눔고딕", 50, "bold"),text="성공!").pack(side="top", fill= 'x',pady=50)

if __name__ == "__main__":
    app = SampleApp()
    app.title("생각마우스")
    app.geometry("1920x1080")
    app.attributes('-fullscreen',True)
    app.mainloop()