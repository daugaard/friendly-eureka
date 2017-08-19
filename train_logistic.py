import csv
import numpy as np

from time import gmtime

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

from sklearn.metrics import accuracy_score
from sklearn.externals import joblib

X = []
with open('data/scheme5_X.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        X.append(map(float,row))

# Convert to numpy
X = np.array(X)

y = []
with open('data/scheme5_y.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        y = map(float,row)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=gmtime().tm_sec) #2)

best_c = 0
best_score = 0

for c in [0.001, 0.01, 0.1, 1, 3, 10, 30,1500]:
    clf = LogisticRegression(C=c, penalty='l2', tol=0.001)

    cv_score = cross_val_score(clf,X,y,cv=5)

    clf.fit(X, y)

    score = cv_score.mean()

    if score > best_score:
        best_score = score
        best_c = c
        print c
        print "Training Score: ", clf.score(X,y)
        print "Cross Validation Score: ", score

# Do final fit with the best algorithm
clf = LogisticRegression(C=best_c, penalty='l2', tol=0.001)
clf.fit(X, y)

y_predictions = clf.predict(X_test)

print accuracy_score(y_test, y_predictions, False)
print clf.score(X_test, y_test)

joblib.dump(clf, "models/logistic_regression_scheme5.pkl")
