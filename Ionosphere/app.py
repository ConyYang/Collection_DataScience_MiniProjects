import os
import numpy as np
import csv
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from matplotlib import pyplot as plt
estimator = KNeighborsClassifier()

data_filename = os.path.join("ionosphere.data")
X = np.zeros((351, 34), dtype="float")
y = np.zeros((351, 1), dtype='bool')

with open(data_filename, 'r') as input_file:
    reader = csv.reader(input_file)
    for i, row in enumerate(reader):
        data = [float(datum) for datum in row[:-1]]
        X[i] = data
        y[i] = (row[-1] == 'g')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=14)
estimator.fit(X_train, np.ravel(y_train))
y_predict = estimator.predict(X_test)

avg_scores = []
all_scores = []
parameters = list(range(1, 21))

for n in parameters:
    estimator = KNeighborsClassifier(n_neighbors=n)
    scores = cross_val_score(estimator, X, np.ravel(y), scoring='accuracy')
    avg_scores.append(np.mean(scores))
    all_scores.append(scores)

# plt.plot(parameters, avg_scores)
plt.plot(parameters, all_scores)
plt.show()




