from os import sys
sys.path.insert(0, '../src/')
from data_gen import *
from util import *
from knn1 import *

print(hamming([1,2,3], [1,1,3]))
print(mode([1,2,3,2,2,2,1,4]))
print(mean([2,3,4]))
print(max_net_occurrences_in([1,2,3,1,2,3,1,2,3],[1,2,1,2,3,1,2,1]))

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

data = ut.unzip(b.gen_random_rows(1000))

o1 = KNNOptimizer()
o1.set_data_rows(data)
o1.set_distance_f(hamming)

u1 = b.gen_random_user_from_template({'Gender':'M'})
u2 = b.gen_random_user_from_template({'Gender':'F', 'Education':'Bachelors'})
u3 = b.gen_random_user_from_template({'Gender':'F', 'Education':'Doctorate'})
s1 = o1.optimize(u1, 5, o1.f2)
s2 = o1.optimize(u2, 5, o1.f2)
s3 = o1.optimize(u3, 5, o1.f2)
print((s1, s2, s3))