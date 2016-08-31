import random as rd

words = open('data/yelp_academic_dataset_review.json', 'r').readlines()
t = 0
words = rd.sample(words, 10)
for w in words:
	print(w)
	if eval(w)['stars'] == 5:
		t += 1
print(float(t) / float(len(words)))

# words = open('data/yelp_academic_dataset_business.json', 'r').readlines()
# t = 0
# ct = 0
# for w in words:
	# obj = eval(w.replace('true', 'True').replace('false', 'False'))
	# if obj['attributes'].has_key("Wi-Fi"):
		# ct += 1
		# if obj['attributes']['Wi-Fi'].lower() == 'free':
			# t += 1
# print(float(t) / float(ct))

# words = open('data/yelp_academic_dataset_user.json', 'r').readlines()
# fnames = []
# for w in words:
	# obj = eval(w.replace('true', 'True').replace('false', 'False'))
	# if obj['votes'].has_key("funny"):
		# if obj['votes']['funny'] >= 10000:
			# fnames.append(obj['name'])#print(obj['name'])
	# fnames.sort()
# print('Names: --------------')
# for n in fnames:
	# print(n)
			
		
		