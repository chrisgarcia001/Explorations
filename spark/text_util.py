#-------------------------------------------------------
# Author: cgarcia
# This is a small library of text-processing functions.
#-------------------------------------------------------
import nltk
from nltk.tokenize import wordpunct_tokenize #, word_tokenize #, sent_tokenize
from nltk.stem.lancaster import LancasterStemmer

# Parse params in CSV format - one param per line. Default separator is ','. All values are strings.
def parse_params(params, sep = ','):
	if type(params) == type(''):
		params = params.split('\n')
	params = filter(lambda x: len(x) > 0, map(lambda y: y.strip(), params))
	parsed = {}
	for line in params:
		seq = line.split(sep)
		param, val = seq[0], seq[1]
		parsed[param] = val
	return parsed
		

# Write a text file	
def write_file(text, filename):
	f = open(filename, "w")
	f.write(text)
	f.close()

# Remove punctuation from a chunk of text.
def remove_punct(text, replace = ''):
	punct = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
	clean = lambda x: replace if (x in punct) else x
	return ''.join(map(clean, text.strip()))

# Remove punctuation, tabs, whitespace, etc. and make ready for text analysis.
def clean_text(text, punct_replace = ''):
	special_chars = '''\n\t'''
	clean = lambda x: ' ' if (x in special_chars) else x
	return ''.join(map(clean, remove_punct(text, punct_replace)))
	
# Turns a chunk of text into a list of words (if it isn't already).
def wordify(text):
	words = text
	if(type(text) == type('')):
		words = text.split(' ')
		#words = wordpunct_tokenize(text)
	return filter(lambda x: len(x) > 1, words)

# Stem and wordify the text.
def stem_wordify(text):
	sw = nltk.corpus.stopwords.words('english') 
	st = LancasterStemmer()
	return map(lambda x: st.stem(x), 
				filter(lambda y: not(y in sw), map(lambda z: st.stem(z), wordify(text))))

# For a chunk of text or lines list and return a list of 
# (word, count) pairs. Stop words are excluded.	Params:
#   text: either a string or list of strings of text
#   stem: True | False (whether or not to stem)
#   preprocessing_filterf: takes in text and returns filtered text 
def wordcounts(text, stem, preprocessing_filterf = lambda x: x):
	text = preprocessing_filterf(text)
	if type(text) == type([]):
		text = str((' ').join(map(lambda x: x.strip(), text)))
	counts = {}
	word_splitf = stem_wordify if stem else wordify
	words = word_splitf(clean_text(str(text).lower(), ' '))
	for word in words:
		if not(counts.has_key(word)):
			counts[word] = 0
		counts[word] += 1
	return counts.items()				
				
