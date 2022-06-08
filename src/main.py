from src.eye_detector.Calculator import Calculator
from src.eye_detector.Calibrator import Calibrator
from src.eye_detector.PupilCoords import PupilCoords

import cv2
import dlib
import mouse

try:
    import Tkinter as tk
except:
    import tkinter as tk
from PIL import Image, ImageTk


centerCalibrate = Calibrator()
leftCalibrate = Calibrator()
rightCalibrate = Calibrator()

calc = Calculator()
fd = PupilCoords()
cap = cv2.VideoCapture(0)

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Label(self, text="ThinkMouse", font=('Helvetica', 50, "bold")).pack(side="top", fill="y", pady=50)
        self.image = Image.open('thinkmouse.png')
        self.image = self.image.resize((500,500))
        self.tkimg = ImageTk.PhotoImage(self.image)
        _label = tk.Label(self, text="thinkmouse", image=self.tkimg)
        _label.pack(pady = 30)
        tk.Button(self, text="Start!",
                  command=lambda: master.switch_frame(CameraCheck)).pack(pady = 20)
        tk.Button(self, text="Go to page two",
                  command=lambda: master.switch_frame(PageTwo)).pack(pady = 20)


class CameraCheck(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        endbutton = tk.Button(self, text="goto calibrating page",
                  command=lambda: master.switch_frame(CalibratingPage))
        tk.Label(self, text = "주의사항!", font=("나눔고딕", 30, "bold")).pack()
        tk.Label(self, text = "1. 머리를 움직이지 마세요!").pack()
        tk.Label(self, text = "2. etc...").pack()
        endbutton.pack()

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
        label.pack()
        label.after(10, self.show_frames)
        #Repeat after an interval to capture continiously

class CalibratingCenter(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #tk.Label(self, text="Gaze Center", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        #tk.Button(self, text="Click When Complete!", command=lambda: master.switch_frame(CalibratingPage)).pack()
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
        #self.newbutton = tk.Button(self, text="Calibration Done! continue to Left Calibration!", font=('Helvetica', 50, "bold") ,command = lambda: self.master.switch_frame(CalibratingLeft))
        self.newbutton = tk.Button(self, text="Calibration Done! continue to Left control your Cursor!", font=('Helvetica', 50, "bold") ,command=lambda: self.master.switch_frame(MouseControlPage))


        self.newbutton.pack()

class CalibratingLeft(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        # tk.Label(self, text="Gaze Center", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        # tk.Button(self, text="Click When Complete!", command=lambda: master.switch_frame(CalibratingPage)).pack()
        self.center_text = tk.Button(self, text="X", font=('Helvetica', 50, "bold"), command=lambda: self.Calibrate())
        self.center_text.pack(side = "top", anchor = "center")

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
        self.center_text = tk.Button(self, text="X", font=('Helvetica', 50, "bold"), command=lambda: self.Calibrate())
        self.center_text.pack()

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


class CalibratingPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Page two", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Calibrate Center",
                  command=lambda: master.switch_frame(CalibratingCenter)).pack()
        tk.Button(self, text = "Calibrate Left",command=lambda: master.switch_frame(CalibratingLeft)).pack()
        tk.Button(self, text = "Calibrate Right",command=lambda: master.switch_frame(CalibratingRight)).pack()
        tk.Button(self, text = "reset all settings",command=lambda:self.reset()).pack()

    def reset(self):
        centerCalibrate.reset()
        leftCalibrate.reset()
        rightCalibrate.reset()

class MouseControlPage(tk.Frame):
    def __init__(self, master):
        frame = cap.read()[1]
        frame = cv2.flip(frame, 1)
        eye_frame, coords = fd.pupil_coords(frame)

        LX = coords[0]
        LY = coords[1]
        RX = coords[2]
        RY = coords[3]

        tk.Frame.__init__(self, master)
        tk.Button(self, text="end control",command=lambda:master.switch_frame(StartPage)).pack()

        while True:
            if(LX<centerCalibrate.avgLX and RX<centerCalibrate.avgRX):
                mouse.move(50,50,absolute=True)
            elif(RX>centerCalibrate.avgRX and LX<centerCalibrate.avgLX):
                mouse.move(100,100,absolute=False)


if __name__ == "__main__":
    app = SampleApp()
    app.title("생각마우스")
    app.geometry("1920x1080")
    app.attributes('-fullscreen',True)
    app.mainloop()