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
	def __init__(self, name):
		self.name = name
		self.state = None
		self.current_client = None
		self.mission_Start = None
		self.mission_Stop = None

	def setState(self, state):
		self.state = state

	def setCurrentClient(self, clientName):
		self.current_client = clientName

	def setMissionStartDate(self, startDate):
		self.mission_Start = startDate

	def setMissionStop(self, stopDate):
		self.mission_Stop = stopDate