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

## 3. 데이터셋
1. MAVE에서 기록된 FFT된 데이터
![image](https://user-images.githubusercontent.com/60168680/173658866-684069ea-ccd4-41b2-92d3-b5ee68a0fe14.png)

2. 데이터 처리를 통해 직접 비교해 보고 싶은 주파수 대역별로 묶어 기록.
![image](https://user-images.githubusercontent.com/60168680/173658282-f69417cf-c373-4b09-b929-bd970a495379.png)
3. ERD/ERS 분석을 위해 Reference 대비 증감율을 기록. 
<br>ex) ratio_mu가 -0.16일 경우 클릭 전보다 클릭후 뮤파 16% 감소.
![image](https://user-images.githubusercontent.com/60168680/173658344-7fae0f5d-1c32-4dd9-964e-e93705b5fffe.png)

