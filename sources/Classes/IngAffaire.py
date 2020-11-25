class IngAffaire(object):
	"""
	Class that describe a business Engineer

	- store :
		name
		role
		activities : his activities through time
		inChargeOf : list of Engineers he's in charge of

	"""
	_ids = 0

	def __init__(self, name, role, idx=None):
		self.name = name
		self.role = role
		self.activities = {}
		self.inChargeOf = []
		if idx == None:
			type(self)._ids += 1
			self.id = IngAffaire._ids
		else:
			self.id = idx
		print("ID", self.id)

	def addActivity(self, week_year, activity):
		self.activities[week_year] = activity

	def addAllActivities(self, activities):
		self.activities = activities

	def save(self, DB):
		data = {
			"name":self.name,
			"role":self.role,
			"activities":self.activities,
			"inChargeOf":self.inChargeOf
		}
		content = DB.getContent()
		content["IAs"][str(self.id)] = data
		DB.write(content)

	def getAllActivities(self, DB):
		content = DB.getContent()
		return content["IAs"][self.id]["activities"]

	def getActivitiesFromWeek(self, DB, week_year):
		content = DB.getContent()
		if week_year in content["IAs"][self.id]["activities"]:
			return content["IAs"][self.id]["activities"][week_year]
		else:
			return [0 for i in range(10)]

	@staticmethod
	def getIngAffaireFromID(idx, DB):
		content = DB.getContent()
		return content["IAs"][idx]

	@staticmethod
	def getIngAffaireIDfromName(name, DB):
		content = DB.getContent()
		return [k for k in content["IAs"].keys() if content["IAs"][k]["name"] == name][0]

	@staticmethod
	def getIngAffaireActivitiesFromID(idx, DB):
		content = DB.getContent()
		return content["IAs"][idx]["activities"]