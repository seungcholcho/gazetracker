#1 가상환경 실행하기
	1. cmd 열어서
		./gazetracker/Scripts/activate.bat
	실행하기


if 가상환경이 생기지 않았다면??? 그때 알려주세요.,.,.
	

#2 requirements 설치 되었는지 확인하기
	1. cmd 열어서 가상환경이 실행된 상태로
		pip freeze
	실행하기	

cmake==3.22.4
cycler==0.11.0
dlib==19.23.1
fonttools==4.33.3
kiwisolver==1.4.2
matplotlib==3.5.1
numpy==1.22.3
opencv-python==4.5.5.64
packaging==21.3
Pillow==9.1.0
pyparsing==3.0.8
python-dateutil==2.8.2
six==1.16.0

	실행 결과 위와 같은 라이브러리들 있으면 성공!

#3 없다면,, requirements 설치하기
	cmd 열어서
		./gazetracker/
	디렉토리로 이동
	pip install -r "requirements.txt"
	실행하기

순서대로 설치되는거 확인하고 pip freeze 로 설치 다 잘 됐는지 확인하기
