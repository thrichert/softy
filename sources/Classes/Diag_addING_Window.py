from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
from Classes.ING import ING
from Classes.IngAffaire import IngAffaire

class Diag_addING_Window(QtWidgets.QDialog):
	"""
	Class that handle a dialog window to create an Engineer
	"""
	def __init__(self, viewPath, database):
		super(Diag_addING_Window, self).__init__()
		uic.loadUi(viewPath,self)
		self.database = database
		self.dbContent = database.getContent()

		self.userName = self.findChild(QtWidgets.QLineEdit,			"name")
		self.userEntryDate = self.findChild(QtWidgets.QDateEdit,	"entryDate")
		self.bu = self.findChild(QtWidgets.QComboBox, 				"BU")
		self.bu.currentIndexChanged.connect(self._populate_managerList)
		self.userManager = self.findChild(QtWidgets.QComboBox,		"manager")

		self.userState = self.findChild(QtWidgets.QComboBox,		"state")
		self.userClient = self.findChild(QtWidgets.QLineEdit,		"client")

		# set entryDate to current Date
		self.userEntryDate.setDate(QtCore.QDate.currentDate())

		# populate Bu combobox
		for buName in self.dbContent["BUs"]:
			self.bu.addItem(buName)

		# populate manager combobox
		for manager in IngAffaire.getNames(self.database):
			self.userManager.addItem(manager)

		# populate State combobox
		for state in ING.STATES:
			self.userState.addItem(ING.STATES[state])

		# update entry date with current day
		self.userEntryDate.setDate(QtCore.QDate().currentDate())

		# populate ING_managerComboList
		#self._populate_managerList()

		userInputsCheck = False # store condition to exit the loop in case of wrong input

		while not userInputsCheck:
			# prompt dialog
			resp = self.exec_()
			# get user input
			self.userNameText = self.userName.text()
			self.userclientText = self.userClient.text()
			self.userStateText = self.userState.currentText()
			self.userManagerText = self.userManager.currentText()
			#check user input
			if resp == QtWidgets.QDialog.Accepted:
				if self.userNameText == "":
					self._sendAlert("error - Name cannot be empty")
					continue
				if self.userStateText == ING.STATES[ING.ING_STATE_MI] and self.userclientText == "":
					self._sendAlert("error - Client's Name cannot be empty if " + self.userNameText + " is in a mission")
					continue
				if self.userNameText != "":
					# check if name already exists
					if self.userNameText in ING.getNames(self.database):
						self._sendAlert("error - UserName already exist")
						continue
					else:
						userInputsCheck = True
						self._addIng()
			# case cancel
			else:
				break


	def _populate_managerList(self):
		IAsNamelist = []
		self.userManager.clear()
		for ia in self.dbContent["IAs"]:
			if self.bu.currentText() in self.dbContent["IAs"][ia]["BU"]:
				IAsNamelist.append(self.dbContent["IAs"][ia]["name"])
		if IAsNamelist == []:
				IAsNamelist.append("None")
		self.userManager.addItems(IAsNamelist)

	def _sendAlert(self, message):
		alert = QtWidgets.QMessageBox()
		alert.setText(message)
		alert.exec_()

	def _addIng(self):
		#add new ING to db

		newIng = ING(self.userNameText, self.database)
		newIng.setEntryDate(self.userEntryDate.date().toString("dd.MM.yyyy"))

		# if ING as manager => add ing in InChargeOF (IA)
		if self.userManagerText != "None":
			manager = IngAffaire.load(self.database, self.userManagerText)
			manager.putInChargeOf(self.userNameText, newIng.getType())
			manager.save()
			newIng.setManagerID(manager.getID())
			newIng.setManagerName(self.userManagerText)
		else:
			newIng.setManagerName(None)
		self.database.write(self.dbContent)
		newIng.setCurrentClient(self.userclientText)
		for state in ING.STATES:
			if self.userStateText == ING.STATES[state]:
				newIng.setState(state)
		newIng.setBu(self.bu.currentText())
		newIng.save()