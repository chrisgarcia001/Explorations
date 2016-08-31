# -----------------------------------------------------------------------------
# Author: cgarcia
# About: This builds a simple text classification pipeline that recognizes the. 
#        difference between two different sets of documents. Input 1) a directory
#        with 2 subdirectories - each contains a particular type of document, 
#        2) an output directory, and 3) an optional training fraction (default is 0.7).
#        Adapted from Spark ML simple text classification pipeline example.
# Example Usage: > spark-submit text_classifer.py ./two_class ./output/results.txt 
# -----------------------------------------------------------------------------

from __future__ import print_function
from os import sys, listdir
from text_util import clean_text, stem_wordify, write_file
from cross_val import confusion_matrix
from pyspark import SparkContext
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.sql import Row, SQLContext


# Determines if a line is meta-data and should be excluded.
def exclude_line(line):
	words = line.strip().split(' ')
	return (True if len(words) > 0 and words[0].endswith(':') else False)

# Handle unicode conversion.
def decode(text):
	out = ''
	for c in text:
		try:
			out += str(c)
		except:
			out += ''
	return out
	
# Clean and stem the text.
def format_text(text):
	if type(text) == type(u'x'):
		text = decode(text)
	if type(text) == type([]):
		text = ','.join(filter(lambda x: not(exclude_line(decode(x))), text))
	return ' '.join(stem_wordify(clean_text(text.lower(), ' ')))


if __name__ == "__main__":
	sc = SparkContext(appName="TextClassificationPipeline")
	sqlContext = SQLContext(sc)

	if len(sys.argv) < 3:
		msg = '\n\nUsage: > text_classify.py <input dir> <output file> [train fraction] [predict on dir] \n'
		msg += '   <input dir> contains 2 subdirs with docs of different classes\n'
		msg += '   <output file> gets results\n'
		msg += '   [train fraction] is optional training fraction - default is 0.7 or 70%\n'
		msg += '   [predict on dir] is directory with text files to predict classes for\n\n'
		print(msg)
		exit(-1)
	
	
	input_dir = sys.argv[1] 
	output_file = sys.argv[2]
	train_fraction = 0.7 if len(sys.argv) < 4 else float(sys.argv[3])
	predict_dir = None if len(sys.argv) < 5 else sys.argv[4]
	
	docs = sc.parallelize([]) # Create empty RDD
	distinct_labels = {} # index:cat_name - used for sparse format
	curr_cat = 0 # starting category numeric index - used for sparse format
	text_filter = lambda text: filter(lambda line: not(exclude_line(line)), text) # Filter out metadata lines

	for category_dir in listdir(input_dir): # Build the dataset of (docname, category, wordcounts) tuples
		distinct_labels[curr_cat] = category_dir
		next_docs = sc.wholeTextFiles(('/').join([input_dir, category_dir])) 
		docs = docs.union(next_docs.map(lambda (doc, lines): (format_text(lines), float(curr_cat))))
		curr_cat += 1
	
	training_rows = docs.sample(False, train_fraction)
	testing_rows = docs.subtract(training_rows)
	
	# Prepare training and test documents, which are labeled.
	LabeledDocument = Row("text", "label")
	train = training_rows.map(lambda x: LabeledDocument(*x)).toDF()
	test = testing_rows.map(lambda x: LabeledDocument(*x)).toDF()		

    # Configure an ML pipeline, which consists of tree stages: tokenizer, hashingTF, and lr.
	tokenizer = Tokenizer(inputCol="text", outputCol="words")
	hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="rawFeatures") #outputCol="features")
	idf = IDF(inputCol="rawFeatures", outputCol="features")
	lr = LogisticRegression(maxIter=1000, regParam=0.001)
	
	#pipeline = Pipeline(stages=[tokenizer, hashingTF, lr])
	p0 = Pipeline(stages=[tokenizer, hashingTF, idf ,lr])
	#m0 = p0.fit(train)
	#pipeline = Pipeline(stages=[m0, lr])
	pipeline = p0
	
	# Fit the pipeline to training documents.
	model = pipeline.fit(train)

    # Make predictions on test documents and print columns of interest.
	prediction = model.transform(test)
	selected = prediction.select("label", "prediction").collect() 
	#for row in selected.collect():
	#	print((row.label, row.prediction))
	actual = map(lambda row: distinct_labels[row.label], selected)
	predicted = map(lambda row: distinct_labels[row.prediction], selected)
	print('---------- CONFUSION MATRIX ------------------------\n\n')
	confusion_matrix(predicted, actual)
	print('\n\n-----------------------------------------------------\n\n')
	# TODO: Incorporate confusion matrix and diagnostics
	
	if predict_dir != None:
		pred_docs = sc.wholeTextFiles(predict_dir).map(lambda (id, lines): (id, format_text(lines)))
		UnlabeledDocument = Row("id", "text")
		for_pred = pred_docs.map(lambda x: UnlabeledDocument(*x)).toDF()
		predictions = model.transform(for_pred).select("id", "prediction").collect()
		str = reduce(lambda y,z: y+z, map(lambda x: '(' + x.id + ', ' + distinct_labels[x.prediction] + ')\n', predictions))
		write_file(str, output_file)
	sc.stop()
