import util as ut

# -------------------- UTIL FUNCTIONS/DISTANCE MEASURES -----------
def count_in(val, val_list):
	return len(filter(lambda x: x == val, val_list))
	
def mean(vals):
	return float(sum(vals)) / float(len(vals))
	
def mode(vals):
	cts = map(lambda x: (x, count_in(x, vals)), vals) 
	return ut.top_n(cts, 1, lambda x: x[1])[0][0]

def max_net_occurrences_in(in_list, out_list):
	net_occs = map(lambda x: (x, count_in(x, in_list) - count_in(x, out_list)), in_list)
	return ut.top_n(net_occs, 1, lambda x: x[1])[0][0]

def max_ratio_occurrences_in(in_list, out_list):
	prp_occs = map(lambda x: (x, float(1 + count_in(x, in_list)) / float(1 + count_in(x, out_list))), in_list)
	return ut.top_n(prp_occs, 1, lambda x: x[1])[0][0]
	
def hamming(v1, v2):
	return len(filter(lambda (x, y): x != y, zip(v1, v2)))
	
def match_count(v1, v2):
	return len(filter(lambda (x, y): x == y, zip(v1, v2)))
	
# A knn_tuple is a (user, message, response, dist) tuple	
def msg_att_vals(knn_tuples):
	return map(lambda x: x[1], knn_tuples)

	
# -------------------- OPTIMIZER CLASS ----------------------------
class KNNOptimizer(object):
	def __init__(self):
		self.data_rows = []
		self.positives = []
		self.negatives = []
		self.distance_f = None
		self.num_msg_attributes = 0
	
	# A data row is a (user, msg, response) tuple
	# A distance_f is a function f : user X user -> R+
	def set_data_rows(self, data_rows):
		self.data_rows = data_rows
		self.positives = filter(lambda (x,y,z): z == 1, data_rows)
		self.negatives = filter(lambda (x,y,z): z == 0, data_rows)
		if len(data_rows) > 0:
			self.num_msg_attributes = len(data_rows[0][1])
	
	# Set the distance calculation function.
	def set_distance_f(self, distance_f):
		self.distance_f = distance_f
	
	# Finds the k-nearest-neighbours for a given user, k, and response class.
	# Returns a knn-tuple: (user, message, response, dist)
	def knn(self, user, k, resp = None):
		rows = self.data_rows
		if resp == 1:
			rows = self.positives
		elif resp == 0:
			rows = self.negatives
		dists = map(lambda (u, m, r): (u, m, r, self.distance_f(user, u)), rows)
		#print(ut.top_n(dists, lambda (u, m, r, d): 1.0 / float(d + 1)) )
		return ut.top_n(dists, lambda (u, m, r, d): 1.0 / float(d + 1)) 
	
	# This returns the best attribute based on the F1 rule:
	# Maximum positive instances.
	def f1(self, pos_tuples, neg_tuples, msg_attr_index):
		vals = map(lambda x: x[1][msg_attr_index], pos_tuples)
		return mode(vals)
	
	# This returns the best attribute based on the F2 rule:
	# Maximum net positive instances - negative instances.
	def f2(self, pos_tuples, neg_tuples, msg_attr_index):
		pos = map(lambda (u,m,r,d): m[msg_attr_index], pos_tuples)
		neg = map(lambda (u,m,r,d): m[msg_attr_index], neg_tuples)
		return max_net_occurrences_in(pos, neg)
	
	# This returns the best attribute based on the F2B rule:
	# Maximum ratio positive instances - negative instances.
	def f3(self, pos_tuples, neg_tuples, msg_attr_index):
		pos = map(lambda (u,m,r,d): m[msg_attr_index], pos_tuples)
		neg = map(lambda (u,m,r,d): m[msg_attr_index], neg_tuples)
		return max_ratio_occurrences_in(pos, neg)
	
	# This returns the best attribute based on the F3 rule:
	# Distance-weighted maximum net positive instances minus negative instances.
	# A knn-tuple: (user, message, response, dist)
	def f4(self, pos_tuples, neg_tuples, msg_attr_index):
		i = msg_attr_index
		distinct_pos = set(map(lambda (u,m,r,d): m[msg_attr_index], pos_tuples))
		mtch = lambda v, tups: filter(lambda (u,m,r,d): m[i] == v, tups)
		wv = lambda v, tups: len(mtch(v, tups)) * sum(map(lambda (u,m,r,d): 1.0 / float(d + 1), mtch(v, tups)))
		twv = lambda v: wv(v, pos_tuples) - wv(v, neg_tuples)
		return ut.top_n(map(lambda x: (x, twv(x)), distinct_pos), 1, lambda x: x[1])[0][0]
		
	
	# Returns the optimal message design given the user and k, based on the
	# specified attribute selector (at present one of f1, f2, or f3).
	def optimize(self, user, k, attr_selector_f):
		tuples = self.knn(user, k)
		pos_tuples = filter(lambda (u,m,r,d): r == 1, tuples)
		neg_tuples = filter(lambda (u,m,r,d): r == 0, tuples)
		#pos_tuples = self.knn(user, k, 1)
		#neg_tuples = self.knn(user, k, 0)
		n = self.num_msg_attributes
		return map(lambda x: attr_selector_f(pos_tuples, neg_tuples, x), range(n))
	
	# Optimize a list of users.
	def optimize_all(self, users, k, attr_selector_f):
		return map(lambda u: self.optimal_msg(u, k, attr_selector_f), users)
	

		
