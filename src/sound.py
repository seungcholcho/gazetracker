from tkinter import *
import datetime
import random
import time as t
import winsound

# 시작 시간으로 파일명 만들어주기 위함.
start_time = datetime.datetime.now()

# 클릭시간 저장할 배열.
click_time=[]
f = open("./seungchol/0610/"+str(start_time.year)+"-"+str(start_time.month)+"-"+str(start_time.day)+" "+str(start_time.hour)+"."+str(start_time.minute)+".txt","wt")

#f = open("./HyeJin/MMDD/"+str(start_time.year)+"-"+str(start_time.month)+"-"+str(start_time.day)+" "+str(start_time.hour)+"."+str(start_time.minute)+".txt","wt")

# 클릭했을 때 시간기록
def timecheck():
    current = datetime.datetime.now()
    click_time.append(str(current)+'\n')
    print(current)
    f.writelines(str(current)+'\n')
    tk.quit()


# ui에서 숫자 카운트 하는 함수
def countdown2sound():
    global time
    global k
    global count

    time += 1
    k -= 1
    # label["text"] = str(k)
    if time >= count:
        winsound.PlaySound("beep.wav", winsound.SND_FILENAME)
        return
    # print(time, count)
    tk.after(1000, countdown2sound)
    # tk.after(100, timecheck)

# tkinter 구성
tk = Tk()
tk.title("생각마우스")
tk.geometry("800x600")

# for문 j는 반복 set 변수. i는 1set에 수행하는 횟수 변수.
# Task : 1번씩 15set. 중간에 7초 휴식. countdown 시간 1-5초 랜덤.
for j in range(15):
    print(j + 1, "set")
    for i in range(1):
        k = random.randint(1, 5)  # k는 카운트 시간. 1-5초 랜덤.
        count = k
        print(k, "sec")
        time = 0

        # label = Label(tk, text=str(k), font=("나눔고딕", 45))
        # label.place(x=350, y=50)  # 카운트
        tk.after(1000, countdown2sound)

        button = Button(text="수강신청", bg='white', width=20, height=7, command=timecheck, font=("나눔고딕", 30, "bold"))
        button.pack()
        button.place(x=150, y=150)  # 예매하기 버튼. 누르면 시간 기록.

        tk.mainloop()

    t.sleep(7)  # set 사이에 rest time.
    continue
f.close()
