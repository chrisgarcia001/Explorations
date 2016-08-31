# -----------------------------------------------------------------------------
# Author: cgarcia
# About: This merges all files in a certain directory into a common file. 
# Usage: > spark-submit file_merge.py <input dir of files> <final output file name>
# -----------------------------------------------------------------------------

from os import sys
from pyspark import SparkContext, SparkConf

# Check input args and print usage instructions if incorrect.
if len(sys.argv) < 2:
	print('\nUsage: > spark-submit file_merge.py <input dir of files> <final output file name>\n\n')
	exit(-1)

# Write a text file	
def write_file(text, filename):
	f = open(filename, "w")
	f.write(text)
	f.close()
	
# Read in command line args
input_dir = sys.argv[1]
output_file = sys.argv[2]
	
# Set up Spark context
conf = SparkConf().setAppName("File Merger")
sc = SparkContext(conf=conf)

input_files = sc.wholeTextFiles(input_dir)	# Read in files 
# Transform files into a single one:
final_content = input_files.map(lambda (doc, content): content.strip()).reduce(lambda x, y: x + "\n" + y) 	
write_file(final_content, output_file) # save final content into output file
sc.stop()

