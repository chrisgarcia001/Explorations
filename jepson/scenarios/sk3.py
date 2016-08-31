from os import sys
sys.path.insert(0, '../src/')
from data_gen import *
from knn import *
import util as ut
import scenario_util as su


b = DataGenerator()
b.set_baseline_response_prob(0.02)
b.add_random_user_attrs(4,4,4) #n_categories, min_levels, max_levels
b.add_random_inter_attrs(4,4,4) #n_categories, min_levels, max_levels
#print(b.user_attrs) # UA_i : L_j
#print(b.inter_attrs) # IA_i : L_j

ut1 = {'UA_1':'L_1', 'UA_2':'L_1', 'UA_3':'L_3'}
mt1 = {'IA_1':'L_1', 'IA_3':'L_3'}
ut2 = {'UA_1':'L_2', 'UA_2':'L_2', 'UA_3':'L_4'}
mt2 = {'IA_1':'L_2', 'IA_3':'L_4'}
ut3 = {'UA_2':'L_3', 'UA_3':'L_1', 'UA_4':'L_2'}
mt3 = {'IA_2':'L_3', 'IA_4':'L_2'}
ut4 = {'UA_1':'L_3', 'UA_3':'L_2', 'UA_4':'L_1'}
mt4 = {'IA_3':'L_2', 'IA_4':'L_1'}
ut5 = {'UA_1':'L_4', 'UA_2':'L_4', 'UA_4':'L_3'}
mt5 = {'IA_2':'L_4', 'IA_4':'L_3'}

b.set_user_inter_propensity(ut1, mt1, 0.5)
b.set_user_inter_propensity(ut2, mt2, 0.5)
b.set_user_inter_propensity(ut3, mt3, 0.5)
b.set_user_inter_propensity(ut4, mt4, 0.99)
b.set_user_inter_propensity(ut5, mt5, 0.5)

rows = []
rows += ut.unzip(b.gen_random_rows_from_template(ut1, mt1, 100))
rows += ut.unzip(b.gen_random_rows_from_template(ut2, mt2, 100))
rows += ut.unzip(b.gen_random_rows_from_template(ut3, mt3, 100))
rows += ut.unzip(b.gen_random_rows_from_template(ut4, mt4, 100))
rows += ut.unzip(b.gen_random_rows_from_template(ut5, mt5, 100))
rows += ut.unzip(b.gen_random_rows(2000))


# Split data into train, calibration, and test.
train, calibrate, test = ut.split_data(rows, 0.5, 0.25, 0.25)
calibration_users = map(lambda (u, m, r): u, calibrate)
test_users = map(lambda (u, m, r): u, test)

# Create three control strategies
best_msgs = su.n_best_messages(test_users, b, 100, 15)
msgs = su.n_best_messages(test_users, b, 100, 100)
ctrl_1 = lambda u: rd.sample(msgs, 1)[0] # Control 1: select a random message each time
ctrl_2 = lambda u: best_msgs[0] # Control 2: Always give the best performing out of the 100
ctrl_3 = lambda u: rd.sample(best_msgs, 1)[0] # Control 3: randomly select one of the top 15 messages for each user

# Build optimizer and attribute selection functions
op = KNNOptimizer()
op.set_data_rows(train)
op.set_similarity_f(match_count)
asf_1 = build_weighted_mode_selector(lambda x: 1)
asf_2 = build_weighted_mode_selector(lambda x: 10**x)
response_f = lambda u, m: b.gen_response(u, m)
k1 = op.find_best_k(calibration_users, 1, 15, asf_1, response_f)
k2 = op.find_best_k(calibration_users, 1, 15, asf_2, response_f)
print('k1, k2: ' + str((k1, k2)))
f_1 = lambda u: op.optimize(u, k1, asf_1)
f_2 = lambda u: op.optimize(u, k2, asf_2)

solvers = [
			(ctrl_1, 'Control Strategy 1 - Random Message for Each User'),
			(ctrl_2, 'Control Strategy 2 - Single Best Test Message for Each User'),
			(ctrl_3, 'Control Strategy 3 - Randomly-Selected Top 15 Message for Each User'),
			(f_1, 'Attribute Selector 1 - Simple Mode-based Attribute Selector'),
			(f_2, 'Attribute Selector 2 -Weighted Mode Selector: 10^(match count)')		
			]
		   

log = su.BasicLogger()
recorder = su.ScenarioRecorder()
su.execute_trial(train, test_users, b, solvers, recorder, logger = log)
