from tkinter import *
import datetime
import random
import time as t


# 클릭했을 때 시간기록

def timecheck():
    current = datetime.datetime.now()
    print(current)
    tk.quit()


# ui에서 숫자 카운트 하는 함수
def countdown():
    # k = random.randint(1, 5)
    # count = k
    # print(k)
    # time = 0
    global time
    global k
    global count

    time += 1
    k -= 1
    label["text"] = str(k)
    if time >= count:
        return
    # print(time, count)
    tk.after(1000, countdown)
    # tk.after(100, timecheck)


# tkinter 구성
tk = Tk()
tk.title("생각마우스")
tk.geometry("800x600")

# 4. 1번씩 25set. 중간에 10초 휴식. countdown 시간 1-5초 랜덤.
for j in range(25):
    print(j + 1, "set")
    for i in range(1):
        k = random.randint(1, 5)  # k는 카운트 시간. 1-5초 랜덤.
        count = k
        print(k, "sec")
        time = 0

        label = Label(tk, text=str(k), font=("나눔고딕", 45))
        label.place(x=350, y=50)  # 카운트
        tk.after(1000, countdown)

        button = Button(text="예매하기", bg='white', width=20, height=7, command=timecheck, font=("나눔고딕", 30, "bold"))
        button.pack()
        button.place(x=150, y=150)  # 예매하기 버튼. 누르면 시간 기록.

        tk.mainloop()

    t.sleep(10)  # set 사이에 rest time.
    continue
