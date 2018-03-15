class Functor:
	def __init__(self, functor):
		self.functor = functor
		

class Expression:
	def __init__(self, exp, is_functor=False, variable_identifier = lambda x: str(x).startswith(':')):
		self.is_functor = is_functor
		self.variable_identifier = variable_identifier
		if type(exp) == type('_'):
			self.exp = parse_to_list(exp)
		else:
			#self.exp = exp 
			self.exp = map(lambda x: Expression(x, variable_identifier = variable_identifier ) if type(x) == type([]) else x, exp)
	
	# Match this expression to another. Return the resulting variable bindings as a dict of form {variable: bound_val}.
	def match(self, other_exp, bindings = {}):
		if type(other_exp) == type([]) and len(other_exp) != len(self.exp):
			return False
		for (a, b) in zip(self.exp, other_exp):
			if a.__class__.__name__ == 'Expression':
				if b.__class__.__name__ == 'Expression':
					if a.is_functor != b.is_functor:
						return False
					b = b.exp
				bindings = a.match(b, bindings)
				if bindings == False:
					return False					
			elif type(a) == type([]) and type(b) == type([]):
				if b.__class__.__name__ == 'Expression':
					if a.is_functor != b.is_functor:
						return False
					b = b.exp
				bindings = Expression(a, self.variable_identifier).match(b, bindings)
				if bindings == False:
					return False
			elif self.variable_identifier(a): 
				if bindings.has_key(a) and bindings[a] != b:
					return False
				else:
					bindings[a] = b
			elif a != b:
				return False
		return bindings
		
def parse_to_exp(string_exp):
	return None #TODO - parse a string into proper Expression object.

def parse_to_list(string_exp):
	return [] #TODO - parse a string into proper list expression.
		
		
	