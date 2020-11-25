class IngAffaire(object):
	"""
	Class that describe a business Engineer

	- store :
		name
		role
		activities : his activities through time
		inChargeOf : list of Engineers he's in charge of

	"""
	def __init__(self, name, role):
		self.name = name
		self.role = role
		self.activities = {}
		self.inChargeOf = []