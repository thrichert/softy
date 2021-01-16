import json

class User(object):
	"""
	Class that describe a Abylsen employe

	- store :
		database : access to main database, allow access for saving

		idx : index to retrieve the dict in Json according to user type
		type : engineer (eng); business eng. (bEng);
		name : user name
		entryDate : hiring date
		exitDate : leaving date
		bu : [] list of business unit the user belong
		profile :	{
						"idx" 	: 		idx
						"type" 	: 		type
						"name"	:		name
						"entryDate" : 	entryDate
						"bu"	:		bu
					}
	"""
	_ING = 0
	_IA = 1
	_USERTYPE = ["INGs", "IAs"]

	def __init__(self, database, userType, idx=None):
		self.__database = database
		if userType in User._USERTYPE:
			pass
		else:
			print ("error - userType not defined in _USERTYPE")
			return None

		self.__dbContent = database.getContent()
		self.__profile = {
						"idx" 	: 		None,
						"type" 	: 		userType,
						"name"	:		None,
						"entryDate" : 	None,
						"exitDate"	:	None,
						"manager":		None,
						"managerID":	None,
						"BU"	:		[]
					}
		if userType == User._USERTYPE[User._IA]:
			self.inChargeOf = {"IAs":[],"INGs":[]}

		if idx == None:
			dictKeys = [int(k) for k in self.__dbContent[userType].keys()]
			archiveDictKeys = [int(k) for k in self.__dbContent["archive"][userType].keys()]
			if len(dictKeys) != 0 and len(archiveDictKeys) != 0:
				self.__profile["idx"] = max( max(dictKeys), max(archiveDictKeys)) + 1
			elif len(dictKeys) == 0 and len(archiveDictKeys) != 0:
				self.__profile["idx"] = max(archiveDictKeys) + 1
			elif len(archiveDictKeys) == 0 and len(dictKeys) != 0:
				self.__profile["idx"] = max(dictKeys) + 1
			else:
				self.__profile["idx"] = 0
		else:
			if str(idx) in self.__dbContent[userType].keys():
				self.__profile = self.__dbContent[userType][str(idx)]
			elif str(idx) in self.__dbContent["archive"][userType].keys():
				self.__profile = self.__dbContent["archive"][userType][str(idx)]


	def setName(self, name):
		self.__profile["name"] = name

	def getName(self):
		return self.__profile["name"]

	def setEntryDate(self, entryDate):
		self.__profile["entryDate"] = entryDate

	def getEntryDate(self):
		return self.__profile["entryDate"]

	def setExitDate(self, exitDate):
		self.__profile["exitDate"] = exitDate

	def getExitDate(self):
		return self.__profile["exitDate"]

	def setBu(self, bu):
		if bu != "None":
			if not bu in self.__dbContent["BUs"].keys():
				self.__dbContent["BUs"][bu] = {"INGs":[], "IAs":[]}
			if not self.__profile["name"] in self.__dbContent["BUs"][bu][self.__profile["type"]]:
				self.__dbContent["BUs"][bu][self.__profile["type"]].append(self.__profile["name"])
			if not bu in self.__profile["BU"]:
				self.__profile["BU"].append(bu)

	def getBu(self):
		return ', '.join(self.__profile["BU"])

	def removeFromBu(self, bu):
		if bu in self.__profile["BU"]:
			self.__profile["BU"].pop(self.__profile["BU"].index(bu))

	def removeFromInCharge(self, name, usertype):
		if self.__profile["type"] == User._USERTYPE[User._IA]:
			if not "inChargeOf" in self.__profile.keys():
				return
			self.__profile["inChargeOf"][usertype].pop(self.__profile["inChargeOf"][usertype].index(name))


	def setManagerID(self, managerID):
		self.__profile["managerID"] = managerID

	def setManagerName(self, managerName):
		self.__profile["manager"] = managerName

	def getManagerName(self):
		return self.__profile["manager"]

	def getManagerID(self):
		return self.__profile["managerID"]

	def putInChargeOf(self, name, usertype):
		if self.__profile["type"] == User._USERTYPE[User._IA]:
			self.inChargeOf[usertype].append(name)
			self.__profile["inChargeOf"] = self.inChargeOf

	def isManagerIA(self):
		if self.__profile["type"] == User._USERTYPE[User._IA]:
			if not "inChargeOf" in self.__profile.keys():
				return False
			if self.__profile["inChargeOf"]["IAs"] != []:
				return True
		return False

	def isManagerING(self):
		if self.__profile["type"] == User._USERTYPE[User._IA]:
			if not "inChargeOf" in self.__profile.keys():
				return False
			if self.__profile["inChargeOf"]["INGs"] != []:
				return True
		return False

	def whoIsManaged(self, usertype):
		if self.__profile["type"] == User._USERTYPE[User._IA]:
			if not "inChargeOf" in self.__profile.keys():
				return []
		return self.__profile["inChargeOf"][usertype]

	def save(self):
		currentDbContent = self.__database.getContent()
		currentDbContent[self.__profile["type"]][str(self.__profile["idx"])] = self.__profile
		self.__database.write(currentDbContent)

	def getID(self):
		return self.__profile["idx"]

	def getProfile(self):
		return self.__profile

	def getdbContent(self):
		return self.__dbContent

	def getType(self):
		return self.__profile["type"]

	def toArchive(self, motif):
		t = self.__profile["type"]
		i = str(self.__profile["idx"])
		# save current state
		self.save()
		# store in archive
		currentDbContent = self.__database.getContent()
		currentDbContent["archive"][t][i] = currentDbContent[t][i]
		currentDbContent["archive"][t][i]["motif"] = motif
		# remove from BUs
		for bu in self.__profile["BU"]:
			currentDbContent["BUs"][bu][t].pop(currentDbContent["BUs"][bu][t].index(self.__profile["name"]))
		# remove from valid list
		currentDbContent[t].pop(i)
		self.__database.write(currentDbContent)

	def delete(self, exitDate, motif):
		self.setExitDate(exitDate)
		# update managed ing and ia
		if self.isManagerIA():
			for ia in self.__profile["inChargeOf"]["IAs"]:
				managedIa = User.load(self.__database, ia, User._USERTYPE[User._IA])
				if managedIa != None:
					managedIa.setManagerID(None)
					managedIa.setManagerName(None)
					managedIa.save()
		if self.isManagerING():
			for ing in self.__profile["inChargeOf"]["INGs"]:
				managedIng = User.load(self.__database, User._USERTYPE[User._ING], ing)
				if managedIng != None:
					managedIng.setManagerID(None)
					managedIng.setManagerName(None)
					managedIng.save()
		if self.__profile["manager"] != None:
				manager = User.load(self.__database, User._USERTYPE[User._IA], self.__profile["manager"])
				if manager != None:
					manager.removeFromInCharge(self.__profile["name"], self.__profile["type"])
					manager.save()
		self.toArchive(motif)

	def __str__(self):
		return json.dumps(self.__profile, sort_keys=True, indent=4)

	@staticmethod
	def load(database, userType, name):
		currentDbContent = database.getContent()
		for i, usr in currentDbContent[userType].items():
			if usr['name'] == name:
				return User(database, userType, usr["idx"])
		for i, usr in currentDbContent["archive"][userType].items():
			if usr['name'] == name:
				return User(database, userType, usr["idx"])
		return None