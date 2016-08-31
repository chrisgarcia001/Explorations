from os import sys
sys.path.insert(0, '../src/')
from util import *



print('Best Matches ---------')
pats = [(['x', None, 'u', None], 0.2), (['x', None, 'u', 's'], 0.8)]
p1 = ['x','q','u','t']
p2 = ['x','q','u','s']
p3 = ['x','q','v','t']
p4 = ['y','p','u','s']
p5 = ['y','p','v','t']
print(best_match(p1, pats, ignore=[None], patlist_accessor=lambda x: x[0]))
print(best_match(p2, pats, ignore=[None], patlist_accessor=lambda x: x[0]))
print(best_match(p3, pats, ignore=[None], patlist_accessor=lambda x: x[0]))
print(best_match(p4, pats, ignore=[None], patlist_accessor=lambda x: x[0]))
print(best_match(p5, pats, ignore=[None], patlist_accessor=lambda x: x[0]))
print('-----------------------')
cum_vals = [0.05, 0.18, 0.34, 0.67, 1.0]
print(cumulative_bin_search(0.03, cum_vals))
print(cumulative_bin_search(0.33, cum_vals))
print(cumulative_bin_search(0.67, cum_vals))
print(top_n([3,9,1,6,7,4],3))
print(top_n([3,9,1,6,7,4],0))
print(top_n([3,9,1,6,7,4],3, lambda x: x + 1))
print(read_csv_args('data/test_params.txt', ignore_lines = '#'))
print(distinct([[0,0,1],[3,2,4], [0,0,1],[3,2,4]]))
print(unzip([(1,2,3),(4,5,6)]))
print(split_data(range(15), 0.33, 0.33, 0.33))

	
a = Cache()
a[[1,2,3]] = 4
a[[2,4,5]] = 8
print(a[[1,2,3]])
print(a.items())
print(a.has_key([1,2,3]))
print(a.has_key([1,2,5]))

def a_outer(x):
	def a_inner(y):
		print((x, y))
	a_inner(x)

a_outer(2)

try:
	a_inner(3)	
except:
	print('No a_inner - good!')

print(cartesian_prod([[1,2,3],[4,5],[6,7]]))	


