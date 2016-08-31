#-------------------------------------------------------
# Author: cgarcia
# This is a small library of Spark conversion functions.
#-------------------------------------------------------

# For a given list of unique words and (word, count) pairs, build 
# a list of counts corresponding to the unique words ordering.
def build_dense_row(label, unique_words, pairs):
	dc = dict(pairs)
	getct = lambda w: dc[w] if dc.has_key(w) else 0
	return [label] + map(getct, unique_words)

# Build a string version with the specified separator.	
def build_dense_row_string(label, unique_words, pairs, sep = ','):
	return ','.join(map(lambda x: str(x), build_dense_row(label, unique_words, pairs)))

# Build a sparse (libsvm) formatted line (a string). Here are the arg specifications:
#  label: a numeric label
#  word_index_map: a dict of format <word>:<1-indexed count>
#  pairs: a list of (word, count) pairs
def build_sparse_row_string(label, word_index_map, pairs):
	features = map(lambda (x, y): str(word_index_map[x]) + ':' + str(y), sorted(pairs, key=lambda (a, b): a))
	return reduce(lambda x, y: x + ' ' + y, [str(label)] + features)
	