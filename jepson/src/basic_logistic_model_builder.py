from sklearn.linear_model import RandomizedLogisticRegression, LogisticRegression

class BasicLogisticModelBuilder(object):
	# Takes in a set of predictor rows (X) and response targets (y) and
	# constructs a logistic regression model with the optimal features.
	# Uses the RandomizedLogisticRegression class to stochastically find the best
	# set of features.
	# Param predictor_rows: An array of observations. User attributes come
	#                       first followed by message/interaction attributes.
	# Param responses: An array of 0 or 1 (1 if positive response).
	def __init__(self, predictor_rows, responses):
		self.ff_model = RandomizedLogisticRegression() # Finds best set of features
		X_new = ff_model.fit_transform(predictor_rows, responses)  # Fit data and get transformed input rows
		self.model = LogisticRegression().fit(X_new, responses)

	# Returns a function of form f:<user_atts list> X <msg atts list> -> <corresponding probabilities>
	def prob_f():
		ff = self.ff_model
		mod = self.model
		return lambda X, Y: mod.predict_proba(ff.transform(map(lambda (x, y): x + y, zip(X, Y))
		
	# Returns a function of form f:<predictor rows> -> <corresponding probabilities>
	# For testing.
	def prob_f_single():
		ff = self.ff_model
		mod = self.model
		return lambda X: mod.predict_proba(ff.transform(X))