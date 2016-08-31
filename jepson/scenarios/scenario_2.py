from os import sys
sys.path.insert(0, '../src/')
from data_gen import *
from knn import *
import util as ut
import scenario_util as su


# Main parameters.
num_trials = 5
num_user_atts, min_user_att_levels, max_user_att_levels = 4, 2, 4
num_msg_atts, min_msg_att_levels, max_msg_att_levels = 4, 2, 4

num_propensity_groups = 25

min_group_user_atts, max_group_user_atts = 3, 3
min_group_msg_atts, max_group_msg_atts = 2, 3
min_group_pos_prob, max_group_pos_prob = 0.2, 0.85

num_test_message_combinations = 100
output_file = '../output/scenario_2B.txt'

# Initializer function
def trial_init(recdr, logr):
	logr.log('Initializing new trial...', 'standard')
	b = DataGenerator()
	b.set_baseline_response_prob(0.02)
	b.add_random_user_attrs(num_user_atts, min_user_att_levels, max_user_att_levels) 
	b.add_random_inter_attrs(num_msg_atts, min_msg_att_levels, max_msg_att_levels) 
	templates = b.set_random_propensities(num_propensity_groups, 
							  min_group_user_atts, max_group_user_atts, 
							  min_group_msg_atts, max_group_msg_atts,
							  min_group_pos_prob, max_group_pos_prob)
	# -> Returns: a pair (user templates, interaction templates)
	logr.log('Generating data...', 'standard')
	messages = b.gen_random_inters(num_test_message_combinations)
	rows = ut.unzip(b.gen_crossprod_rows(b.unique_users(), messages))
	logr.log('Number of rows: ' + str(len(rows)), 'standard')
	# Split data into train, calibration, and test.
	train, calibrate, test = ut.split_data(rows, 0.5, 0.25, 0.25)
	calibration_users = map(lambda (u, m, r): u, calibrate)
	test_users = map(lambda (u, m, r): u, test)
	controls = su.build_std_control_solvers(calibrate, b, 100, 15)
	treatments = su.build_std_knn_optims(train, calibrate, b, recorder, 1, 15)
	solvers = controls + treatments
	return (train, test_users, b, solvers)

logger = su.BasicLogger()
recorder = su.ScenarioRecorder()
	
su.run_trials(trial_init, su.standard_analyzer_f, num_trials, recorder, logger)
logger.write(output_file)
