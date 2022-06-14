from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.svm import SVC

# 파일 load
df = pd.read_excel('C:/BCI Data/ratio file/trainset588.xlsx')

x = df[df.columns[1,4]] # ratio_mu, ratio_theta, ratio_beta
y = df['ClickorNot'] # y label (0 or 1)

X_train, X_test, y_train, y_test = train_test_split(x, y , test_size = 0.2, random_state=123)

# 모델 학습
model = SVC(kernel='rbf', gamma=0.01).fit(X_train, y_train)

# 평가
print("훈련 세트 정확도: {:.2f}".format(model.score(X_train, y_train)))
print("테스트 세트 정확도: {:.2f}".format(model.score(X_test, y_test)))


