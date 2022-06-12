from datetime import datetime
import pandas as pd
from time import sleep

now = datetime.now()

# 파일 이름 만들어주기
if int(now.hour) > 12:
    hour = int(now.hour)-12
    file_name = now.strftime('%Y-%m-%d_'+'오후 '+str(hour)+'_%M')
elif int(now.hour) == 12:
    file_name = now.strftime('%Y-%m-%d_'+'오후 '+'%H_%M')
else :
    file_name = now.strftime('%Y-%m-%d_'+'오전 '+'%H_%M')

f = open("C:/MAVE_RawData/"+file_name+"/Fp1_FFT.txt", "r")
# 실시간으로 recording 되고 있는 뇌파 전체 가져와서 데이터프레임에 바로 넣기.
# 파일명이 지금 시간인걸 가져오도록 했으니까 MAVE 시작 타임이랑 프로그램 시작 시간 맞춰줘야하는거 주의하기.

while True:
    realtime_df = pd.read_table("C:/MAVE_RawData/"+file_name+"/Fp1_FFT.txt",sep='\t',encoding = 'cp949')
#     new   _df = pd.DataFrame(data)
#     line = f.readline().strip()
    print(realtime_df)
    print('-----')
    sleep(1) # 있어도 되고 없어도 됨. sleep(1)로 해주면 1초마다 가져오고, 안해주면 그냥 무한루프 돌면서 계속 가져옴.
