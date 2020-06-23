from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from app import X_train, X, y
from sklearn.neighbors import KNeighborsClassifier
from matplotlib import pyplot as plt
import numpy as np


X_broken = np.array(X)
X_broken[:, ::2]/= 10
print(X == X_broken)


estimator = KNeighborsClassifier()
original_scores = cross_val_score(estimator, X, np.ravel(y), scoring='accuracy')
print("The original average score for is {}".format(np.mean(original_scores)*100))

broken_scores = cross_val_score(estimator, X_broken, np.ravel(y), scoring='accuracy')
print("The 'broken' average score for is {}".format(np.mean(broken_scores)*100))
