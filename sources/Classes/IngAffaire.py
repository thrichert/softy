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
	#==============================
	# activity constants ; used as index
	_PROSP = 0
	_NVXBESION = 1
	_BESOINACTIF = 2
	_KLIF = 3
	_START = 4
	_PUSHDC = 5
	_EC1 = 6
	_EC2 = 7
	_PPLS = 8
	_RH = 9
	#==============================

	#==============================
	# metrics constants ; used as index in Tx de transfo
	_BESOIN_PER_PROSP = 0
	_RT_PER_BESOIN = 1
	_RPLUS_PER_RT = 2
	_EC2_PER_EC1 = 3
	_RH_PER_EC1 = 4
	#==============================

	#==============================
	# metrics constants ; used as index in avg Perf
	_AVG_PROSP = 0
	_AVG_BESOIN = 1
	_AVG_RT = 2
	_AVG_RPLUS = 3
	_AVG_EC1_BM = 4
	_AVG_EC1_CDR = 5
	_AVG_EC2 = 6
	_AVG_PROPAL = 7
	#==============================


	def __init__(self, name=None, role=None, idx=None):
		self.name = name
		self.role = role
		self.activities = {}
		self.inChargeOf = []
		self.txTranfo = [0 for i in range(5)]
		self.avgPerf = [0 for i in range(10)]
		if idx == None:
			type(self)._ids += 1
			self.id = IngAffaire._ids
		else:
			self.id = idx

	def addActivity(self, week_year, activity):
		self.activities[week_year] = activity

	def addAllActivities(self, activities):
		self.activities = activities

	def save(self, DB):
		data = {
			"name":				self.name,
			"role":				self.role,
			"activities":		self.activities,
			"inChargeOf":		self.inChargeOf,
			"taux_de_transfo":	self.txTranfo,
			"avg_perf":			self.avgPerf
		}
		content = DB.getContent()
		content["IAs"][str(self.id)] = data
		DB.write(content)

	def getTxTransfo(self, DB):
		content = DB.getContent()
		return content["IAs"][self.id]["taux_de_transfo"]

	def getAvgPerf(self, DB):
		content = DB.getContent()
		return content["IAs"][self.id]["avg_perf"]

	def getAllActivities(self, DB):
		content = DB.getContent()
		return content["IAs"][self.id]["activities"]

	def getActivitiesFromWeek(self, DB, week_year):
		content = DB.getContent()
		if week_year in content["IAs"][self.id]["activities"]:
			return content["IAs"][self.id]["activities"][week_year]
		else:
			return [0 for i in range(10)]

	def processMetrics(self):
		# get Totaux
		totaux = [0 for i in range(10)]
		if len(self.activities) == 0:
			return
		for activity in self.activities:
			for i in range(10):
				# print("i", i, "activity", activity)
				totaux[i] += int(self.activities[activity][i])
		#===============================================
		# process taux de transformation
		#===============================================
		# _BESOIN_PER_PROSP
		if totaux[self._PROSP] == 0:
			self.txTranfo[self._BESOIN_PER_PROSP] = 0
		else:
			self.txTranfo[self._BESOIN_PER_PROSP] = totaux[self._NVXBESION] / totaux [self._PROSP]
		# _RT_PER_BESOIN
		if totaux[self._NVXBESION] == 0:
			self.txTranfo[self._RT_PER_BESOIN] = 0
		else:
			self.txTranfo[self._RT_PER_BESOIN] = totaux[self._KLIF] / totaux [self._NVXBESION]
		# _RPLUS_PER_RT
		if totaux[self._KLIF] == 0:
			self.txTranfo[self._RPLUS_PER_RT] = 0
		else:
			self.txTranfo[self._RPLUS_PER_RT] = totaux[self._START] / totaux[self._KLIF]
		# _EC2_PER_EC1 & _RH_PER_EC1
		som = (totaux[self._PUSHDC] + totaux[self._EC1])
		if som == 0:
			self.txTranfo[self._EC2_PER_EC1] = 0
			self.txTranfo[self._RH_PER_EC1] = 0
		else:
			self.txTranfo[self._EC2_PER_EC1] = totaux[self._EC2] / som
			self.txTranfo[self._RH_PER_EC1] = totaux[self._RH] / som

	def loadFromDB(self, DB):
		content = DB.getContent()
		# check if ia_id match
		dictKey = content["IAs"].keys()
		if self.id in dictKey:
			self.name = content["IAs"][self.id]["name"]
			self.role = content["IAs"][self.id]["role"]
			self.activities = content["IAs"][self.id]["activities"]
			self.inChargeOf = content["IAs"][self.id]["inChargeOf"]
			self.txTranfo = content["IAs"][self.id]["taux_de_transfo"]
			self.avgPerf = content["IAs"][self.id]["avg_perf"]
			return self
		else:
			print('Nop')
			return None

	@staticmethod
	def getIngAffaireFromID(idx, DB):
		content = DB.getContent()
		return content["IAs"][idx]

	@staticmethod
	def getIngAffaireIDfromName(name, DB):
		if name == None:
			return None
		content = DB.getContent()
		out =  [k for k in content["IAs"].keys() if content["IAs"][k]["name"] == name]
		return out[0]

	@staticmethod
	def getIngAffaireActivitiesFromID(idx, DB):
		content = DB.getContent()
		return content["IAs"][idx]["activities"]