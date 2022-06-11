from src.eye_detector.Calculator import Calculator
from src.eye_detector.Calibrator import Calibrator
from src.eye_detector.PupilCoords import PupilCoords

import cv2
import dlib
import mouse

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
        #self.switch_frame(StartPage)
        #self.switch_frame(Cali1)
        self.switch_frame(MouseControlPage)
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
        tk.Label(self, height=40, width=1920).pack(side="top", fill='x')
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
        self.newbutton = tk.Button(self, text="Calibration Done! continue to Left control your Cursor!", font=('Helvetica', 50, "bold") ,command=lambda: self.master.switch_frame(CalibratingLeft))
        self.newbutton.pack()

class CalibratingLeft(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, height = 5, width = 1920).pack(side ="top",fill='x')
        tk.Label(self, text="Gaze Left", font=('Helvetica', 18, "bold")).pack(side="top", fill="x")
        tk.Label(self, height = 23, width = 1920).pack(side ="top",fill='x')

        self.center_text = tk.Button(self, text="X", font=('Helvetica', 50, "bold") ,command = lambda: self.Calibrate())
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
                                   font=('Helvetica', 50, "bold"),
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

class Cali1(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.center_text = tk.Button(self, text="X", font=('Helvetica', 50, "bold") ,command = lambda: self.Calibrate())
        self.center_text.pack(anchor ="nw")

    def Calibrate(self):
        while(topLeft.isCalibrated == False):
            frame = cap.read()[1]
            frame = cv2.flip(frame, 1)
            eye_frame, coords = fd.pupil_coords(frame)
            topLeft.calibrate(coords)

        print("calibration Complete!")
        print(topLeft.avgLX, topLeft.avgLY, topLeft.avgRX, topLeft.avgRY)
        self.newbutton = tk.Button(self, text="Calibration Done! continue!", font=('Helvetica', 50, "bold") ,command=lambda: self.master.switch_frame(Cali2))
        self.newbutton.pack()

class Cali2(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.center_text = tk.Button(self, text="X", font=('Helvetica', 50, "bold") ,command = lambda: self.Calibrate())
        self.center_text.pack()


    def Calibrate(self):
        while(topLeft.isCalibrated == False):
            frame = cap.read()[1]
            frame = cv2.flip(frame, 1)
            eye_frame, coords = fd.pupil_coords(frame)
            top.calibrate(coords)

        print("calibration Complete!")
        print(top.avgLX, top.avgLY, top.avgRX, top.avgRY)
        self.newbutton = tk.Button(self, text="Calibration Done! continue to Left control your Cursor!", font=('Helvetica', 50, "bold") ,command=lambda: self.master.switch_frame(Cali3))
        self.newbutton.pack()

class Cali3(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.center_text = tk.Button(self, text="X", font=('Helvetica', 50, "bold"), command=lambda: self.Calibrate())
        self.center_text.pack(anchor = "ne")

    def Calibrate(self):
        while (topLeft.isCalibrated == False):
            frame = cap.read()[1]
            frame = cv2.flip(frame, 1)
            eye_frame, coords = fd.pupil_coords(frame)
            top.calibrate(coords)

        print("calibration Complete!")
        print(top.avgLX, top.avgLY, top.avgRX, top.avgRY)
        self.newbutton = tk.Button(self, text="Calibration Done! continue to Left control your Cursor!",
                                   font=('Helvetica', 50, "bold"), command=lambda: self.master.switch_frame(Cali3))
        self.newbutton.pack()


condition = True
clicks = 0

class MouseControlPage(tk.Frame):
    def click(self):
        global clicks
        clicks = clicks + 1
        print(clicks)

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.resizable=(False,False)

        tk.Button(self, text="stop control",command=lambda:self.stop()).grid(row =0, column = 1)
        tk.Button(self, text="start control",command=lambda:self.start()).grid(row =0, column = 0)
        tk.Label(self, text="과목명", font=("나눔고딕", 15, "bold")).grid(row =1, column = 0)
        tk.Label(self, text="과목 1", font=("나눔고딕", 15, "bold")).grid(row =1, column = 1)
        tk.Label(self, text="                                                                   ", font=("나눔고딕", 15,)).grid(row=1, column=2)
        tk.Label(self, text="과목 2", font=("나눔고딕", 15, "bold")).grid(row =1, column = 3)
        tk.Label(self, text="                                                                   ", font=("나눔고딕", 15,)).grid(row=1, column=4)
        tk.Label(self, text="과목 3", font=("나눔고딕", 15, "bold")).grid(row=1, column=5)
        tk.Label(self, text="학수번호", font=("나눔고딕", 15, "bold")).grid(row=2, column=0)
        tk.Label(self, text="학년", font=("나눔고딕", 15, "bold")).grid(row=3, column=0)
        tk.Label(self, text="학점", font=("나눔고딕", 15, "bold")).grid(row=4, column=0)
        tk.Button(self, text="수강신청", font=("나눔고딕", 15, "bold"), command=lambda: self.click()).grid(row=5, column=1)
        tk.Button(self, text="수강신청", font=("나눔고딕", 15, "bold"), command=lambda: self.click()).grid(row=5, column=2)
        tk.Button(self, text="수강신청", font=("나눔고딕", 15, "bold"), command=lambda: self.click()).grid(row=5, column=3)

        #self.after(1000, self.getPupil())


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
            mouse.move(480, 540, absolute=True, duration=0.2)
        elif gazewhere ==1:
            print("looking center")
            mouse.move(960, 540, absolute=True, duration=0.2)
        elif gazewhere ==2:
            print("looking right")
            mouse.move(1440, 540, absolute=True, duration=0.2)
        # if (LX < centerCalibrate.avgLX and RX < centerCalibrate.avgRX):
        #     print("<<<looking left")
        #     mouse.move(480, 540, absolute=True, duration=0.2)
        # elif (RX > centerCalibrate.avgRX and LX > centerCalibrate.avgLX):
        #     print("looking right>>>")
        #     mouse.move(1440, 540, absolute=True, duration=0.2)
        # else:
        #     print("nothing found!")

        print("it checks the conditions")
    def getPupil(self):
        global condition
        if condition:
            frame = cap.read()[1]
            frame = cv2.flip(frame, 1)
            eye_frame, coords = fd.pupil_coords(frame)
            print("is looping? and checks the Conditions?")
            self.moveMouse(coords)
            #self.clicker()
            self.after(100,self.getPupil)

    def clicker(self):
        print("is ERD/ERS?")
        #if ERD/ERS() ==True : mouse.click

    def ERDERS(self):
        print("hello")
        #read real time data
        #read trained data
        #check threshhold



if __name__ == "__main__":
    app = SampleApp()
    app.title("생각마우스")
    app.geometry("1920x1080")
    app.attributes('-fullscreen',True)
    app.mainloop()