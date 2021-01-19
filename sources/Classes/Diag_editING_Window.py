from PyQt5 import QtWidgets, uic, QtCore, QtGui
from Classes.IngAffaire import IngAffaire
from Classes.ING import ING
from Classes.User import User

class Diag_editING_Window(QtWidgets.QDialog):
	"""
		Class that handle a dialog window to Edit an Engineer
		> edit name, entry date, BUs he belongs ...
		> prompt stats total number of mission and longest
	"""
	def __init__(self, viewPath, selectedIng, database):
		super(Diag_editING_Window, self).__init__()
		uic.loadUi(viewPath, self)
		self.__database = database
		self.__dbContent = database.getContent()
		# get selected ing
		self.ing = ING.load(database, selectedIng)

		###################################
		# get elements from ui
		###################################
		self.userName = self.findChild(QtWidgets.QLineEdit, "name")
		self.entryDate = self.findChild(QtWidgets.QDateEdit, "entryDate")
		self.BU_label = self.findChild(QtWidgets.QLabel, "BU_label")
		self.scrollArea_Bus = self.findChild(QtWidgets.QScrollArea, "scrollArea_Bus")
		self.manager_label = self.findChild(QtWidgets.QLabel, "manager_label")
		self.scrollArea_IAs = self.findChild(QtWidgets.QScrollArea, "scrollArea_IAs")
		self.userState = self.findChild(QtWidgets.QComboBox, "ing_State_comboBox")

		self.curMissionStartDate = self.findChild(QtWidgets.QDateEdit, "curMissionStartDate")
		self.curMissionStopDate = self.findChild(QtWidgets.QDateEdit, "curMissionStopDate")
		self.curClientName = self.findChild(QtWidgets.QLineEdit, "curClientName")

		self.addPrevMission = self.findChild(QtWidgets.QPushButton, "addPrevMission")
		self.delPrevMission = self.findChild(QtWidgets.QPushButton, "delPrevMission")
		self.scrollArea_prevMission = self.findChild(QtWidgets.QScrollArea, "scrollArea_prevMission")

		self.totalMissionLabel = self.findChild(QtWidgets.QLabel, "totalMissionLabel")
		self.longestMissionLabel = self.findChild(QtWidgets.QLabel, "longestMissionLabel")
		###################################
		# setup element
		###################################
		self.userName.setText(self.ing.getName())
		self.entryDate.setDate(QtCore.QDate().fromString(self.ing.getEntryDate(), "dd.MM.yyyy"))
		ingBUsStr = self.ing.getBu()
		self.BU_label.setText(ingBUsStr)

		# setup - scroll area layout
		self.scrollAreaLayout_Bus = QtWidgets.QVBoxLayout()
		self.containerBUs = QtWidgets.QWidget()
		self.containerBUs.setLayout(self.scrollAreaLayout_Bus)
		self.scrollArea_Bus.setWidget(self.containerBUs)
		self.BUs_checkBox = []
		self.BUs_checked = []
		i = 0
		for bu in self.__dbContent["BUs"]:
			self.BUs_checkBox.append(QtWidgets.QCheckBox(bu))
			# TODO need to add call back when checked or unchecked
			if bu in ingBUsStr:
				self.BUs_checkBox[i].setChecked(True)
				self.BUs_checked.append(bu)
			self.scrollAreaLayout_Bus.addWidget(self.BUs_checkBox[i])
			i += 1

		ingManagerName = self.ing.getManagerName()
		self.manager_label.setText(ingManagerName)
		self.scrollAreaLayout_IAs = QtWidgets.QVBoxLayout()
		self.containerIAs = QtWidgets.QWidget()
		self.containerIAs.setLayout(self.scrollAreaLayout_IAs)
		self.scrollArea_IAs.setWidget(self.containerIAs)
		self.Mgr_checkBox = []
		i = 0
		for bu in self.BUs_checked:
			for iaName in self.__dbContent["BUs"][bu]["IAs"]:
				self.Mgr_checkBox.append(QtWidgets.QCheckBox(iaName))
				if ingManagerName == iaName:
					self.Mgr_checkBox[i].setChecked(True)
				self.scrollAreaLayout_IAs.addWidget(self.Mgr_checkBox[i])
				i += 1

		for state in ING.STATES:
			self.userState.addItem(ING.STATES[state])
			if ING.STATES[state] == self.ing.getState():
				self.userState.setCurrentText(ING.STATES[state])

		startMiStr = self.ing.getMissionStart()
		stopMiStr = self.ing.getMissionStop()
		startMiDate = QtCore.QDate().fromString(startMiStr, "dd.MM.yyyy")
		stopMiDate = QtCore.QDate().fromString(stopMiStr, "dd.MM.yyyy")
		if startMiStr != None and stopMiStr != None:
			self.curMissionStartDate.setDate(startMiDate)
			self.curMissionStopDate.setDate(stopMiDate)
			self.curClientName.setText(self.ing.getCurrentClient())
		else:
			self.curMissionStartDate.setEnabled(False)
			self.curMissionStopDate.setEnabled(False)
			self.curClientName.setEnabled(False)
		## TODO create call back for add/del prev mission

		self.scrollAreaLayout_prevMission = QtWidgets.QVBoxLayout()
		self.containerPrevMission = QtWidgets.QWidget()
		self.containerPrevMission.setLayout(self.scrollAreaLayout_prevMission)
		self.scrollArea_prevMission.setWidget(self.containerPrevMission)
		self.prevMission_checkBox = []
		prevMissions = self.ing.getPrevMissions()
		i = 0
		for miID in prevMissions:
			text = "Client : {client} - start : {start} / stop : {stop}".format(client=prevMissions[miID]["client"], start=prevMissions[miID]["mission_Start"], stop=prevMissions[miID]["mission_Stop"])
			self.prevMission_checkBox.append(QtWidgets.QCheckBox(text))
			self.scrollAreaLayout_prevMission.addWidget(self.prevMission_checkBox[i])
			i += 1

		# prompt metrics
		if self.ing.getState() == ING.STATES[ING.ING_STATE_MI]:
			self.totalMissionLabel.setText(str(len(prevMissions) + 1))
		else:
			self.totalMissionLabel.setText(str(len(prevMissions)))

		nMonth = 0
		while startMiDate < stopMiDate:
			startMiDate = startMiDate.addMonths(1)
			nMonth += 1
		self.longestMissionLabel.setText("{Mo} Months".format(Mo=str(nMonth)))
		resp = self.exec_()
		if resp == QtWidgets.QDialog.Accepted:
			print ("CheckModif")
			print ("doModif")
		else:
			print("Nop")