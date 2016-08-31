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

log = su.BasicLogger()
recorder = su.ScenarioRecorder()

# Split data into train, calibration, and test.
train, calibrate, test = ut.split_data(rows, 0.5, 0.25, 0.25)
calibration_users = map(lambda (u, m, r): u, calibrate)
test_users = map(lambda (u, m, r): u, test)

controls = su.build_std_control_solvers(calibrate, b, 100, 15)
treatments = su.build_std_knn_optims(train, calibrate, b, recorder, 1, 15)

solvers = controls + treatments
		   
su.execute_trial(train, test_users, b, solvers, recorder, logger = log)
