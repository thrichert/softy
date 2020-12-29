from Classes.User import User

class IngAffaire(User):
	"""
	Class that describe a business Engineer

	- store :
		name
		role
		activities : his activities through time
		inChargeOf : list of Engineers he's in charge of

	"""
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

	_IA_ROLE_IA = 0
	_IA_ROLE_IA_MANAGER = 1
	_IA_ROLE_IA_COACH = 2
	_IA_ROLE_IA_RA = 3
	_IA_ROLE_IA_DA = 4
	_IA_ROLE_IA_DD = 5


	ROLES = {	_IA_ROLE_IA:"ingénieur affaire",
				_IA_ROLE_IA_MANAGER:"manager",
				_IA_ROLE_IA_COACH:"coach",
				_IA_ROLE_IA_RA:"RA",
				_IA_ROLE_IA_DA:"DA",
				_IA_ROLE_IA_DD:"DD"}

	def __init__(self, name, database, idx=None):
		super().__init__(database, "IAs", idx)
		self.__profile = self.getProfile()
		self.__dbContent = self.getdbContent()
		self.__name__ = "IA"
		self.setName(name)
		self.role = None
		self.bu = None
		self.manager = None

		self.__profile["activities"] = {}
		self.__profile["txTranfo"] = [0 for i in range(5)]
		self.__profile["avgPerf"] = [0 for i in range(10)]
		self.__profile["prev_perf"] = {
			"txTransfo":{},
			"avgPerf":{}}
		self.inChargeOf = {"IAs":[],"INGs":[]}

	def setManagerName(self, managerName):
		self.manager = managerName
		self.__profile["manager"] = managerName

	def setRole(self, role):
		if role in self.ROLES.keys():
			self.__profile["role"] = role
		else:
			print ("[{Obj}-{fctName}] - warning unknowned role : {role}\nExpected :[{exp1}:{expV1}, {exp2}:{expV2}, {exp3}:{expV3}...]".format(
						Obj=self.__name__,
						fctName=self.setRole.__name__,
						role=role,
						exp1=self._IA_ROLE_IA,
						expV1=self.ROLES[self._IA_ROLE_IA],
						exp2=self._IA_ROLE_IA_MANAGER,
						expV2=self.ROLES[self._IA_ROLE_IA_MANAGER],
						exp3=self._IA_ROLE_IA_COACH,
						expV3=self.ROLES[self._IA_ROLE_IA_COACH]))

	def addActivity(self, week_year, activity):
		self.__profile["activities"][week_year] = activity

	def getAllActivities(self):
		return self.__profile["activities"]

	def addAllActivities(self, activities):
		self.__profile["activities"] = activities

	def getTxTransfo(self):
		return self.__profile["taux_de_transfo"]

	def getAvgPerf(self):
		return self.__profile["avg_perf"]

	def getActivitiesFromWeek(self, week_year):
		if week_year in self.__profile["activities"]:
			return self.__profile["activities"][week_year]
		else:
			return [0 for i in range(10)]

	def processMetrics(self):
		# get Totaux
		totaux = [0 for i in range(10)]
		if len(self.__profile["activities"]) == 0:
			return
		for activity in self.__profile["activities"]:
			for i in range(10):
				# print("i", i, "activity", activity)
				totaux[i] += int(self.__profile["activities"][activity][i])
		#===============================================
		# process taux de transformation
		#===============================================
		# _BESOIN_PER_PROSP
		if totaux[self._PROSP] == 0:
			self.__profile["txTranfo"][self._BESOIN_PER_PROSP] = 0
		else:
			self.__profile["txTranfo"][self._BESOIN_PER_PROSP] = totaux[self._NVXBESION] / totaux [self._PROSP]
		# _RT_PER_BESOIN
		if totaux[self._NVXBESION] == 0:
			self.__profile["txTranfo"][self._RT_PER_BESOIN] = 0
		else:
			self.__profile["txTranfo"][self._RT_PER_BESOIN] = totaux[self._KLIF] / totaux [self._NVXBESION]
		# _RPLUS_PER_RT
		if totaux[self._KLIF] == 0:
			self.__profile["txTranfo"][self._RPLUS_PER_RT] = 0
		else:
			self.__profile["txTranfo"][self._RPLUS_PER_RT] = totaux[self._START] / totaux[self._KLIF]
		# _EC2_PER_EC1 & _RH_PER_EC1
		som = (totaux[self._PUSHDC] + totaux[self._EC1])
		if som == 0:
			self.__profile["txTranfo"][self._EC2_PER_EC1] = 0
			self.__profile["txTranfo"][self._RH_PER_EC1] = 0
		else:
			self.__profile["txTranfo"][self._EC2_PER_EC1] = totaux[self._EC2] / som
			self.__profile["txTranfo"][self._RH_PER_EC1] = totaux[self._RH] / som

	def saveCurrentMetrics(self, week_year):
		self.__profile["prev_perf"]["txTranfo"][week_year] = self.__profile["txTransfo"]
		self.__profile["prev_perf"]["avg_perf"][week_year] = self.__profile["avg_perf"]


	@staticmethod
	def getIngAffaireIDfromName(name, DB):
		if name == None:
			return None
		content = DB.getContent()
		out =  [k for k in content["IAs"].keys() if content["IAs"][k]["name"] == name]
		return out[0]

	@staticmethod
	def getNames(database):
		l = []
		content = database.getContent()
		for i, ia in content["IAs"].items():
			if ia['name'] != None:
				l.append(ia['name'])
		return l

	@staticmethod
	def load(database, name):
		currentDbContent = database.getContent()
		for i, ia in currentDbContent["IAs"].items():
			if ia['name'] == name:
				return IngAffaire(ia["name"], database, ia["idx"])
		return None
