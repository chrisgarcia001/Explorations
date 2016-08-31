from os import sys
sys.path.insert(0, '../src/')
from data_gen import *
from util import *
from knn import *

print(match_count([1,2,3], [1,1,3]))

b = DataGenerator()
b.set_baseline_response_prob(0.1)
b.add_user_attr('Gender', ['M', 'F'])
b.add_user_attr('Age', (0, 100))
b.add_user_attr('Education', ['HS', 'Assoc', 'Bachelors', 'Masters', 'Doctorate'])
b.add_inter_attr('Tone', ['Funny', 'Factual', 'Compassionate'])
b.add_inter_attr('Channel', ['Twitter', 'Facebook', 'Email'])
b.add_inter_attr('Sender', ['Friend', 'Politician', 'Business Leader', 'Famous Actor'])
b.add_inter_attr('Theme', ['Environment', 'Music', 'Business', 'Economy', 'Sports'])
b.set_propensity({'Gender':'M', 'Theme':'Sports', 'Tone':'Funny'}, 0.45)
b.set_propensity({'Gender':'F', 'Education':'Bachelors', 'Theme':'Music', 'Sender':'Famous Actor'}, 0.5)
users, inters, resps = b.gen_random_rows(10000)

data = ut.unzip(b.gen_random_rows(1960))
data += ut.unzip(b.gen_random_rows_from_template({'Gender':'M'}, {'Theme':'Sports', 'Tone':'Funny'}, 200))
data += ut.unzip(b.gen_random_rows_from_template({'Gender':'F', 'Education':'Bachelors'}, {'Theme':'Music', 'Sender':'Famous Actor'}, 200))

o1 = KNNOptimizer()
print(o1.normalize([([[1,2,3], [4,5,6]], 50), ([[7,8,9], [10,11,12]], 100)]))
o1.set_data_rows(data)
o1.set_similarity_f(match_count)

u1 = b.gen_random_user_from_template({'Gender':'M'})
u2 = b.gen_random_user_from_template({'Gender':'F', 'Education':'Bachelors'})
u3 = b.gen_random_user_from_template({'Gender':'F', 'Education':'Doctorate'})

att_selector_f = build_weighted_mode_selector(lambda x: 1)
s1 = o1.optimize(u1, 10, att_selector_f)
s2 = o1.optimize(u2, 10, att_selector_f)
s3 = o1.optimize(u2, 10, att_selector_f)
print((s1, s2, s3))