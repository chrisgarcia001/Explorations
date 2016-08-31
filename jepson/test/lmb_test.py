from os import sys
sys.path.insert(0, '../src/')
from logistic_model_builder import *

u1 = ['A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'C']
u2 = ['P', 'Q', 'R', 'P', 'Q', 'R', 'P', 'Q', 'R', 'P', 'Q', 'R', 'P', 'Q', 'R', 'P', 'Q']
i1 = range(len(u1))
i2 = ['X', 'Y', 'X', 'Y', 'X', 'X', 'X', 'Y', 'X', 'Y', 'X', 'Y', 'X', 'Y', 'X', 'Y', 'X']
r =  [1,    0,   1,   0,   1,   0,   0,   1,   0,   1,   0,   1,   0,   0,   0,   1,   1]
r2 = [1,    0,   1,   0,   1,   1,   1,   0,   1,   0,   1,   0,   1,   0,   1,   1,   1]

user_data = map(lambda x: list(x), zip(u1, u2))
inter_data = map(lambda x: list(x), zip(i1, i2))
model = LogisticModelBuilder()
model.set_data(user_data, inter_data, r2)
				
user_test_data =  [['A', 'P'], ['A', 'Q'], ['B', 'R'], ['C', 'Q'], ['C', 'P']]
inter_test_data = [[2, 'X'],   [19, 'Y'],  [12, 'X'],  [6, 'Y'],   [3, 'X']]
				
print(model.inter_attr_levels())
f = model.prob_f()
print(map(lambda (x, y): f(x, y), zip(user_test_data, inter_test_data)))