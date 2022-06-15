# Think Mouse

### (2022.04 ~ 2022.06)

**2022년 1학기 신경공학 BCI Project**


----------
![image](https://user-images.githubusercontent.com/60168680/173652392-633a716b-bac7-45db-85eb-4ea73765d713.png)<br>
----------
**프로젝트 주제** : <br>시선추적 + 뇌파를 이용해 집중상태에서 마우스를 제어.


**기획 목적** :<br>수강신청, 티켓팅 등 극도로 긴장된 상태에서의 마우스 사용은 실수를 유발하기 때문에 시선추적과 뇌파를 이용해 실수를 줄이고자 한다.

**팀원**

|                            이름                             |              역할              |
| :---------------------------------------------------------: | :----------------------------: | 
|     [seungcholcho(조승철)](https://github.com/seungcholcho)     | 시선추적   |
| [hyejinHong0602(홍혜진)](https://github.com/hyejinHong0602) | 뇌파 데이터 분석 | 


## 1. BCI System의 기능
![image](https://user-images.githubusercontent.com/60168680/173656368-4b6769f0-5f61-4365-96a0-1cb93cd3e859.png)

## 2. 데이터 분석
![image](https://user-images.githubusercontent.com/60168680/173656572-0c099985-a3e8-486f-ba59-a0112b09082e.png)
![image](https://user-images.githubusercontent.com/60168680/173657682-24ccb9a6-a407-407a-bef5-f2424abfa23b.png)
![image](https://user-images.githubusercontent.com/60168680/173657693-d02b700b-aabc-4295-8a17-2a92865d89fe.png)

### 1) 세션별 클릭시점 앞뒤 5초 데이터 확인
![image](https://user-images.githubusercontent.com/60168680/173711722-f4b7a123-9fc1-4a27-a9c8-2fc2b9d17ac0.png)
![image](https://user-images.githubusercontent.com/60168680/173711919-2ae83927-7ceb-460c-a19c-92963efc1eed.png)
### 2) Analysis time / interval setting
![image](https://user-images.githubusercontent.com/60168680/173712489-71e8cc28-9a64-433a-b719-74061b79150f.png)
### 3) beta/theta 주파수 세부적으로 확인
-> beta/theta 영역에 대해 개인별 발현 주파수가 다를 수 있다고 해서 4hz단위, 2hz 단위로도 잘라서 확인해봤는데 최종적으로는 합쳐서 쓰는게 더 의미있다고 판단하여 beta는 12-40Hz, theta는 4-8Hz로 사용하였다.
![image](https://user-images.githubusercontent.com/60168680/173712567-f5db55f3-dc9e-4dda-a0fe-bbdad54cfcfa.png)


## 3. 데이터셋
1. MAVE에서 기록된 FFT된 데이터
![image](https://user-images.githubusercontent.com/60168680/173658866-684069ea-ccd4-41b2-92d3-b5ee68a0fe14.png)

2. 데이터 처리를 통해 직접 비교해 보고 싶은 주파수 대역별로 묶어 기록.
![image](https://user-images.githubusercontent.com/60168680/173658282-f69417cf-c373-4b09-b929-bd970a495379.png)
3. ERD/ERS 분석을 위해 Reference 대비 증감율을 기록. 
<br>ex) ratio_mu가 -0.16일 경우 클릭 전보다 클릭후 뮤파 16% 감소.
![image](https://user-images.githubusercontent.com/60168680/173658344-7fae0f5d-1c32-4dd9-964e-e93705b5fffe.png)



