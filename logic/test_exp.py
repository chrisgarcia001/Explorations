from logic import *

e1 = Expression([':A', '+', [':B', '+', '2']])
print(type(e1))
print(e1.match(['x', '+', ['y', '+', '2']]))
print(e1.match(['x', '+', ['y', '+', '3']]))
print(e1.match(['x', '+', ['y', '+']]))