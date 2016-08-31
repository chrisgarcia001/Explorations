# Useful source:
# http://scikit-learn.org/stable/modules/feature_extraction.html#feature-extraction

from sklearn.feature_extraction import DictVectorizer

measurements = [
	{'city': 'Dubai', 'temperature': 33.},
	{'city': 'London', 'temperature': 12.},
	{'city': 'San Fransisco', 'temperature': 18.},
	]

vec = DictVectorizer()
print(vec.fit_transform(measurements).toarray())
print(vec.get_feature_names())
print(vec.transform(measurements).toarray())