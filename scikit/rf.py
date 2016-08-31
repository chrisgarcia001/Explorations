from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
import numpy as np

iris = load_iris()
X, y = iris.data, iris.target

model = RandomForestClassifier(n_estimators=10)
model.fit(X, y)
print(model.predict_proba(X))

# Doesn't work without transforming to numeric X:
X2 = [['a','b','c'], ['a','b','c'], ['a','b','c'], ['b','b','b'], ['b','b','c'],\
		['b','c','a'], ['a','b','a'], ['b','b','a'], ['a','c','a'], ['a','c','c'], \
		['b','a','c'], ['b','a','a']]
y2 = [1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0]

# Smaller sample:
X2 = [{'x':'a','y':'b','z':'c'},{'x':'a','y':'c','z':'b'},\
		{'x':'b','y':'b','z':'c'}, {'x':'c','y':'b','z':'b'}]
y2 = [1,1,0,0]
X3 = [{'x':'a','y':'b','z':'c'},{'x':'b','y':'c','z':'b'}]

vec = DictVectorizer()
X2t = vec.fit_transform(X2).toarray()
X3t = vec.transform(X3).toarray()
print(vec.get_feature_names())

model2 = RandomForestClassifier(n_estimators=10)
model2.fit(X2t, y2)
print(model2.predict_proba(X3t))

