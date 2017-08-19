import csv
from time import gmtime

from sklearn import svm

from sklearn.model_selection import train_test_split
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

clf = svm.SVC(kernel='rbf',gamma=0.001, C=0.001, probability=True)
clf.fit(X_train, y_train)

print "Score: ", clf.score(X_test, y_test)
