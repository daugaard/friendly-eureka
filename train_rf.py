import csv
import numpy as np

from time import gmtime

from sklearn.ensemble import RandomForestClassifier
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

clf = RandomForestClassifier()

cv_score = cross_val_score(clf,X_train,y_train,cv=5)

clf.fit(X_train, y_train)

score = cv_score.mean()

print "Training Score: ", clf.score(X,y)
print "Cross Validation Score: ", score

y_predictions = clf.predict(X_test)

print accuracy_score(y_test, y_predictions, False)
print clf.score(X_test, y_test)

joblib.dump(clf, "models/random_forest_scheme5.pkl")
