import csv
from time import gmtime
from sklearn.neural_network import MLPClassifier

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

from sklearn.metrics import accuracy_score
from sklearn.externals import joblib

X = []
with open('data/scheme5_X.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        X.append(map(float,row))

y = []
with open('data/scheme5_y.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        y = row

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=gmtime().tm_sec)

best_i = 0
best_score = 0

for i in [16,34,68]:
    clf = MLPClassifier(solver='adam', alpha=0.001, hidden_layer_sizes=(i), random_state=gmtime().tm_sec, max_iter=500)
    cv_score = cross_val_score(clf,X,y,cv=5)

    clf.fit(X,y)

    if cv_score.mean() > best_score:
        best_score = cv_score.mean()
        best_i = i

    print cv_score
    print "%(i)d, Train Classification Score = %(train)f, Cross Validation Score = %(test)f" % {"i":i, "train": clf.score(X, y)*100, "test": cv_score.mean()*100 }


print best_i, best_score

# Do final fit of best algorithm
clf = MLPClassifier(solver='adam', alpha=0.001, hidden_layer_sizes=(best_i), random_state=gmtime().tm_sec, max_iter=500)
clf.fit(X_train,y_train)

y_predictions = clf.predict(X_test)

print accuracy_score(y_test, y_predictions, False)
print clf.score(X_test, y_test)

joblib.dump(clf, "models/neural_network_scheme5.pkl")
