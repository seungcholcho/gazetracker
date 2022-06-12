# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from time import sleep

data = [] # data 저장 배열
address = 'C:/MAVE_RawData/2022-05-31_오후 4_20' # 데이터 저장 경로
#sleep(5)


# ↓ 무시
def draw_graph(data):
    #ecg = np.loadtxt(file,delimiter="\t",unpack=False)
    # x축
    time = data[:, 0]
    # y축
    amplitude = data[:, 1]

    # plot 세팅
    plt.figure(num=1, dpi=100, facecolor='white')
    plt.plot(time, amplitude, color="blue", linewidth=0.5)

    plt.title('ecg')
    plt.xlabel('time')
    plt.ylabel('amplitude')
    plt.xlim(1, 1204)
    plt.ylim(-0.0003, 0.0003)

    plt.show()

#여기서부터
delay_time_1 = 0 # 딜레이 시간
with open(r"C:\MAVE_RawData\2022-06-08_오후 2_59\Fp1_FFT.txt","r") as f:  # mave뇌파 recoding 후 파일 경로 설정
    while True:
        where = f.tell()
        line = f.readline().strip().replace('오후','').split(sep='\t',maxsplit=641)
        # 한줄씩 읽기 / FFT에 '오후' 때문에 그래프 안그려져서 없앰. split tab기준으로 641번 쪼갬.
        if not line or line == ['']:
            sleep(0.1)
            delay_time_1 += 0.1
            f.seek(where)
            if delay_time_1 > 1.5:
                print("Delay has benn exceed.")
                break
        else:
            delay_time_1 = 0
            print(line)
            data.append(line)
            df = pd.DataFrame(data)
            #df.to_csv(address + '/test1.csv', sep='\t', index=False)
            #draw_graph(data)