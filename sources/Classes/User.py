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
						"BU"	:		[]
					}
		if idx == None:
			dictKeys = self.__dbContent[userType].keys()
			archiveDictKeys = self.__dbContent["archive"][userType].keys()

			if len(dictKeys) != 0 and len(archiveDictKeys) != 0:
				self.__profile["idx"] = int(max( max(dictKeys), max(archiveDictKeys))) + 1
			elif len(dictKeys) == 0 and len(archiveDictKeys) != 0:
				self.__profile["idx"] = int(max('0', max(archiveDictKeys))) + 1
			elif len(archiveDictKeys) == 0 and len(dictKeys) != 0:
				self.__profile["idx"] = int(max(max(dictKeys), '0')) + 1
			else:
				self.__profile["idx"] = 0
		else:
			self.__profile = self.__dbContent[userType][idx]


	def setName(self, name):
		self.__profile["name"] = name

	def setEntryDate(self, entryDate):
		self.__profile["entryDate"] = entryDate

	def setExitDate(self, exitDate):
		self.__profile["exitDate"] = exitDate

	def setBu(self, bu):
		self.__profile["BU"].append(bu)

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

	def __str__(self):
		return json.dumps(self.__profile, sort_keys=True, indent=4)