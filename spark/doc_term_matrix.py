# -----------------------------------------------------------------------------
# Author: cgarcia
# About: This builds a document-term matrix for document classification. 
#        Pass in a folder containing sub-folders named according to the 
#        document class each contains (as a command-line arg).
# Example Usage: > spark-submit doc_term_matrix.py train_tiny ./output sparse dense
# -----------------------------------------------------------------------------

from os import sys, listdir
from pyspark import SparkContext, SparkConf
from text_util import wordcounts, write_file
from conversion_util import build_dense_row_string, build_sparse_row_string

dense_matrix_filename = 'dense_matrix.csv'
sparse_matrix_filename = 'sparse_matrix.txt'
words_filename = 'all_words.txt'
labels_filename = 'labels.csv'

# ------------------------------------ UTILITY FUNCTIONS ----------------------

# Determines if a line is meta-data and should be excluded.
def exclude_line(line):
	words = line.strip().split(' ')
	return (True if len(words) > 0 and words[0].endswith(':') else False)

# Print a note on how to use
def print_usage():
	print('\nUsage: > spark-submit doc_term_matrix.py <input dir> <output dir> [dense] [sparse]\n\n')
	
# ------------------------------------ MAIN SPARK PROGRAM ---------------------	

if len(sys.argv) < 2:
	print_usage()
	exit(-1)

# Set path to directory of category directories (each category directory 
# contains only documents of the respective category name).
path = sys.argv[1] 
output_dir = sys.argv[2]
do_dense = 'dense' in map(lambda x: x.lower(), sys.argv)
do_sparse = 'sparse' in map(lambda x: x.lower(), sys.argv)

# Set up Spark context
conf = SparkConf().setAppName("Doc-Term Matrix Builder")
sc = SparkContext(conf=conf)

docs = sc.parallelize([]) # Create empty RDD
distinct_labels = {} # category_name : index - used for sparse format
curr_cat = 0 # starting category numeric index - used for sparse format
text_filter = lambda text: filter(lambda line: not(exclude_line(line)), text) # Filter out metadata lines

for category_dir in listdir(path): # Build the dataset of (docname, category, wordcounts) tuples
	distinct_labels[category_dir] = curr_cat
	curr_cat += 1
	next_docs = sc.wholeTextFiles(('/').join([path, category_dir]))
	docs = docs.union(next_docs.map(lambda (doc, lines): (doc, category_dir, wordcounts(lines, True, text_filter))))

# Generate the list of all unique words in sorted order:
all_words = sorted(docs.flatMap(lambda (doc, cat, counts): counts).map(lambda (x, y): x).distinct().collect())

# Build a word-index map for use in making the sparse matrix:
word_index_map = dict(map(lambda x: (all_words[x - 1], x), range(1, len(all_words) + 1)))

# Generate the document-term matrix (dense format)
if do_dense:
	dense_row_gen = lambda (doc, cat, counts): build_dense_row_string(distinct_labels[cat], all_words, counts)
	dense_matrix = docs.map(dense_row_gen).reduce(lambda x, y: x + '\n' + y)
	write_file(dense_matrix, output_dir + dense_matrix_filename)
	
# Generate the document-term matrix (sparse format)
if do_sparse:
	sparse_row_gen = lambda (doc, cat, counts): build_sparse_row_string(distinct_labels[cat], word_index_map, counts)
	sparse_matrix = docs.map(sparse_row_gen).reduce(lambda x, y: x + '\n' + y)
	write_file(sparse_matrix, output_dir + sparse_matrix_filename)
	
# Write output files
write_file('\n'.join(all_words), output_dir + words_filename)
write_file('\n'.join(map(lambda (x, y): str(x) + ',' + str(y), distinct_labels.items())), output_dir + labels_filename)
	
sc.stop()

