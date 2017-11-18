import csv
from time import gmtime

from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

import numpy as np

X = []
with open('data/scheme4_X.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        X.append(map(float,row))
X = np.array(X)

y = []
with open('data/scheme4_y.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        y =  map(float,row)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=gmtime().tm_sec)

best_c = 0
best_g = 0
best_score = 0

for c in [0.001, 0.01, 0.1, 1, 3, 10]:
    for g in [0.001, 0.01, 0.1, 1, 3, 10, 30,1500]:
        print "C:", c, "G:", g
        clf = svm.SVC(kernel='rbf',gamma=g, C=c, probability=True)

        cv_score = cross_val_score(clf,X,y,cv=5)

        clf.fit(X, y)

        score = cv_score.mean()
        print "Cross Validation Score: ", score

        if score > best_score:
            best_score = score
            best_c = c
            best_g = g
            print c
            print "Training Score: ", clf.score(X,y)
            print "Cross Validation Score: ", score


# Do final fit with the best algorithm
clf = svm.SVC(kernel='rbf',gamma=best_g, C=best_c, probability=True)
clf.fit(X, y)

y_predictions = clf.predict(X_test)

print accuracy_score(y_test, y_predictions, False)
print clf.score(X_test, y_test)


print "Score: ", clf.score(X_test, y_test)
