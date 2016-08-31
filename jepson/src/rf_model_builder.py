from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from util import dict_list_representation
import util as ut
import numpy as np

class RandomForestModelBuilder(object):

	def __init__(self, n_estims=10):
		self.inter_levels = None
		self.dicts_rep = None
		self.model = None
		self.dict_vectorizer = DictVectorizer()
		self.n_estims = n_estims
		
		
	# Specify the data: users, interactions, and responses.
	def set_data(self, user_atts, inter_atts, responses):
		self.build_data_representations(user_atts, inter_atts)
		# Convert from dict representation into matrix:
		predictor_rows = self.dict_vectorizer.fit_transform(self.dicts_rep).toarray()
		print('Building Random Forest model...')		  
		self.model = RandomForestClassifier(n_estimators=self.n_estims).fit(predictor_rows, responses)
		print('Done!')
	
	# Set data based on tuples/rows
	def set_data_rows(self, tuples):
		self.set_data(*ut.unzip(tuples))
	
	# Builds a list-of-dictionaries representation and builds 
	# msg/interaction factor level matrix.
	def build_data_representations(self, user_atts, inter_atts):
		print('Building internal data representations...')
		print('   Building factor level matrix...')
		itp = map(lambda x: set(x), zip(*inter_atts)) # transpose and get row sets
		self.inter_levels = map(lambda x: x if len(filter(lambda y: type(y) == type(''), x)) > 0 else (min(x), max(x)), itp)
		print('   Building dict list representation...')
		self.dicts_rep = dict_list_representation(user_atts, inter_atts)
		print('Done!')	
			
	# Returns a function of form f: X x Y -> P
	# where X = <user_att vals>, Y = <inter. att vals>, and P = P(R = 1)
	def prob_f(self):
		dv = self.dict_vectorizer
		dlr = lambda x, y: dict_list_representation([x], [y])
		mod = self.model
		f = lambda X, Y: mod.predict_proba(dv.transform(dlr(X, Y)).toarray())
		return lambda X, Y: map(lambda z: z[1], f(X, Y))[0]
	
	# Return a vector of interaction attribute levels corresponding to each
	# interaction attribute. For each attribute the following rule is applied:
	# 1) If the attribute is categorical the attribute levels are a list of unique values
	# 2) If the attribute is numeric then a pair (min, max) is returned bounding the values.
	def inter_attr_levels(self):
		return map(lambda lv: lv if type(lv) == type(()) else list(lv), self.inter_levels)  
		