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

	def setManagerID(self, managerID):
		self.__profile["managerID"] = managerID

	def setManagerName(self, managerName):
		self.__profile["manager"] = managerName

	def setCurrentClient(self, clientName):
		self.__profile["current_client"] = clientName

	def setMissionStartDate(self, startDate):
		self.__profile["mission_Start"] = startDate

	def setMissionStop(self, stopDate):
		self.__profile["mission_Stop"] = stopDate


	@staticmethod
	def getIngIDfromName(name, DB):
		if name == None:
			return None
		content = DB.getContent()
		out =  [k for k in content["INGs"].keys() if content["INGs"][k]["name"] == name]
		return out[0]

	@staticmethod
	def getNames(database):
		l = []
		content = database.getContent()
		for i, ing in content["INGs"].items():
			if ing['name'] != None:
				l.append(ing['name'])
		return l