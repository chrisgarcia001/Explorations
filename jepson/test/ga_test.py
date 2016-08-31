from os import sys
sys.path.insert(0, '../src/')
from data_gen import *
from logistic_model_builder import *
from rf_model_builder import *
from ga import *

b = DataGenerator()
b.set_baseline_response_prob(0.02)
b.add_user_attr('Gender', ['M', 'F'])
b.add_user_attr('Age', (0, 100))
b.add_user_attr('Education', ['HS', 'Assoc', 'Bachelors', 'Masters', 'Doctorate'])
b.add_inter_attr('Tone', ['Funny', 'Factual', 'Compassionate'])
b.add_inter_attr('Channel', ['Twitter', 'Facebook', 'Email'])
b.add_inter_attr('Sender', ['Friend', 'Politician', 'Business Leader', 'Famous Actor'])
b.add_inter_attr('Theme', ['Environment', 'Music', 'Business', 'Economy', 'Sports'])
b.set_propensity({'Gender':'M', 'Theme':'Sports', 'Tone':'Funny'}, 0.31)
b.set_propensity({'Gender':'F', 'Education':'Bachelors', 'Theme':'Music', 'Sender':'Famous Actor'}, 0.25)
users, inters, resps = b.gen_random_rows(10000)
model = LogisticModelBuilder()
#model = RandomForestModelBuilder(500)
model.set_data(users, inters, resps)

def log(msg, level):
	print(msg)
	
params = {'logger_f':log, 'max_time':10, 'elitism':0.2, 'max_noimprove_iterations':20, 
			'pop_size':300}
ga_optimizer = GeneticAlgorithm(model.inter_attr_levels(), model.prob_f(), params)
u1 = b.gen_random_user_from_template({'Gender':'M'})
u2 = b.gen_random_user_from_template({'Gender':'F', 'Education':'Bachelors'})
u3 = b.gen_random_user_from_template({'Gender':'F', 'Education':'Doctorate'})
s1 = ga_optimizer.optimize(u1)
s2 = ga_optimizer.optimize(u2)
s3 = ga_optimizer.optimize(u3)
print((s1, s2, s3))