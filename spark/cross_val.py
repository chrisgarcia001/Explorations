# Author: cgarcia
# About: This provides a few functions to support cross-validation for machine learning.

import random as rnd

# Given a set of observations (feature rows), corresponding labels, and a set of training indices, 
# split the data into training and test sets.
def index_split(feature_rows, labels, train_inds):
	train_dat = map(lambda i: feature_rows[i], train_inds)
	train_labels = map(lambda i: labels[i], train_inds)
	test_inds = set(range(len(feature_rows))).difference(train_inds)
	test_dat = map(lambda i: feature_rows[i], test_inds)
	test_labels = map(lambda i: labels[i], test_inds)
	return {"train_data":train_dat, "test_data":test_dat, "train_labels":train_labels, "test_labels":test_labels}

# Split into n random subsamples with the specified.
def random_subsample_splits(feature_rows, labels, n = 1, train_proportion = 0.7):
	splits = []
	for i in range(n):
		train_inds = rnd.sample(range(len(feature_rows)), int(train_proportion * len(feature_rows)))
		splits.append(index_split(feature_rows, labels, train_inds))
	return splits
	
# Split into k sections for kfold cross-validation.
def kfold_splits(feature_rows, labels, k = 2):
	splits = []
	min_ind = 0
	max_ind = -1
	chunk_size = int(float(len(feature_rows)) / float(k))
	for i in range(1, k + 1):
		min_ind = max_ind + 1
		max_ind += chunk_size
		train_inds = set(range(len(feature_rows))).difference(range(min_ind, min(max_ind, len(feature_rows))))
		splits.append(index_split(feature_rows, labels, train_inds))
	return splits

# Splits into leave-one-out sets for leave-one-out cross-validation.
def leave_one_out_splits(feature_rows, labels):
	splits = []
	for i in range(len(feature_rows)):
		train_inds = set(range(len(feature_rows))).difference([i])
		splits.append(index_split(feature_rows, labels, train_inds))
	return splits

# Pad a string with spaces on the back to get to the desired length.
def post_pad(string, length):
	strin = str(string)
	while len(strin) < length:
		strin += ' '
	return strin
	
# Print a simple confusion matrix.	
def confusion_matrix(predicted, actual):
	h = {}
	for i in range(len(predicted)):
		pair = str(predicted[i]) + '-' + str(actual[i])
		if not(h.has_key(pair)):
			h[pair] = 0
		h[pair] += 1
	print("\nPredicted   Actual   Count")
	successes = 0
	for (key, val) in h.items():
		names = key.split('-')
		if(names[0] == names[1]):
			successes += val
		string = post_pad(str(names[0]), len("Predicted   ")) + str(names[1])
		string = post_pad(string, len("Predicted   Actual   ")) + str(val)
		print(string)
	print("\n")
	print("Accuracy: " + str(float(successes) / float(len(predicted))) + "\n")

# Using the specified model and data splits, do a cross_validation and report basic results.	
# model_gen: a function that builds a model (assumes model has these functions: fit(data, labels) and predict(test_data))
# data_splits: a set of data splits (presumably generated from one of the methods above).
def cross_validate(model_gen, data_splits):
	predicted = []
	actual = []
	print("Training and Cross-Validating Model...")
	for split in data_splits:
		model = model_gen().fit(split["train_data"], split["train_labels"])
		predicted += list(model.predict(split["test_data"]))
		actual += split["test_labels"]
	print("Done!")
	confusion_matrix(predicted, actual)
		
		
		