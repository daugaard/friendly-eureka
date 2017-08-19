import csv
from time import gmtime
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error


X = []
with open('data/scheme2_X.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        X.append(map(float,row))

# Convert to numpy
X = np.array(X)

y = []
with open('data/scheme2_y.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        y = map(float,row)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=gmtime().tm_sec)

print len(X_train), len(y_train)
print len(X_test), len(y_test)

best_c = 0.001

for i in range(10,1600,50):
    X_train_new = X_train[:i]
    y_train_new = y_train[:i]

    clf = LogisticRegression(C=best_c, penalty='l2', tol=0.001)
    clf.fit(X_train_new, y_train_new)

    y_train_prediction = clf.predict(X_train_new)
    y_test_predictions = clf.predict(X_test)

    print len(X_train_new), np.mean((y_train_prediction-y_train_new)**2), np.mean((y_test_predictions-y_test)**2)
