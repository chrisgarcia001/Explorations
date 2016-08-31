import random as rd
import util as ut


def n_best_inters(users, inters, responses, n):
	rows = zip(users, inters, responses)
	mcount = lambda m: sum(map(lambda x: x[2], filter(lambda y: y[1] == m, rows)))
	pos_count = lambda y: sum(map(lambda x: x[2], filter(lambda z: y == z[1], tups)))
	results = map(lambda msg: (msg, mcount(msg)), inters)
	return ut.top_n(results, n, lambda x: x[1])

# Builds a function to extract the top n best-performing interactions
# from a dataset and build a predictive model on that. 
# Returns a function that returns the best message for a user from these top n
# based on the predictive model.
def build_top_n_optimizer(users, inters, resps, top_n, model_builder, relative_percent_compare=False):
	tups = zip(users, inters, resps)
	pos_count = lambda y: sum(map(lambda x: x[2], filter(lambda z: y == z[1], tups)))
	rel_pos_perc = lambda y: float(pos_count(y)) / float(len(filter(lambda z: y == z[1], tups)))
	top_inters = None
	if relative_percent_compare:
		top_inters = ut.top_n(inters, top_n, rel_pos_perc)
	else:
		top_inters = ut.top_n(inters, top_n, pos_count)
	top_tups = filter(lambda x: x[1] in top_inters, tups)
	print(top_tups[:5])
	model_builder.set_data_rows(tups)
	f = lambda x: ut.top_n(top_inters, 1, lambda y: model_builder.prob_f()(x, y))[0]
	return f
	# best_message, best_count = n_best_inters(users, inters, resps, 1)[0]
	# return lambda x: best_message