from Classes.User import User
class ING(User):
	"""
	Class that describe an Abylsen Engineer

	- store :
		name
		state : [with-Mission, IC, AR]
		current_client : the current client he's working for
		mission_Start : the date his mission has/(will) started/(start)
		mission_Stop : the date his mission has/(will) stoped/(stop)
	"""
	ING_STATE_IC = 0
	ING_STATE_AM = 1
	ING_STATE_MI = 2

	STATES = {	ING_STATE_IC:"inter-contrat",
				ING_STATE_AM:"arret-maladie",
				ING_STATE_MI:"in mission"}

	def __init__(self, name, database, idx=None):
		super().__init__(database, "INGs", idx)
		self.__profile = self.getProfile()
		self.__name__ = "ING"
		self.setName(name)
		if idx == None:
			self.__profile["prev_mission"] = {}
			self.__profile["state"] = None
			self.state = None
			self.entryDate = None
			self.managerID = None
			self.manager = None
			self.bu = None
			self.current_client = None
			self.mission_Start = None
			self.mission_Stop = None

	def setState(self, ing_state):
		if ing_state in self.STATES.keys():
			self.state = ing_state
			self.__profile["state"] = self.STATES[ing_state]
		else:
			print ("[{Obj}-{fctName}] - warning unknowned state : {val}\nExpected :[{exp1}:{expV1}, {exp2}:{expV2}, {exp3}:{expV3}]".format(
						Obj=self.__name__,
						fctName=self.setState.__name__,
						val=ing_state,
						exp1=self.ING_STATE_IC,
						expV1=self.STATES[self.ING_STATE_IC],
						exp2=self.ING_STATE_AM,
						expV2=self.STATES[self.ING_STATE_AM],
						exp3=self.ING_STATE_MI,
						expV3=self.STATES[self.ING_STATE_MI]))

	def getState(self):
		return self.__profile["state"]

	def getStateKey(self):
		return list(ING.STATES.values()).index(self.__profile["state"])


	def setCurrentClient(self, clientName):
		self.current_client = clientName
		self.__profile["current_client"] = clientName

	def getCurrentClient(self):
		return self.__profile["current_client"]

	def setMissionStart(self, startDate):
		self.mission_Start = startDate
		self.__profile["mission_Start"] = startDate

	def getMissionStart(self):
		return self.__profile["mission_Start"]

	def setMissionStop(self, stopDate):
		self.mission_Stop = stopDate
		self.__profile["mission_Stop"] = stopDate

	def getMissionStop(self):
		return  self.__profile["mission_Stop"]

	def saveCurrentMission(self, missionStop=None):
		l = len(self.__profile["prev_mission"])
		if missionStop == None:
			self.__profile["prev_mission"][str(l)] = {
				"mission_Start":	self.getMissionStart(),
				"mission_Stop":		self.getMissionStop(),
				"client":			self.getCurrentClient()}
		else:
			self.__profile["prev_mission"][str(l)] = {
				"mission_Start":	self.getMissionStart(),
				"mission_Stop":		missionStop,
				"client":			self.getCurrentClient()}

	def startMission(self, startDate, stopDate, client):
		if self.getState() == ING.STATES[ING.ING_STATE_MI]:
			print ("error - stop mission first")
			return
		self.setMissionStart(startDate)
		self.setMissionStop(stopDate)
		self.setCurrentClient(client)
		self.setState(ING.ING_STATE_MI)

	def stopMission(self, nextState, stopDate=None):
		# if self.getState() != ING.STATES[ING.ING_STATE_MI]:
		# 	print ('error - mission not started')
		# 	return
		self.setState(nextState)
		self.saveCurrentMission(stopDate)
		self.setMissionStop(None)
		self.setMissionStart(None)
		self.setCurrentClient(None)

	@staticmethod
	def getNames(database):
		l = []
		content = database.getContent()
		for i, ing in content["INGs"].items():
			if ing['name'] != None:
				l.append(ing['name'])
		return l

	@staticmethod
	def load(database, name):
		currentDbContent = database.getContent()
		for i, ing in currentDbContent["INGs"].items():
			if ing['name'] == name:
				return ING(ing["name"], database, ing["idx"])
		for i, ing in currentDbContent["archive"]["INGs"].items():
			if ing['name'] == name:
				return ING(ing["name"], database, ing["idx"])
		return None