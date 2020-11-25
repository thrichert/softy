class ING(object):
	"""
	Class that describe an Abylsen Engineer

	- store :
		name
		state : []
		current_client : the current client he's working for
		mission_Start : the date his mission has/(will) started/(start)
		mission_Stop : the date his mission has/(will) stoped/(stop)
	"""
	_ids = 0

	def __init__(self, name, idx=None):
		self.name = name
		self.state = None
		self.current_client = None
		self.mission_Start = None
		self.mission_Stop = None
		if idx == None:
			type(self)._ids += 1
			self.id = ING._ids
		else:
			self.id = idx

	def setState(self, state):
		self.state = state

	def setCurrentClient(self, clientName):
		self.current_client = clientName

	def setMissionStartDate(self, startDate):
		self.mission_Start = startDate

	def setMissionStop(self, stopDate):
		self.mission_Stop = stopDate

	def save(self, DB):
		data = {
			"name" : self.name,
			"state": self.state,
			"current_client": self.current_client,
			"mission_Start": self.mission_Start,
			"mission_Stop": self.mission_Stop
		}
		content = DB.getContent()
		content["INGs"][self.id] = data
		DB.write(content)
