# This file builds R-friendly CSV files from the Yelp data.
# The sentiment coding used is the AFINN-111 list, originating here: 
#   http://www2.imm.dtu.dk/pubdb/views/publication_details.php?id=6010

import sys
from csv_util import *
import random
import json

# For a file of sentiment-coded words, get into a 
# {<word> : <code>} form.
def get_sentiment_codes(filename):
	lines = open(filename, 'r').readlines()
	codes = {}
	for line in lines:
		words = line.lower().strip().replace("\t", " ").split(' ')
		words = filter(lambda x: x != '', words)
		if len(words) == 2:
			codes[words[0]] = float(words[1])
	return codes

# For a given punctuation list and character, return a whitespace if char is in list.
def remove_punct(char, punct):
	if char in punct:
		return ' '
	else:
		return char

# For a given passage of text, build a tuple of (<total_word_count>, <sentiment_word_count>, <sentiment_total_score>).		
def sentiment_tuple(codes, text, punct = ['.', '?', '!', ',', '-', "'", ';', ':', '/', "\n", "\t"]):
	clean_text = ''.join(map(lambda x: remove_punct(x, punct), text)).lower()
	words = filter(lambda x: x != '', clean_text.split(' '))
	total_word_count = 0
	sentiment_word_count = 0
	sentiment_score_total = 0
	for word in words:
		total_word_count += 1
		if codes.has_key(word):
			sentiment_word_count += 1
			sentiment_score_total += codes[word]
	return (total_word_count, sentiment_word_count, sentiment_score_total)

# Get the sentiment score for the given text passage.
def sentiment_score(codes, text, avg_total_words = True, punct = ['.', '?', '!', ',', '-', "'", ';', ':', '/', "\n", "\t", '"']):
	total_word_count, sent_word_count, total_score = sentiment_tuple(codes, text, punct)
	denom = total_word_count
	if not(avg_total_words):
		denom = sent_word_count
	if denom == 0:
		return 0
	return float(total_score) / float(denom)

def build_review_csv(sentiment_code_file, review_json_file, output_file, sample = None):
	codes = get_sentiment_codes(sentiment_code_file)
	lines = open(review_json_file, 'r').readlines()
	print('Total Records: ' + str(len(lines)))
	if sample != None:
		lines = random.sample(lines, sample)
	data = [['user_id', 'business_id', 'sentiment','stars','text']]
	for line in lines:
		jd = eval(line)#json.loads(line.strip())
		uid = jd['user_id']
		bid = jd['business_id']
		text = jd['text'].replace(',', ' ').replace("\n", ' ')
		stars = str(jd['stars'])
		sentiment = str(sentiment_score(codes, text))
		data.append([uid, bid, sentiment, stars, text])
	write_csv(data, output_file)

def build_basic_review_csv(review_json_file, output_file, sample = None):
	lines = open(review_json_file, 'r').readlines()
	print('Total Records: ' + str(len(lines)))
	if sample != None:
		lines = random.sample(lines, sample)
	data = [['user_id', 'business_id', 'stars', 'text']]
	for line in lines:
		jd = eval(line)#json.loads(line.strip())
		uid = jd['user_id']
		bid = jd['business_id']
		text = jd['text'].replace(',', ' ').replace("\n", ' ')
		stars = str(jd['stars'])
		data.append([uid, bid, stars, text])
	write_csv(data, output_file)
	
outfile = 'review_data.csv'
n = None
print(sys.argv)
if len(sys.argv) > 1:
	outfile = sys.argv[1]
if len(sys.argv) > 2:
	n = int(sys.argv[2])
#build_review_csv('auxiliary_data/AFINN-111.txt', 'data/yelp_academic_dataset_review.json', outfile, n)
build_basic_review_csv('data/yelp_academic_dataset_review.json', outfile, n)	
	
	