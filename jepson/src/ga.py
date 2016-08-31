import random as rd
import util as ut

class GeneticAlgorithm(object):
	def __init__(self, inter_atts, prob_f, params={}):
		self.inter_atts = inter_atts
		self.prob_f = prob_f
		self.logger_f = params['logger_f'] if params.has_key('logger_f') else None
		self.crossover_rate = params['crossover_rate'] if params.has_key('crossover_rate') else 0.3
		self.mutation_rate = params['mutation_rate'] if params.has_key('mutation_rate') else 0.01
		self.pop_size = params['pop_size'] if params.has_key('pop_size') else 100
		self.max_iterations = params['max_iterations'] if params.has_key('max_iterations') else 100
		self.max_time = params['max_time'] if params.has_key('max_time') else None
		self.max_noimprove_iterations = params['max_noimprove_iterations'] if params.has_key('max_noimprove_iterations') else None
		self.max_noimprove_time = params['max_noimprove_time'] if params.has_key('max_noimprove_time') else None
		self.elitism = params['elitism'] if params.has_key('elitism') else 0.1
		self.curr_iter = 0
		self.start_time = 0
		self.start_noimprove_time = 0
		self.noimprove_iterations = 0
	
	# This determines if a termination condition has been met.
	# Returns: True or False, accordingly
	def should_terminate(self):
		if self.curr_iter >= self.max_iterations:
			return True
		if self.max_time != None and ut.curr_time() >= self.start_time + self.max_time:
			return True
		if self.noimprove_iterations >= self.max_noimprove_iterations:
			return True
		if self.max_noimprove_time != None and ut.curr_time() >= self.start_noimprove_time + self.max_noimprove_time:
			return True
		return False
	
	# Constructs a list of randomly-generated interactions.
	# Param n: the number of interactions to generated
	# Returns: a list of randomly-generated interactions
	def build_random_candidates(self, n):
		rv = lambda levs: rd.uniform(levs[0], levs[1]) if type(levs) == type(()) else rd.sample(levs, 1)[0] 
		return map(lambda x: map(lambda y: rv(y), self.inter_atts), range(n))
	
	# Performs point mutations on an interaction according to the mutation rate.
	# For each mutated attribute: if it is categorical, a new level is randomly selected,
	# otherwise a uniform random number generated on the attribute's [min, max] range.
	# Param inter: an interaction
	# Returns: a new mutated interaction
	def mutate(self, inter):
		rv = lambda levs: rd.uniform(levs[0], levs[1]) if type(levs) == type(()) else rd.sample(levs, 1)[0] 
		ptf = lambda (cv, levs): rv(levs) if rd.uniform(0, 1) <= self.mutation_rate else cv
		return map(ptf, zip(inter, self.inter_atts))
	
	# Performs uniform crossover between two interactions, based on the specified crossover rate.
	# Param inter1: an interaction
	# Param inter2: an interaction
	# Returns: a pair of form (child 1, child 2)
	def crossover(self, inter1, inter2):
		i1, i2 = list(inter1), list(inter2)
		for i in range(len(i1)):
			if rd.uniform(0, 1) <= self.crossover_rate:
				t = i1[i]
				i1[i] = i2[i]
				i2[i] = t
		return (i1, i2)	
	
	# For a population of (interaction, prob) pairs, construct a 
	# cumulative-sum list for the population by each pair's prob.
	# Param population: a list of (interaction, prob) pairs
	# Returns: a corresponding cumulative-sum list.
	def cumulative_sums(self, population):
		cum = 0.0
		cum_sums = []
		for (inter, prob) in population:
			cum += prob
			cum_sums.append(cum)
		return cum_sums
	
	# Constructs a new generation from the current population. Uses
	# roulette-wheel selection. A population is a list of (interaction, prob) pairs.
	# Param user: A user (list of user attribute values)
	# Param curr_population: A list of (interaction, prob) pairs
	# Param n: The size of the new generation
	# Returns: A list of n new (interaction, prob) pairs.
	def build_new_gen(self, user, curr_population, n):
		new_pop = []
		cum_sums = self.cumulative_sums(curr_population)
		maxval = cum_sums[len(cum_sums) - 1]
		while len(new_pop) < n:
			v1, v2 = rd.uniform(0, maxval), rd.uniform(0, maxval)
			i1, i2 = ut.cumulative_bin_search(v1, cum_sums), ut.cumulative_bin_search(v2, cum_sums)
			c1, c2 = curr_population[i1][0], curr_population[i2][0]
			s1, s2 = self.crossover(c1, c2)
			new_pop.append(s1)
			if len(new_pop) < n:
				new_pop.append(s2)
		return map(lambda x: (x, self.prob_f(user, x)), map(lambda y: self.mutate(y), new_pop))
	
	# Log a message.
	# Param msg: the message
	# Param level: the log level (standard or debug)
	def log(self, msg, level):
		if self.logger_f != None:
			self.logger_f(msg, level)
	
	# Find the best solution given the user.
	# Param user: a list of user attribute values.
	# Returns: Optimal solution as a 3-tuple: (best interaction, prob, elapsed time)
	def optimize(self, user):
		self.log('Beginning GA Optimizer for user: ' + str(user), 'standard')
		reg_n = int(self.pop_size * (1 - self.elitism))
		elite_n = min(1, int(self.pop_size * self.elitism))
		pop = sorted(map(lambda x: (x, self.prob_f(user, x)), self.build_random_candidates(self.pop_size)), key = lambda x: x[1])
		regulars = pop[:reg_n]
		elites = pop[reg_n:]
		best = pop[len(pop) - 1]
		self.curr_iter = 1
		self.start_time = ut.curr_time()
		self.start_noimprove_time = ut.curr_time()
		self.noimprove_iterations = 0
		while not(self.should_terminate()):
			self.log('  Iteration ' + str(self.curr_iter) + ', Best so far: ' + str(best), 'debug')
			regulars = self.build_new_gen(user, regulars + elites, reg_n)
			pop = sorted(regulars + elites, key=lambda x: x[1])
			regulars = pop[:reg_n]
			elites = pop[reg_n:]
			if elites[0][1] > best[1]:
				self.start_noimprove_time = ut.curr_time()
				self.noimprove_iterations = -1
				best = elites[0]
			self.noimprove_iterations += 1
			self.curr_iter += 1
		best_inter, best_prob = best
		elapsed_time = ut.curr_time() - self.start_time
		msg = 'Best Solution = ' + str(best) + ', Elapsed Time (sec.): ' + str(elapsed_time)
		self.log(msg, 'standard')
		return (best_inter, best_prob, elapsed_time)
	