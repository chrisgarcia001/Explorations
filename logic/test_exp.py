from logic import *

e1 = Expression([':A', '+', [':B', '+', '2']])

e2 = Expression(['x', '+', ['y', '+', '2']])
e3 = Expression(['x', '+', ['y', '+', '3']])
e4 = Expression(['x', '+', ['y', '+']])
print(type(e1))
print(e1.match(['y', '+', ['x', '+', '2']]))
print(e1.match(['x', '+', ['y', '+', '3']]))
print(e1.match(['y', '+', ['x', '+']]))

print(e1.match(e2))
print(e1.match(e3))
print(e1.match(e4))

e5 = Expression([':A', '_', '_'])
print(e5.match(e2))
print(e5.match(['x', '+', ['y', '+', '3']]))
print(e5.exp)