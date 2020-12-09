class ING(object):
	"""
	Class that describe an Abylsen Engineer

	- store :
		name
		state : [with-Mission, IC, AR]
		current_client : the current client he's working for
		mission_Start : the date his mission has/(will) started/(start)
		mission_Stop : the date his mission has/(will) stoped/(stop)
	"""

	def __init__(self, name, database, idx=None):
		self.database = database
		self.dbContent = database.getContent()
		self.name = name
		self.state = None
		self.entryDate = None
		self.managerID = None
		self.manager = None
		self.bu = None
		self.current_client = None
		self.mission_Start = None
		self.mission_Stop = None
		if idx == None:
			ING_key = self.dbContent["INGs"].keys()
			archiveING_id = self.dbContent["archive"]["INGs"].keys()

			if len(ING_key) != 0 and len(archiveING_id) != 0:
				self.id = int(max( max(ING_key), max(archiveING_id))) + 1
			elif len(ING_key) == 0 and len(archiveING_id) != 0:
				self.id = int(max('0', max(archiveING_id))) + 1
			elif len(archiveING_id) == 0 and len(ING_key) != 0:
				self.id = int(max(max(ING_key), '0')) + 1
			else:
				self.id = 0
		else:
			self.id = idx

	def setState(self, state):
		self.state = state

	def setEntryDate(self, entryDate):
		self.entryDate = entryDate

	def setManagerID(self, managerID):
		self.managerID = managerID

	def setManagerName(self, managerName):
		self.manager = managerName

	def setCurrentClient(self, clientName):
		self.current_client = clientName

	def setMissionStartDate(self, startDate):
		self.mission_Start = startDate

	def setMissionStop(self, stopDate):
		self.mission_Stop = stopDate

	def setBu(self, Bu):
		self.bu = Bu

	def save(self, DB):
		data = {
			"name" :			self.name,
			"state":			self.state,
			"entryDate":		self.entryDate,
			"manager":			self.manager,
			"managerID":		self.managerID,
			"BU":				self.bu,
			"current_client":	self.current_client,
			"mission_Start":	self.mission_Start,
			"mission_Stop":		self.mission_Stop
		}
		content = DB.getContent()
		content["INGs"][str(self.id)] = data
		DB.write(content)

	@staticmethod
	def getIngFromID(idx, DB):
		content = DB.getContent()
		return content["INGs"][idx]

	@staticmethod
	def getIngIDfromName(name, DB):
		if name == None:
			return None
		content = DB.getContent()
		out =  [k for k in content["INGs"].keys() if content["INGs"][k]["name"] == name]
		return out[0]
