from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from app import X_train, X, y
from sklearn.neighbors import KNeighborsClassifier
from matplotlib import pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
estimator = KNeighborsClassifier()

X_broken = np.array(X)
X_broken[:, ::2]/= 10

def print_test():
    original_scores = cross_val_score(estimator, X, np.ravel(y), scoring='accuracy')
    broken_scores = cross_val_score(estimator, X_broken, np.ravel(y), scoring='accuracy')
    X_transform = MinMaxScaler().fit_transform(X_broken)
    transform_scores = cross_val_score(estimator, X_transform, np.ravel(y), scoring='accuracy')

    print(X == X_broken)
    print("The original average score for is {}".format(np.mean(original_scores)*100))
    print("The 'broken' average score for is {}".format(np.mean(broken_scores)*100))
    print("The 'transform' average score for is {}".format(np.mean(transform_scores)*100))

# There are two steps for pipeline
# (1) Use MinMaxScaler to scale value range from 0-1
# (2) Use Kneighbors Classifier
# Every step use a element ('name', step). Forms a list of elements. (1) scale (2) predict

def pipeline():
    scaling_pipeline = Pipeline([('scale', MinMaxScaler()),('predice', KNeighborsClassifier())])
    scores = cross_val_score(scaling_pipeline, X_broken, np.ravel(y), scoring='accuracy')
    print("The 'transform' average score for is {}".format(np.mean(scores)*100))
pipeline()
