# Useful sources:
# http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RandomizedLogisticRegression.html#sklearn.linear_model.RandomizedLogisticRegression
# http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegressionCV.html#sklearn.linear_model.LogisticRegressionCV

from sklearn.linear_model import RandomizedLogisticRegression, LogisticRegression #, LogisticRegressionCV
from sklearn.datasets import load_iris
import numpy as np

iris = load_iris()
X, y = iris.data, iris.target
print(X)
print(y)
ff_model = RandomizedLogisticRegression() # Finds best set of features
X_new = ff_model.fit_transform(X, y)  # Fit data and get transformed input rows
print(X_new)
print(X.shape)
print(X_new.shape)
print(X[0:4])
print(ff_model.transform(X[0:4]))  # Transform the first 4 rows of data to get only best features
model = LogisticRegression().fit(X_new, y) # Fit logistic regression with best features
print(model.predict_proba(ff_model.transform(X[0:4]))) # predict probabilities for first 4 rows of data
print(ff_model.inverse_transform(ff_model.transform(X[0:4]))) # Test inverse transforming
arr = np.array([[1,1,1]])
print(ff_model.inverse_transform(arr)) # Get original matrix structure with 1's only in columns of retained features.
