from os import sys
sys.path.insert(0, '../src/')
from data_gen import *
from logistic_model_builder import *
from rf_model_builder import *
from ga import *
import util as ut

# ---------------------- UTIL FUNCTIONS ---------------------
def parse_val(string):
	if len(filter(lambda x: x == '-', string)) > 0:
		if string[len(string) - 1] != ')':
			string += ')'
		if string[0] != '(':
			string = '(' + string
	return eval(string.replace(' ', '').replace('-', ';').replace(';', ','))

def parse_params(params):
	nd = {}
	for (k, v) in params.items():
		try:
			nd[k] = parse_val(v)
		except:
			nd[k] = v
	return nd
			
log_messages = []
def log(msg, level):
	print(msg)
	if level == 'standard':
		log_messages.append(msg)

def print_usage():
	print('Usage: > scenario_runner.py <param file path>\n')
	
# ---------------------- SET PARAMS -------------------------
params = {} # Read from CSV file
#try:
params = ut.read_csv_args(sys.argv[1], ignore_lines = '#')
print(params)
params = parse_params(params)
#except:
#	print_usage()
#	exit(-1)

params['logger_f'] = lambda x, y: log(x, y)

baseline_prob = params['baseline_prob'] if params.has_key('baseline_prob') else 0.005
n_user_attrs = params['n_user_attrs'] if params.has_key('n_user_attrs') else 5
n_inter_attrs = params['n_inter_attrs'] if params.has_key('n_inter_attrs') else 5
user_att_levels = params['user_att_levels'] if params.has_key('user_att_levels') else (5,5)
inter_att_levels = params['inter_att_levels'] if params.has_key('inter_att_levels') else (5,5)
n_users = params['n_users'] if params.has_key('n_users') else 50
n_test_inter_designs = params['n_test_inter_designs'] if params.has_key('n_test_inter_designs') else 50
top_n_control_inters = params['top_n_control_inters'] if params.has_key('top_n_control_inters') else 4
model = params['model'] if params.has_key('model') else LogisticModelBuilder()
replications = params['replications'] if params.has_key('replications') else 10
output_csv = params['output_csv'] if params.has_key('output_csv') else None
log_file = params['log_file'] if params.has_key('log_file') else None

# A random propensity spec is a tuple:
#   (num. distinct templates,  
#    num. user attrs specified,
#    num. inter atts specified,
#    probability of successful response,
#    num. matching user replicates generated for each template)
# Propensity specs begin with "propensity" in the params.
random_propensity_specs = map(lambda (x, y): y, filter(lambda (x, y): x.lower().startswith("propensity"), params.items()))
		
# ---------------------- POST-PARAM UTIL FUNCTIONS -----------
def write_log_file():
	if log_file != None:
		ut.write_file(reduce(lambda x,y: x + "\n" + y, log_messages), log_file)

def write_output_csv(rows):
	if output_csv != None:
		ut.write_csv(rows, output_csv)

def n_best_messages(datagen, users, messages, n):
	mcount = lambda m: sum(datagen.gen_crossprod_rows(users, [m])[2])
	results = map(lambda msg: (msg, mcount(msg)), messages)
	return ut.top_n(results, n, lambda x: x[1])
	
# ---------------------- BUILD SCENARIO ----------------------
b = DataGenerator()
b.set_baseline_response_prob(baseline_prob)
b.add_random_user_attrs(n_user_attrs, user_att_levels[0], user_att_levels[1])
b.add_random_inter_attrs(n_inter_attrs, inter_att_levels[0], inter_att_levels[1])

user_templates = [] #[(template, num_matchng_users)...]
inter_templates = [] #[templates]
total_users = 0
for (nt, nua, nia, p, nu) in random_propensity_specs:
	uts, its = b.set_random_propensities(nt, nua, nua, nia, nia, p, p)
	for temp in uts:
		user_templates.append((temp, nu))
		total_users += nu
	for temp in its:
		inter_templates.append(temp)

results = [[1,2,3]]		
for rep in range(1, replications + 1):
	users = b.gen_random_users(n_users, user_templates)
	test_messages = b.gen_random_inters(n_test_inter_designs, []) # TODO: Add specific number of propensity-based interactions if needed.
	model.set_data(*b.gen_crossprod_rows(users, test_messages))
	start_time = ut.curr_time()
	log('Beginning Simulation Interation ' + str(rep), 'standard')
	best_message, best_count = n_best_messages(b, users, test_messages, 1)[0]
	ga = GeneticAlgorithm(model.inter_attr_levels(), model.prob_f(), params)
	optimal_messages = map(lambda u: ga.optimize(u), users)
	log('Top message: ' + str((best_message, float(best_count)/float(len(users)))), 'standard')
	resps = b.gen_responses(users, map(lambda x: x[0], optimal_messages))
	log('Optimal targeted messages results: ' + str(float(sum(resps)) / float(len(users))), 'standard')

write_output_csv(results)
write_log_file()	
	
	
	
	